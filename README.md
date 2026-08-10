# E-Commerce Learning Project (Version 0.1)

## Project Overview

This is a simple monolithic e-commerce learning application. It includes:
- Customer registration and login
- Admin login with fixed credentials
- Product viewing for customers
- Product add/update for admins
- PostgreSQL database persistence
- FastAPI backend with SQLAlchemy and Pydantic
- React frontend with Vite

## Architecture

- Backend: `backend/`
- Frontend: `frontend/`
- Backend provides REST APIs for authentication and products.
- Frontend communicates with backend at `http://localhost:8000`.

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- React
- Vite
- JavaScript

## Folder Structure

backend/
- `app/main.py` - FastAPI application entry point
- `app/database/connection.py` - SQLAlchemy database connection
- `app/models/` - SQLAlchemy models for users and products
- `app/schemas/` - Pydantic request and response schemas
- `app/routes/` - API routes for auth and products
- `app/services/` - Business logic for auth and products
- `.env.example` - Example environment variables
- `.gitignore` - Ignore local env and venv files
- `requirements.txt` - Python dependencies

frontend/
- `src/App.jsx` - React router and app shell
- `src/main.jsx` - React entry point
- `src/components/` - Login, registration, product list, and product form components
- `src/pages/` - Login page, customer dashboard, admin dashboard
- `src/services/api.js` - Fetch wrapper for backend API
- `src/index.css` - Basic styles
- `package.json` - Frontend dependencies and scripts
- `vite.config.js` - Vite config
- `.gitignore` - Ignore node_modules and build output

## PostgreSQL Setup

1. Install PostgreSQL.
2. Create database:

```sql
CREATE DATABASE ecommerce_db;
```

3. Set `DATABASE_URL` in `backend/.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
```

## Backend Setup

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Frontend Setup

```powershell
cd frontend
npm install
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string

## How to Run Backend

```powershell
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

## How to Run Frontend

```powershell
cd frontend
npm run dev
```

## API Endpoints

- `GET /health` - Health check
- `POST /auth/register` - Register a new customer
- `POST /auth/login` - Customer login
- `POST /auth/admin-login` - Admin login (`admin` / `admin`)
- `GET /products` - List products
- `POST /products` - Add product
- `PUT /products/{product_id}` - Update product

## Sample API Requests

Register:

```http
POST /auth/register
Content-Type: application/json

{
  "username": "user1",
  "password": "strongpass",
  "confirm_password": "strongpass"
}
```

Customer login:

```http
POST /auth/login
Content-Type: application/json

{
  "username": "user1",
  "password": "strongpass"
}
```

Admin login:

```http
POST /auth/admin-login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

Add product:

```http
POST /products
Content-Type: application/json

{
  "name": "Dell Laptop",
  "rate": 65000,
  "stock": 10
}
```

Update product:

```http
PUT /products/1
Content-Type: application/json

{
  "name": "Dell Laptop",
  "rate": 64000,
  "stock": 12
}
```

## Current Limitations

- Admin credentials are fixed in code for version 0.1.
- No token-based session persistence.
- No product deletion.
- Simple UI and no production-ready auth flows.
