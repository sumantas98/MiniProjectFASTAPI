from typing import List
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from fastapi import FastAPI, Response, HTTPException
from starlette import status
from . import schemas
from . import models
from .database import engine_n, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine_n)


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Get All Product Details
@app.get("/products", response_model=List[schemas.Product], status_code=201)
async def products(db: Session = Depends(getDB)):
    product_ = db.query(models.Product).all()
    return product_


# Get Product Details by ID Value
@app.get("/product_id", response_model=schemas.CustomDisplay)
async def products(product_id, response: Response, db: Session = Depends(getDB)):
    product_id = db.query(models.Product).filter_by(id=product_id).first()
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product not found')
    return product_id


# Remove a specific Product by ID value
@app.delete("/product_delete")
async def products(db: Session = Depends(getDB), product_id: int = None):
    product_id = db.query(models.Product).filter_by(id=product_id).delete(synchronize_session=False)
    db.commit()
    return "Product deleted"


# Add New Product in DB Using Postman call/ FastAPI Docs.
@app.post('/addProduct')
async def addProduct(product: schemas.Product, db: Session = Depends(getDB)):
    new_product = models.Product(name=product.name, price=product.price, description=product.description)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Update a records based on ID value
@app.put('/updateProduct/{product_id}')
async def updateProduct(product_id: int, product: schemas.Product, db: Session = Depends(getDB)):
    product_id = db.query(models.Product).filter_by(id=product_id)
    if not product_id.first():
        pass
    else:
        product_id.update(product.dict())
        db.commit()
        return "Product updated"
