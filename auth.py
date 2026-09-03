from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    name, email, password = data.get("name"), data.get("email"), data.get("password")
    if not all([name, email, password]):
        return {"message": "Name, email and password are required"}, 400
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cur.fetchone():
        conn.close()
        return {"message": "Email already registered"}, 409
    cur.execute(
        "INSERT INTO users(name,email,password_hash,role) VALUES(%s,%s,%s,%s)",
        (name, email, generate_password_hash(password), "staff")
    )
    conn.commit()
    conn.close()
    return {"message": "Registration successful"}, 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id,name,email,password_hash,role FROM users WHERE email=%s", (data.get("email"),))
    user = cur.fetchone()
    conn.close()
    if not user or not check_password_hash(user["password_hash"], data.get("password","")):
        return {"message": "Invalid email or password"}, 401
    token = create_access_token(identity=str(user["id"]))
    return {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}}

@auth_bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id,name,email,role FROM users WHERE id=%s", (uid,))
    user = cur.fetchone()
    conn.close()
    return {"user": user}
