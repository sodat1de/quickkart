from pydantic import BaseModel, Field, ConfigDict

class OrderCreate(BaseModel):
    item: str = Field(min_length=1)


class OrderOut(BaseModel):
    id: int
    user_email: str
    item: str
    model_config = ConfigDict(from_attributes=True)
