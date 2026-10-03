from pydantic import BaseModel, ConfigDict, conint


class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: conint(ge=1)


class CartItemUpdate(BaseModel):
    quantity: conint(ge=1)


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    quantity: int
    product_name: str
    product_rate: float
    product_stock: int
