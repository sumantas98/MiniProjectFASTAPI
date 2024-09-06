import os
from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from .. import schemas, database, models
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import getDB
from starlette import status
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 10
router = APIRouter(
    tags=['Login']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDB)):
    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect username or password or username '
                                                                          'not found')
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')

    # Gen JWT token
    access_token = generate_token(
        data={
            "sub": user.username
        })

    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect username')
        token_data = schemas.TokenData(username=username)

    except JWTError:
        raise credentials_exception
