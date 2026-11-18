# E-commerce Microservices

This repository contains three FastAPI services backed by PostgreSQL:

| Service | Default port | Owns |
| --- | ---: | --- |
| Auth Service | 8001 | `users` |
| Product Service | 8002 | `products` |
| Cart Service | 8003 | `cart_items` |

The services currently use the same PostgreSQL database, but each service owns its own tables. Cart records store user and product IDs as integers; Cart Service does not use cross-service SQLAlchemy models or foreign keys. Cart Service obtains product data from Product Service over HTTP.

## Requirements

- Python 3.10 or later
- PostgreSQL
- Network access between Cart Service and Product Service

The example assumes the services run on one host. Configure Nginx or another reverse proxy to expose the public API; keep the service ports private to that host/network. No frontend or Nginx configuration is included in this repository.

## Configuration

Each service loads environment variables from its own `.env` file. Copy the relevant example and set values for your environment:

```sh
cp auth-service/.env.example auth-service/.env
cp product-service/.env.example product-service/.env
cp cart-service/.env.example cart-service/.env
```

Set `DATABASE_URL` to the PostgreSQL database connection string in all three files. Set the **same random `JWT_SECRET_KEY`** in each service. Use at least 32 random characters; do not use the example placeholder or commit `.env` files.

Auth Service:

```dotenv
DATABASE_URL=postgresql://admin:password@localhost:5432/ecommerce_db
JWT_SECRET_KEY=<same-long-random-secret-in-all-services>
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Product Service:

```dotenv
DATABASE_URL=postgresql://admin:password@localhost:5432/ecommerce_db
JWT_SECRET_KEY=<same-long-random-secret-in-all-services>
```

Cart Service:

```dotenv
DATABASE_URL=postgresql://admin:password@localhost:5432/ecommerce_db
JWT_SECRET_KEY=<same-long-random-secret-in-all-services>
PRODUCT_SERVICE_URL=http://127.0.0.1:8002
```

`PRODUCT_SERVICE_URL` must be an absolute HTTP or HTTPS URL reachable from Cart Service. Cart-to-product requests have a 2-second connect timeout and a 5-second overall timeout; they are not retried indefinitely.

## Install and run

Run each service in a separate terminal from the repository root. The `--host 127.0.0.1` binding keeps these ports local to the machine; adjust it only if your network and firewall are configured to protect the services.

Auth Service:

```sh
python -m pip install -r auth-service/requirements.txt
cd auth-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Product Service:

```sh
python -m pip install -r product-service/requirements.txt
cd product-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

Cart Service:

```sh
python -m pip install -r cart-service/requirements.txt
cd cart-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8003
```

Each service creates its own tables at startup. Auth Service also adds a `role` column to an existing `users` table if needed, defaulting existing and new users to `customer`.

Health checks:

```sh
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
curl http://127.0.0.1:8003/health
```

Interactive API documentation is available at `http://127.0.0.1:<port>/docs`.

## Authentication and roles

Registration creates a customer account. Passwords are stored as bcrypt hashes. Login verifies the password and returns an HS256 JWT with the user ID, role, and expiration. Protected endpoints expect:

```http
Authorization: Bearer <access-token>
```

There is no built-in admin account or public endpoint for granting admin privileges. To grant admin privileges, use a trusted, access-controlled database administration session:

```sql
UPDATE users SET role = 'admin' WHERE username = 'your-admin-username';
```

Existing tokens keep their claims until they expire. Have the promoted user log in again to receive a token with the new role. Do not expose database administration credentials to clients.

## API routes

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | Public | Register a customer |
| `POST` | `/auth/login` | Public | Verify credentials and return a JWT |
| `POST` | `/auth/admin-login` | Public | Log in an existing admin account; returns 403 for non-admins |
| `GET` | `/auth/me` | Bearer token | Return the authenticated user's ID, username, and role |
| `GET` | `/products` | Public | List products |
| `GET` | `/products/{product_id}` | Bearer token | Get one product; used by Cart Service |
| `POST` | `/products` | Admin bearer token | Create a product |
| `PUT` | `/products/{product_id}` | Admin bearer token | Update a product |
| `DELETE` | `/products/{product_id}` | Admin bearer token | Delete a product |
| `POST` | `/cart` | Bearer token | Add an item to the authenticated user's cart |
| `GET` | `/cart` | Bearer token | Get the authenticated user's cart |
| `GET` | `/cart/{user_id}` | Bearer token | Compatibility route; only the token owner's ID is accepted |
| `PUT` | `/cart/{cart_item_id}` | Bearer token | Update an item owned by the authenticated user |
| `DELETE` | `/cart/{cart_item_id}` | Bearer token | Delete an item owned by the authenticated user |

