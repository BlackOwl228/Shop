from fastapi import Depends
from sqlalchemy.orm import Session
from core.db import get_db
from fastapi.security import OAuth2PasswordBearer
from .tokens.access import decode_access_token
from models.users import User
from services.checking import check_user_exists

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth_scheme),
                     db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    
    user = db.query(User).filter(User.id == user_id).first()

    check_user_exists(user)

    return user

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)