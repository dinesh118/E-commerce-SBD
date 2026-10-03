from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemUpdate
from app.services.cart_service import add_item_to_cart, delete_cart_item, get_cart_for_user, update_cart_item

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(item_data: CartItemCreate, db: Session = Depends(get_db)):
    return add_item_to_cart(db, item_data.user_id, item_data.product_id, item_data.quantity)


@router.get("/{user_id}", response_model=list[CartItemResponse])
def list_cart(user_id: int, db: Session = Depends(get_db)):
    return get_cart_for_user(db, user_id)


@router.put("/{cart_item_id}", response_model=CartItemResponse)
def edit_cart_item(cart_item_id: int, item_data: CartItemUpdate, db: Session = Depends(get_db)):
    return update_cart_item(db, cart_item_id, item_data.quantity)


@router.delete("/{cart_item_id}")
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    return delete_cart_item(db, cart_item_id)
