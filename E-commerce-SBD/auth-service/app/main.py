from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.connection import Base, engine
from app.routes.auth import router as auth_router

# Create tables for the shared PostgreSQL database.
# This service owns the users table.
Base.metadata.create_all(bind=engine)
with engine.begin() as connection:
    connection.execute(
        text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) NOT NULL DEFAULT 'customer'")
    )

app = FastAPI(title="Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}
