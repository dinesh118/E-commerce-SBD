from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.database.connection import get_db
from app.services.product_service import get_all_products, create_product, update_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.post("", response_model=ProductResponse, status_code=201)
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data.name, product_data.rate, product_data.stock)


@router.put("/{product_id}", response_model=ProductResponse)
def edit_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db, product_id, product_data.name, product_data.rate, product_data.stock)