Product create/update request fields are `name`, `rate` (greater than zero), and `stock` (zero or greater). Cart add requests contain only `product_id` (positive integer) and `quantity` (integer of at least one); the user ID is always taken from the JWT.

Typical errors include `401` for missing, invalid, or expired tokens; `403` for insufficient role or another user's cart item; `404` for missing products or cart items; and `503` if Product Service cannot serve a cart's product lookup.

## Request flow

1. A customer registers and logs in with Auth Service.
2. Auth Service checks the stored password hash and issues a JWT.
3. The client sends that token to protected Product Service or Cart Service routes.
4. Product Service verifies the JWT for product detail and admin operations; product listing is public.
5. Cart Service verifies the JWT and derives the cart owner from its user ID claim.
6. When adding, viewing, or updating cart items, Cart Service requests product details from Product Service over HTTP, forwarding the bearer token.
7. Cart Service checks product existence and stock before saving or updating the cart record.

## Test the main flow

The following examples use Bash and `curl`. Run them after all services are configured and running. Replace the sample credentials and IDs as needed.

### Register and log in a customer

```sh
curl -i -X POST http://127.0.0.1:8001/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"customer-pass-1","confirm_password":"customer-pass-1"}'
```

Expected: `201 Created` with an ID, username, and `role: customer`. No password or password hash is returned.

```sh
CUSTOMER_TOKEN=$(curl -s -X POST http://127.0.0.1:8001/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"customer-pass-1"}' |
  python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
```

Expected: a response containing `access_token`, `token_type: bearer`, and the user details.

```sh
curl -i http://127.0.0.1:8001/auth/me \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
```

Expected: `200 OK` with Alice's ID, username, and role.

### List products and create one as an admin

Product listing is public:

```sh
curl -i http://127.0.0.1:8002/products
```

To create an admin, register a separate account, grant it the `admin` role through a trusted database session as described above, then log in:

```sh
ADMIN_TOKEN=$(curl -s -X POST http://127.0.0.1:8001/auth/admin-login \
  -H 'Content-Type: application/json' \
  -d '{"username":"your-admin-username","password":"your-admin-password"}' |
  python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
```

Create a product with the admin token:

```sh
curl -i -X POST http://127.0.0.1:8002/products \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Sample product","rate":19.99,"stock":10}'
```

Expected: `201 Created` with the product object. Save its returned `id` as `PRODUCT_ID`.

### Add and inspect a cart item

```sh
curl -i -X POST http://127.0.0.1:8003/cart \
  -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"product_id":<PRODUCT_ID>,"quantity":1}'
```

Replace `<PRODUCT_ID>` with the numeric ID returned by product creation. Expected: `201 Created` with cart item and product details.

```sh
curl -i http://127.0.0.1:8003/cart \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
```

Expected: `200 OK` with Alice's cart. To update or delete an item, use its returned cart item ID:

```sh
curl -i -X PUT http://127.0.0.1:8003/cart/<CART_ITEM_ID> \
  -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"quantity":2}'

curl -i -X DELETE http://127.0.0.1:8003/cart/<CART_ITEM_ID> \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
```

### Verify authorization and errors

- Add a nonexistent product to the cart: expect `404 Not Found`.
- Call `/cart` without an `Authorization` header: expect `401 Unauthorized`.
- Use an invalid or expired token for a protected route: expect `401 Unauthorized`.
- Use Alice's token with another user's ID at `/cart/{user_id}`, or Alice's token with another user's cart item ID: expect `403 Forbidden`.
- Stop Product Service and try adding a cart item: expect `503 Service Unavailable`.
- Use a customer token to create, update, or delete a product: expect `403 Forbidden`.

## Dependencies

- Auth Service: FastAPI, Uvicorn, SQLAlchemy, psycopg, python-dotenv, passlib[bcrypt], PyJWT.
- Product Service: FastAPI, Uvicorn, SQLAlchemy, psycopg, python-dotenv, PyJWT.
- Cart Service: FastAPI, Uvicorn, SQLAlchemy, psycopg, python-dotenv, PyJWT, httpx.
