from pydantic import BaseModel, ConfigDict, conint, confloat, constr


class ProductBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    rate: confloat(gt=0)
    stock: conint(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
