from app.auth.security import check_password, hash_password
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.app.auth.token.access import create_access_token
from src.app.auth.token.refresh import create_refresh_token
from src.core.resources.db import get_db
from src.models.tokens import RefreshToken
from src.models.users import User

from ..config import templates

router = APIRouter(tags=["FOR WEBSITE"])


@router.get("/front/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        "reg.html",
        {"request": request},
    )


@router.post("/front/register")
def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    exist_user = db.query(User).filter(User.email == email).first()
    if exist_user:
        raise HTTPException(status_code=409, detail="User already exists")

    hashed_password = hash_password(password)
    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()

    return RedirectResponse("/front/login", status_code=303)


@router.get("/front/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.post("/front/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not check_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user_id=user.id)
    refresh_token = create_refresh_token(user_id=user.id, db=db)

    response = RedirectResponse("/front/home", status_code=303)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        path="/",
    )

    return response


@router.post("/front/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401)

    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if refresh_token:
        raise HTTPException(status_code=401, detail="Wrong token, login again")

    new_access = create_access_token(refresh_token.user_id)

    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        samesite="lax",
    )

    return {"status": "refreshed"}
