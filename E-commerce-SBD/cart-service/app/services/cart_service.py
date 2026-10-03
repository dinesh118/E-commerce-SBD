from fastapi import HTTPException, status
from sqlalchemy import MetaData, Table, select
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.models.cart import CartItem

metadata = MetaData()
user_table = Table("users", metadata, autoload_with=engine)
product_table = Table("products", metadata, autoload_with=engine)


def _get_user_row(db: Session, user_id: int):
    stmt = select(user_table).where(user_table.c.id == user_id)
    return db.execute(stmt).first()


def _get_product_row(db: Session, product_id: int):
    stmt = select(product_table).where(product_table.c.id == product_id)
    return db.execute(stmt).first()


def _serialize_cart_item(db: Session, cart_item: CartItem):
    product_row = _get_product_row(db, cart_item.product_id)
    if not product_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product = product_row._mapping
    return {
        "id": cart_item.id,
        "user_id": cart_item.user_id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "product_name": product["name"],
        "product_rate": product["rate"],
        "product_stock": product["stock"],
    }


def get_cart_for_user(db: Session, user_id: int):
    if not _get_user_row(db, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    return [_serialize_cart_item(db, item) for item in items]


def add_item_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    if not _get_user_row(db, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    product_row = _get_product_row(db, product_id)
    if not product_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product = product_row._mapping
    if quantity > product["stock"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {product['stock']} units available")

    existing_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()
    if existing_item:
        new_quantity = existing_item.quantity + quantity
        if new_quantity > product["stock"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {product['stock']} units available in stock")
        existing_item.quantity = new_quantity
        db.commit()
        db.refresh(existing_item)
        return _serialize_cart_item(db, existing_item)

    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return _serialize_cart_item(db, cart_item)


def update_cart_item(db: Session, cart_item_id: int, quantity: int):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    product_row = _get_product_row(db, cart_item.product_id)
    if not product_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product = product_row._mapping
    if quantity > product["stock"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {product['stock']} units available")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return _serialize_cart_item(db, cart_item)


def delete_cart_item(db: Session, cart_item_id: int):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}
