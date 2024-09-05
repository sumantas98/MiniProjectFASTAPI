from fastapi import APIRouter
from fastapi import APIRouter, Response, HTTPException
from typing import List
from .. import schemas
from .. import models
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import getDB
from starlette import status
from passlib.context import CryptContext

router = APIRouter(
    tags=['Seller']
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Add New Seller in Seller DB
@router.post('/addSeller', response_model=schemas.DisplaySeller)
async def addSeller(request_seller: schemas.Seller, db: Session = Depends(getDB)):
    hash_password = pwd_context.hash(request_seller.password)
    seller = models.Seller(name=request_seller.name, username=request_seller.username, password=hash_password,
                           email=request_seller.email, phone=request_seller.phone, address=request_seller.address)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller
