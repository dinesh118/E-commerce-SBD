from pydantic import BaseModel, constr, conint, confloat

class ProductBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    rate: confloat(gt=0)
    stock: conint(ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
