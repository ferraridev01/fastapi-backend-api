from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    category: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)


class ProductUpdate(BaseModel):
    category: str | None = Field(None, min_length=3, max_length=50)
    name: str | None = Field(None, min_length=3, max_length=100)
    price: float | None = Field(None, gt=0)


class ProductResponse(BaseModel):
    id: int
    category: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)

    class Config:
        from_attributes = True
