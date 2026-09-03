from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_connection
inventory_bp=Blueprint("inventory",__name__)

@inventory_bp.post("/transaction")
@jwt_required()
def transaction():
    d=request.get_json() or {}
    pid, qty, typ = d.get("product_id"), int(d.get("quantity",0)), d.get("type")
    if not pid or qty<=0 or typ not in ("IN","OUT"): return {"message":"product_id, positive quantity and type IN/OUT required"},400
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    cur.execute("SELECT stock_quantity FROM products WHERE id=%s FOR UPDATE",(pid,)); p=cur.fetchone()
    if not p: conn.rollback(); conn.close(); return {"message":"Product not found"},404
    newstock=p["stock_quantity"]+qty if typ=="IN" else p["stock_quantity"]-qty
    if newstock<0: conn.rollback(); conn.close(); return {"message":"Insufficient stock"},400
    cur2=conn.cursor()
    cur2.execute("UPDATE products SET stock_quantity=%s WHERE id=%s",(newstock,pid))
    cur2.execute("INSERT INTO stock_transactions(product_id,type,quantity,reference,note,user_id) VALUES(%s,%s,%s,%s,%s,%s)",
                 (pid,typ,qty,d.get("reference"),d.get("note"),int(get_jwt_identity())))
    conn.commit(); conn.close()
    return {"message":"Stock updated","new_stock":newstock}

@inventory_bp.get("/transactions")
@jwt_required()
def transactions():
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    cur.execute("""SELECT t.*,p.name product_name,u.name user_name FROM stock_transactions t
                   JOIN products p ON p.id=t.product_id LEFT JOIN users u ON u.id=t.user_id
                   ORDER BY t.created_at DESC""")
    rows=cur.fetchall(); conn.close(); return {"transactions":rows}
