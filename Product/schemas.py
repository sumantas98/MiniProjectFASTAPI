from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: int
    description: str
    seller_id: int


class Seller(BaseModel):
    name: str
    username: str
    password: str
    email: str
    phone: str
    address: str


class DisplaySeller(BaseModel):
    name: str
    username: str
    email: str
    phone: str
    address: str

    class Config:
        orm_mode = True


class CustomDisplay(BaseModel):
    name: str
    description: str
    seller: DisplaySeller

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
