from fastapi import APIRouter, Response, HTTPException
from typing import List

from .login import get_current_user
from .. import schemas
from .. import models
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import getDB
from starlette import status

router = APIRouter(
    tags=['Products']
)


# Get All Product Details
@router.get("/allProducts", response_model=List[schemas.CustomDisplay], status_code=201)
async def products(db: Session = Depends(getDB), current_user: schemas.Seller = Depends(get_current_user)):
    product_ = db.query(models.Product).all()
    if not product_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_


# Get Product Details by ID Value
@router.get("/singleProductById", response_model=schemas.CustomDisplay)
async def products(product_id, response: Response, db: Session = Depends(getDB), current_user: schemas.Seller = Depends(get_current_user)):
    product_id = db.query(models.Product).filter_by(id=product_id).first()
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    return product_id


# Remove a specific Product by ID value
@router.delete("/deleteProduct")
async def products(db: Session = Depends(getDB), product_id: int = None, current_user: schemas.Seller = Depends(get_current_user)):
    product_id = db.query(models.Product).filter_by(id=product_id).delete(synchronize_session=False)
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    db.commit()
    return "Product Deleted Successfully"


# Add New Product in DB Using Postman call/ FastAPI Docs.
@router.post('/addProduct')
async def addProduct(product: schemas.Product, db: Session = Depends(getDB), current_user: schemas.Seller = Depends(get_current_user)):
    new_product = models.Product(name=product.name, price=product.price, description=product.description,
                                 seller_id=product.seller_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Update a records based on ID value
@router.put('/updateProduct/{product_id}')
async def updateProduct(product_id: int, product: schemas.Product, db: Session = Depends(getDB), current_user: schemas.Seller = Depends(get_current_user)):
    product_id = db.query(models.Product).filter_by(id=product_id)
    if not product_id.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    else:
        product_id.update(product.dict())
        db.commit()
        return "Product Updated Successfully"
