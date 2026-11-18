from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemUpdate
from app.security import TokenPrincipal, get_current_user
from app.services.cart_service import add_item_to_cart, delete_cart_item, get_cart_for_user, update_cart_item

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    return add_item_to_cart(
        db, current_user.user_id, item_data.product_id, item_data.quantity, current_user.access_token
    )


@router.get("", response_model=list[CartItemResponse])
def list_current_cart(
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    return get_cart_for_user(db, current_user.user_id, current_user.access_token)


@router.get("/{user_id}", response_model=list[CartItemResponse])
def list_legacy_cart_path(
    user_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot access another user's cart")
    return get_cart_for_user(db, current_user.user_id, current_user.access_token)


@router.put("/{cart_item_id}", response_model=CartItemResponse)
def edit_cart_item(
    cart_item_id: int = Path(gt=0),
    item_data: CartItemUpdate = ...,
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    return update_cart_item(
        db, cart_item_id, current_user.user_id, item_data.quantity, current_user.access_token
    )


@router.delete("/{cart_item_id}")
def remove_cart_item(
    cart_item_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    return delete_cart_item(db, cart_item_id, current_user.user_id)
