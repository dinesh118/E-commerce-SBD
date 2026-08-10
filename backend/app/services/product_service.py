from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import Product


def get_all_products(db: Session):
    return db.query(Product).all()


def create_product(db: Session, name: str, rate: float, stock: int) -> Product:
    existing_product = db.query(Product).filter(Product.name == name).first()
    if existing_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this name already exists")

    product = Product(name=name, rate=rate, stock=stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, name: str, rate: float, stock: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product.name = name
    product.rate = rate
    product.stock = stock
    db.commit()
    db.refresh(product)
    return product
