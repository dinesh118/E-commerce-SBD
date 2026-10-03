from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.routes.cart import router as cart_router

# Create tables for the shared PostgreSQL database.
# This service owns the cart_items table.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cart Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cart_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "cart"}
