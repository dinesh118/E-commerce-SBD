from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cart import CartItem
from app.services.product_client import ProductDetails, get_product_details


def _serialize_cart_item(cart_item: CartItem, product: ProductDetails):
    return {
        "id": cart_item.id,
        "user_id": cart_item.user_id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "product_name": product.name,
        "product_rate": product.rate,
        "product_stock": product.stock,
    }


def get_cart_for_user(db: Session, user_id: int, access_token: str):
    items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    return [
        _serialize_cart_item(item, get_product_details(item.product_id, access_token))
        for item in items
    ]


def add_item_to_cart(db: Session, user_id: int, product_id: int, quantity: int, access_token: str):
    product = get_product_details(product_id, access_token)
    if quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} units available",
        )

    existing_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        .first()
    )
    if existing_item:
        new_quantity = existing_item.quantity + quantity
        if new_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {product.stock} units available in stock",
            )
        existing_item.quantity = new_quantity
        db.commit()
        db.refresh(existing_item)
        return _serialize_cart_item(existing_item, product)

    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return _serialize_cart_item(cart_item, product)


def _get_owned_item(db: Session, cart_item_id: int, user_id: int) -> CartItem:
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    if cart_item.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cart item belongs to another user")
    return cart_item


def update_cart_item(
    db: Session,
    cart_item_id: int,
    user_id: int,
    quantity: int,
    access_token: str,
):
    cart_item = _get_owned_item(db, cart_item_id, user_id)
    product = get_product_details(cart_item.product_id, access_token)
    if quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} units available",
        )

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return _serialize_cart_item(cart_item, product)


def delete_cart_item(db: Session, cart_item_id: int, user_id: int):
    cart_item = _get_owned_item(db, cart_item_id, user_id)
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}
