# Smart Inventory Management System

Interview-ready full-stack project built with React.js + Python Flask + MySQL.

## Features
- JWT login/register
- Admin/user roles
- Product CRUD
- Category management
- Supplier management
- Stock in/out transactions
- Automatic stock update when orders are created
- Low-stock and out-of-stock alerts
- Order management and status updates
- Dashboard statistics and charts
- Search/filter
- REST APIs
- Sample data loader
- Postman collection

## Requirements
- Python 3.10+
- Node.js 18+
- MySQL 8+
- VS Code

## 1. Database
Create a MySQL database:

```sql
CREATE DATABASE smart_inventory;
```

Then run `database/schema.sql` in MySQL Workbench.

Optional sample data:
```bash
cd backend
python seed.py
```

## 2. Backend
```bash
cd backend
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and edit the MySQL password.

Start:
```bash
python app.py
```

Backend: http://127.0.0.1:5000

## 3. Frontend
Open another VS Code terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally:
http://localhost:5173

## Demo accounts
After running `python seed.py`:
- Admin: admin@inventory.com / Admin@123
- Staff: staff@inventory.com / Staff@123

## API
Base URL: http://127.0.0.1:5000/api

See `postman/inventory-api.json`.

## Project architecture

React.js -> REST API -> Flask -> MySQL

The frontend stores the JWT token and sends it in the Authorization header.
