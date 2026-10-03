from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.routes.products import router as products_router

# Create tables for the shared PostgreSQL database.
# This service owns the products table.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "products"}
