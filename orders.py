from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_connection
orders_bp=Blueprint("orders",__name__)

@orders_bp.get("")
@jwt_required()
def list_orders():
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    cur.execute("""SELECT o.*,u.name customer_name FROM orders o LEFT JOIN users u ON u.id=o.created_by ORDER BY o.created_at DESC""")
    rows=cur.fetchall(); conn.close(); return {"orders":rows}

@orders_bp.post("")
@jwt_required()
def create_order():
    d=request.get_json() or {}; items=d.get("items",[])
    if not items:return {"message":"At least one item is required"},400
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    try:
        total=0
        for item in items:
            cur.execute("SELECT id,name,price,stock_quantity FROM products WHERE id=%s FOR UPDATE",(item["product_id"],))
            p=cur.fetchone()
            q=int(item.get("quantity",0))
            if not p or q<=0: raise ValueError("Invalid product or quantity")
            if p["stock_quantity"]<q: raise ValueError(f"Insufficient stock for {p['name']}")
            total += float(p["price"])*q
        cur.execute("INSERT INTO orders(customer_name,total_amount,status,created_by) VALUES(%s,%s,%s,%s)",
                    (d.get("customer_name","Walk-in Customer"),total,"PENDING",int(get_jwt_identity())))
        oid=cur.lastrowid
        for item in items:
            q=int(item["quantity"]); cur.execute("SELECT price FROM products WHERE id=%s",(item["product_id"],)); price=cur.fetchone()["price"]
            cur.execute("INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES(%s,%s,%s,%s)",(oid,item["product_id"],q,price))
            cur.execute("UPDATE products SET stock_quantity=stock_quantity-%s WHERE id=%s",(q,item["product_id"]))
            cur.execute("INSERT INTO stock_transactions(product_id,type,quantity,reference,note,user_id) VALUES(%s,'OUT',%s,%s,%s,%s)",
                        (item["product_id"],q,f"ORDER-{oid}","Order stock deduction",int(get_jwt_identity())))
        conn.commit()
    except Exception as e:
        conn.rollback(); conn.close(); return {"message":str(e)},400
    conn.close(); return {"message":"Order created","order_id":oid},201

@orders_bp.patch("/<int:oid>/status")
@jwt_required()
def update_status(oid):
    status=(request.get_json() or {}).get("status")
    allowed=["PENDING","CONFIRMED","PROCESSING","SHIPPED","DELIVERED","CANCELLED"]
    if status not in allowed:return {"message":"Invalid status"},400
    conn=get_connection(); cur=conn.cursor(); cur.execute("UPDATE orders SET status=%s WHERE id=%s",(status,oid)); conn.commit(); a=cur.rowcount; conn.close()
    return {"message":"Status updated" if a else "Order not found"},(200 if a else 404)
