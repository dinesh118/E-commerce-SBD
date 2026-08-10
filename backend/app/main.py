from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine, Base
from app.routes.auth import router as auth_router
from app.routes.products import router as products_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce V0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router)


@app.get("/health")
def health():
    return {"status": "ok"}
