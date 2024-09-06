from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship('Seller', back_populates='products')


class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    products = relationship('Product', back_populates='seller')

