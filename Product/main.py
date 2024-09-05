from fastapi import FastAPI, Response, HTTPException
from . import models
from .database import engine_n, SessionLocal
from .routers import product
from .routers import seller

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


@app.get("/", tags=['Index'])
async def root():
    return {"message": "Please visit this page for all operations :: http://127.0.0.1:8000/docs"}

app.include_router(product.router)
app.include_router(seller.router)

models.Base.metadata.create_all(bind=engine_n)
