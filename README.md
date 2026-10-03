# E-Commerce SBD

This project is a learning e-commerce application built with FastAPI and React. The backend has been split into three independent services while keeping the same PostgreSQL database and preserving the existing frontend API paths for auth, products, and cart.

## Project goals

- Separate authentication from product and cart logic
- Keep the same PostgreSQL database for now
- Allow each backend service to run independently
- Preserve the existing frontend behavior as much as possible
- Keep the app simple and suitable for learning and local development

## Current architecture

The application now contains:

- Auth service: handles customer and admin authentication
- Product service: handles product listing and management
- Cart service: handles add-to-cart, fetch cart, update quantity, and remove item
- Frontend: React + Vite UI for login, customer dashboard, admin dashboard, and cart page

## Service ports

- Auth service: 8001
- Product service: 8002
- Cart service: 8003
- Frontend: 5173

## Main project structure

```text
E-commerce-SBD/
├── auth-service/
│   ├── app/
│   ├── requirements.txt
│   └── .env.example
├── product-service/
│   ├── app/
│   ├── requirements.txt
│   └── .env.example
├── cart-service/
│   ├── app/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
├── backend/   # existing monolithic backend kept for compatibility during migration
├── README.md
└── .gitignore
```

## Shared database

All services currently use the same PostgreSQL database:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
```

The logical ownership is:

- Auth service -> users
- Product service -> products
- Cart service -> cart_items

## PostgreSQL setup

1. Create the database:

```sql
CREATE DATABASE ecommerce_db;
```

2. Set the database URL in each service environment file.

Example:

```env
DATABASE_URL=postgresql://dinesh:dinesh123@localhost:5432/ecommerce_db
```

If you already have a working `.env` in the old backend, you can copy it into each service folder before running the apps.

## Backend service setup

### Auth service

```powershell
cd E-commerce-SBD/auth-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Product service

```powershell
cd E-commerce-SBD/product-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Cart service

```powershell
cd E-commerce-SBD/cart-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run all backend services

### Auth service

```powershell
cd E-commerce-SBD/auth-service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Product service

```powershell
cd E-commerce-SBD/product-service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

### Cart service

```powershell
cd E-commerce-SBD/cart-service
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

## Frontend setup

```powershell
cd E-commerce-SBD/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Open:

```text
http://localhost:5173
```

## Frontend API paths

The frontend is designed to keep the same API path structure when routed through a gateway or reverse proxy:

- /auth/*
- /products/*
- /cart/*

This means the frontend does not need a major rewrite if the deployed environment proxies requests to the appropriate service.

## Service API contracts

### Auth service

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/admin-login`

### Product service

- `GET /products`
- `POST /products`
- `PUT /products/{product_id}`

### Cart service

- `POST /cart`
- `GET /cart/{user_id}`
- `PUT /cart/{cart_item_id}`
- `DELETE /cart/{cart_item_id}`

## Example requests

### Register user

```http
POST /auth/register
Content-Type: application/json

{
  "username": "dinesh",
  "password": "dinesh123",
  "confirm_password": "dinesh123"
}
```

### Customer login

```http
POST /auth/login
Content-Type: application/json

{
  "username": "dinesh",
  "password": "dinesh123"
}
```

### Admin login

```http
POST /auth/admin-login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### Get products

```http
GET /products
```

### Add product

```http
POST /products
Content-Type: application/json

{
  "name": "iphone",
  "rate": 50000,
  "stock": 5
}
```

### Add item to cart

```http
POST /cart
Content-Type: application/json

{
  "user_id": 1,
  "product_id": 1,
  "quantity": 1
}
```

## Notes on the migration

- The project keeps the same PostgreSQL database for now.
- This is a service split, not a full distributed microservice architecture.
- No order, payment, inventory, or notification services were added.
- The cart service avoids importing user and product SQLAlchemy models directly to keep the services independent.
- The frontend can remain stable if requests are routed via Nginx or a gateway.

## Current limitations

- No authentication token system yet
- No service-to-service communication layer yet
- No database containerization or migration management
- No production-level API gateway configuration yet
- No deployment automation yet

## Quick troubleshooting

If the app fails to start, confirm:

- PostgreSQL is running locally
- The `.env` file contains the correct `DATABASE_URL`
- Each service is started on the correct port
- There is no port conflict with another local app

## Important

This split is intentionally scoped to the requested migration. It does not introduce unrelated services or architectural changes beyond the auth, product, and cart service split.
