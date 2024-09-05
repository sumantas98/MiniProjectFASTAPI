from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: int
    description: str


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

    class Config:
        orm_mode = True
