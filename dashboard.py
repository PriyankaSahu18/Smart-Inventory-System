from flask import Blueprint
from flask_jwt_extended import jwt_required
from db import get_connection
dashboard_bp=Blueprint("dashboard",__name__)

@dashboard_bp.get("")
@jwt_required()
def dashboard():
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) total_products, COALESCE(SUM(stock_quantity),0) total_stock, COALESCE(SUM(CASE WHEN stock_quantity<=reorder_level AND stock_quantity>0 THEN 1 ELSE 0 END),0) low_stock, COALESCE(SUM(CASE WHEN stock_quantity=0 THEN 1 ELSE 0 END),0) out_of_stock FROM products")
    stats=cur.fetchone()
    cur.execute("SELECT COUNT(*) total_orders, COALESCE(SUM(total_amount),0) total_sales, COALESCE(SUM(status='PENDING'),0) pending_orders FROM orders")
    stats.update(cur.fetchone())
    cur.execute("""SELECT c.name, COUNT(p.id) product_count FROM categories c LEFT JOIN products p ON p.category_id=c.id GROUP BY c.id ORDER BY product_count DESC""")
    by_category=cur.fetchall()
    cur.execute("""SELECT status,COUNT(*) count FROM orders GROUP BY status""")
    order_status=cur.fetchall()
    conn.close()
    return {"stats":stats,"by_category":by_category,"order_status":order_status}
