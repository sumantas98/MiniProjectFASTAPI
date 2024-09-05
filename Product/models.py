from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from .database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)


class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)