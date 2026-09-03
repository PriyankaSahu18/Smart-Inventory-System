from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from db import get_connection
suppliers_bp=Blueprint("suppliers",__name__)

@suppliers_bp.get("")
@jwt_required()
def list_suppliers():
    conn=get_connection(); cur=conn.cursor(dictionary=True); cur.execute("SELECT * FROM suppliers ORDER BY name"); rows=cur.fetchall(); conn.close(); return {"suppliers":rows}

@suppliers_bp.post("")
@jwt_required()
def create_supplier():
    d=request.get_json() or {}
    if not d.get("name"): return {"message":"Supplier name required"},400
    conn=get_connection(); cur=conn.cursor(); cur.execute("INSERT INTO suppliers(name,email,phone) VALUES(%s,%s,%s)",(d["name"],d.get("email"),d.get("phone"))); conn.commit(); sid=cur.lastrowid; conn.close()
    return {"id":sid,"message":"Supplier created"},201
