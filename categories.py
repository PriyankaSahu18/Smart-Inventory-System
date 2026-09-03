from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from db import get_connection
categories_bp=Blueprint("categories",__name__)

@categories_bp.get("")
@jwt_required()
def list_categories():
    conn=get_connection(); cur=conn.cursor(dictionary=True); cur.execute("SELECT * FROM categories ORDER BY name"); rows=cur.fetchall(); conn.close(); return {"categories":rows}

@categories_bp.post("")
@jwt_required()
def create_category():
    d=request.get_json() or {}; name=d.get("name")
    if not name:return {"message":"Name required"},400
    conn=get_connection(); cur=conn.cursor(); cur.execute("INSERT INTO categories(name) VALUES(%s)",(name,)); conn.commit(); cid=cur.lastrowid; conn.close()
    return {"id":cid,"message":"Category created"},201
