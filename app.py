from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from routes.auth import auth_bp
from routes.products import products_bp
from routes.categories import categories_bp
from routes.suppliers import suppliers_bp
from routes.inventory import inventory_bp
from routes.orders import orders_bp
from routes.dashboard import dashboard_bp

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
CORS(app, resources={r"/api/*": {"origins": "*"}})
JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(products_bp, url_prefix="/api/products")
app.register_blueprint(categories_bp, url_prefix="/api/categories")
app.register_blueprint(suppliers_bp, url_prefix="/api/suppliers")
app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
app.register_blueprint(orders_bp, url_prefix="/api/orders")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Inventory API is running"}

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
