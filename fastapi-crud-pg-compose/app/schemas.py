from typing import Optional
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    price: float = Field(ge=0)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, ge=0)

class ItemOut(ItemBase):
    id: int

    class Config:
        from_attributes = True
