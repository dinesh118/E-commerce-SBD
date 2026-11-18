from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.security import TokenPrincipal, get_current_user
from app.services.product_service import create_product, delete_product, get_all_products, get_product, update_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.post("", response_model=ProductResponse, status_code=201)
def add_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    require_admin(current_user)
    return create_product(db, product_data.name, product_data.rate, product_data.stock)


@router.put("/{product_id}", response_model=ProductResponse)
def edit_product(
    product_data: ProductUpdate,
    product_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    require_admin(current_user)
    return update_product(db, product_id, product_data.name, product_data.rate, product_data.stock)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(
    product_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: TokenPrincipal = Depends(get_current_user),
):
    require_admin(current_user)
    delete_product(db, product_id)


@router.get("/{product_id}", response_model=ProductResponse)
def product_details(
    product_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    _current_user: TokenPrincipal = Depends(get_current_user),
):
    return get_product(db, product_id)


def require_admin(current_user: TokenPrincipal) -> None:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
