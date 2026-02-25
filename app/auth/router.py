from datetime import datetime, timedelta, timezone
import os, uuid

from fastapi import APIRouter, HTTPException,BackgroundTasks, Form, Depends, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import ValidationError

from core import get_db, hash_password, verify_password, create_access_token, create_refresh_token, delete_refresh_token, send_message
from models import User, RefreshToken, EmailToken
from .schemas import UserEmail, UserName, UserPassword, LoginData, LoginResponse, RefreshResponse

router = APIRouter(tags=["Auth"])

email_timedelta = int(os.getenv("VERIFICATION_EMAIL_TOKEN_HOURS"))
verify_email_time = datetime.now(timezone.utc) + timedelta(hours=email_timedelta)

@router.post('/reg', status_code=202)
def registration(backgrond_tasks: BackgroundTasks,
                 name: UserName = Form(...),
                 email: UserEmail = Form(...),
                 password: UserPassword = Form(...),
                 db: Session = Depends(get_db)
                 ):
    
    exist_user = db.query(User).filter(User.email == email).first()
    if exist_user:
        raise HTTPException(status_code=409, detail="User already exists")
    
    hashed_password = hash_password(password)
    user = User(name=name, email=email, hashed_password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    user_uuid = uuid.uuid4().hex
    expires_at = verify_email_time
    token = EmailToken(id=user_uuid, user_id=user.id, expires_at=expires_at)

    db.add(token)
    db.commit()

    #backgrond_tasks.add_task(send_message, user.email, token.id)

    return {"status": "created", "message": "Verify your email by magic link"}

@router.post('/login', status_code=201, response_model=LoginResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(get_db)
               ):
    try:
        login_data = LoginData.model_validate({"username": form_data.username,
                                               "password": form_data.password})
        email = login_data.username
        password = login_data.password
    except ValidationError:
        raise HTTPException(status_code=422, detail="Incorrect data, try again")

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong data, try again")
    
    return {"access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id, db),
            "token_type": "bearer"}

@router.delete('/logout', status_code=204)
def logout_user(token: str = Form(...),
                db: Session = Depends(get_db)
                ):
    delete_refresh_token(token, db)

@router.post('/verify/{token_id}', status_code=204)
def verify_email(token_id: str = Path(..., ge=1),
                 db: Session = Depends(get_db)):
    
    token = db.query(EmailToken).filter(EmailToken.id == token_id,
                                        EmailToken.expires_at >= datetime.now(timezone.utc)).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    user = db.query(User).filter(User.id == token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email_verified = True

    db.delete(token)
    db.commit()

@router.post('/refresh', status_code=201, response_model=RefreshResponse)
def refresh_token(token: str = Form(...),
                  db: Session = Depends(get_db)):
    
    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Wrong token, login again")
    
    return {"access_token": create_access_token(refresh_token.user_id)}