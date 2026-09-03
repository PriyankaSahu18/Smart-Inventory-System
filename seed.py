from db import get_connection
from werkzeug.security import generate_password_hash

conn=get_connection(); cur=conn.cursor()
cur.execute("INSERT IGNORE INTO users(name,email,password_hash,role) VALUES(%s,%s,%s,%s)",("Admin User","admin@inventory.com",generate_password_hash("Admin@123"),"admin"))
cur.execute("INSERT IGNORE INTO users(name,email,password_hash,role) VALUES(%s,%s,%s,%s)",("Staff User","staff@inventory.com",generate_password_hash("Staff@123"),"staff"))
cur.execute("INSERT IGNORE INTO categories(name) VALUES(%s),(%s),(%s)",("Electronics","Office Supplies","Accessories"))
cur.execute("INSERT IGNORE INTO suppliers(name,email,phone) VALUES(%s,%s,%s),(%s,%s,%s)",("Tech Supplier","sales@techsupplier.com","9876543210","Office World","contact@officeworld.com","9123456780"))
cur.execute("SELECT id FROM categories ORDER BY id LIMIT 3"); cats=[x[0] for x in cur.fetchall()]
cur.execute("SELECT id FROM suppliers ORDER BY id LIMIT 2"); sups=[x[0] for x in cur.fetchall()]
products=[("Laptop Pro","LAP-001",cats[0],sups[0],65000,25,5),("Wireless Mouse","MOU-001",cats[2],sups[0],1200,4,10),("Keyboard","KEY-001",cats[2],sups[0],1800,35,10),("Printer Paper","PAP-001",cats[1],sups[1],450,0,5)]
for p in products:
    cur.execute("""INSERT IGNORE INTO products(name,sku,category_id,supplier_id,price,stock_quantity,reorder_level)
                   VALUES(%s,%s,%s,%s,%s,%s,%s)""",p)
conn.commit(); conn.close(); print("Seed completed.")
