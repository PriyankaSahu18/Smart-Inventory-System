from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from db import get_connection

products_bp = Blueprint("products", __name__)

@products_bp.get("")
@jwt_required()
def list_products():
    search = request.args.get("search","")
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT p.*, c.name category_name, s.name supplier_name
                   FROM products p LEFT JOIN categories c ON p.category_id=c.id
                   LEFT JOIN suppliers s ON p.supplier_id=s.id
                   WHERE p.name LIKE %s OR p.sku LIKE %s ORDER BY p.id DESC""",
                (f"%{search}%", f"%{search}%"))
    rows = cur.fetchall(); conn.close()
    return {"products": rows}

@products_bp.post("")
@jwt_required()
def create_product():
    d=request.get_json() or {}
    required=["name","sku","price","stock_quantity","reorder_level"]
    if any(d.get(x) is None for x in required):
        return {"message":"name, sku, price, stock_quantity and reorder_level are required"},400
    conn=get_connection(); cur=conn.cursor()
    try:
        cur.execute("""INSERT INTO products(name,sku,category_id,supplier_id,price,stock_quantity,reorder_level)
                       VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                    (d["name"],d["sku"],d.get("category_id"),d.get("supplier_id"),d["price"],d["stock_quantity"],d["reorder_level"]))
        conn.commit(); pid=cur.lastrowid
    except Exception as e:
        conn.rollback(); conn.close(); return {"message":str(e)},400
    conn.close(); return {"message":"Product created","id":pid},201

@products_bp.put("/<int:pid>")
@jwt_required()
def update_product(pid):
    d=request.get_json() or {}
    conn=get_connection(); cur=conn.cursor()
    cur.execute("""UPDATE products SET name=%s,sku=%s,category_id=%s,supplier_id=%s,price=%s,
                   stock_quantity=%s,reorder_level=%s WHERE id=%s""",
                (d.get("name"),d.get("sku"),d.get("category_id"),d.get("supplier_id"),d.get("price"),
                 d.get("stock_quantity",0),d.get("reorder_level",0),pid))
    conn.commit(); affected=cur.rowcount; conn.close()
    return {"message":"Product updated" if affected else "Product not found"}, (200 if affected else 404)

@products_bp.delete("/<int:pid>")
@jwt_required()
def delete_product(pid):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s",(pid,)); conn.commit(); affected=cur.rowcount; conn.close()
    return {"message":"Product deleted" if affected else "Product not found"}, (200 if affected else 404)
