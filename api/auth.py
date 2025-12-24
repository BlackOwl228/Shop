from fastapi import APIRouter, HTTPException, Form, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import hash_password , verify_password
from models.users import User
from models.tokens import RefreshToken
from core.tokens.access import create_access_token
from core.tokens.refresh import delete_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/reg')
def registration(name: str = Form(...),
                 email: str = Form(...),
                 password: str = Form(...),
                 db: Session = Depends(get_db)
                 ):
    exist_user = db.query(User).filter(User.email == email).first()
    if exist_user:
        raise HTTPException(status_code=409, detail="User is already exists")
    
    hashed_password = hash_password(password)
    new_user = User(name = name, email = email, hash = hashed_password)
    db.add(new_user)
    db.commit()

@router.post('/login')
def login_user(email: str = Form(...),
               password: str = Form(...),
               db: Session = Depends(get_db)
               ):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hash):
        raise HTTPException(status_code=401, detail="Wrong data, try again")
    
    return create_access_token(user.id)

@router.post('/refresh')
def refresh_token(token: str = Form(...),
                  db: Session = Depends(get_db)):
    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if refresh_token:
        raise HTTPException(status_code=401, detail="Wrong token, login again")
    
    return create_access_token(refresh_token.user_id)

@router.delete('/logout')
def logout_user(token: str = Form(...),
                db: Session = Depends(get_db)
                ):
    delete_refresh_token(token)
    return 204