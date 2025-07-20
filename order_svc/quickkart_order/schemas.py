from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    item: str = Field(min_length=1)


class OrderOut(BaseModel):
    id: int
    user_email: str
    item: str

    class Config:
        orm_mode = True
