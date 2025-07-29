from pydantic import BaseModel, Field, ConfigDict

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(gt=0)

class ProductOut(ProductCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)