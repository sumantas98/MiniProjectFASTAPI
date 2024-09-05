from fastapi.openapi.models import Schema
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: int
    description: str


class CustomDisplay(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True
