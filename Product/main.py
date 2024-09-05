from typing import List
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from fastapi import FastAPI, Response, HTTPException
from starlette import status
from . import schemas
from . import models
from .database import engine_n, SessionLocal
from passlib.context import CryptContext

app = FastAPI(
    title='Products API',
    description='API will provide to access all product info along with seller details. Developer can access this api '
                'to perform the below operations.',
    version='0.1.0',
    terms_of_service='https://github.com/sumantas98',
    contact={
        'Developer Name': 'Sumanta Samanta',
        'website': 'https://www.linkedin.com/in/sumanta-samanta-3261a317a/',
        'email': 'sumantasamanta98.gmail.com',
    },
    license_info={
        'name': 'License',
        'url': 'https://www.google.com',
    }

)
models.Base.metadata.create_all(bind=engine_n)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Please visit this page for all operations :: http://127.0.0.1:8000/docs"}


# Get All Product Details
@app.get("/allProducts", response_model=List[schemas.CustomDisplay], status_code=201)
async def products(db: Session = Depends(getDB)):
    product_ = db.query(models.Product).all()
    if not product_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_


# Get Product Details by ID Value
@app.get("/singleProductById", response_model=schemas.CustomDisplay)
async def products(product_id, response: Response, db: Session = Depends(getDB)):
    product_id = db.query(models.Product).filter_by(id=product_id).first()
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    return product_id


# Remove a specific Product by ID value
@app.delete("/deleteProduct")
async def products(db: Session = Depends(getDB), product_id: int = None):
    product_id = db.query(models.Product).filter_by(id=product_id).delete(synchronize_session=False)
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    db.commit()
    return "Product Deleted Successfully"


# Add New Product in DB Using Postman call/ FastAPI Docs.
@app.post('/addProduct')
async def addProduct(product: schemas.Product, db: Session = Depends(getDB)):
    new_product = models.Product(name=product.name, price=product.price, description=product.description,
                                 seller_id=product.seller_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Update a records based on ID value
@app.put('/updateProduct/{product_id}')
async def updateProduct(product_id: int, product: schemas.Product, db: Session = Depends(getDB)):
    product_id = db.query(models.Product).filter_by(id=product_id)
    if not product_id.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    else:
        product_id.update(product.dict())
        db.commit()
        return "Product Updated Successfully"


# Add New Seller in Seller DB
@app.post('/addSeller', response_model=schemas.DisplaySeller)
async def addSeller(request_seller: schemas.Seller, db: Session = Depends(getDB)):
    hash_password = pwd_context.hash(request_seller.password)
    seller = models.Seller(name=request_seller.name, username=request_seller.username, password=hash_password,
                           email=request_seller.email, phone=request_seller.phone, address=request_seller.address)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller
