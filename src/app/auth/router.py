from fastapi import APIRouter, BackgroundTasks, Depends, Form, Path
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies.services import get_auth_service, get_token_service, get_user_service
from src.integrations.gmail import send_message  # noqa: F401
from src.services.auth import AuthService
from src.services.tokens import TokenService
from src.services.users import UserService

from .schemas import LoginResponse, RefreshResponse, UserEmail, UserName, UserPassword

router = APIRouter(tags=["Auth"])


@router.post("/reg", status_code=202)
def registration(
    backgrond_tasks: BackgroundTasks,
    name: UserName = Form(...),
    email: UserEmail = Form(...),
    password: UserPassword = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
):
    user_service.check_existing(email=email)

    hashed_password = auth_service.hash_password(password=password)

    user = user_service.create_user(name=name, email=email, hashed_password=hashed_password)

    token = token_service.create_email_token(user.id)  # noqa: F841

    # backgrond_tasks.add_task(send_message, user.email, token)

    return {"status": "created", "message": "Verify your email by magic link"}


@router.post("/login", status_code=201, response_model=LoginResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
):
    email, password = auth_service.check_login_data(form_data)

    user = user_service.user_by_email(email)

    auth_service.verify_password(password=password, user=user)

    return {
        "access_token": token_service.create_access_token(user.id),
        "refresh_token": token_service.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/logout", status_code=204)
def logout_user(token: str = Form(...), token_service: TokenService = Depends(get_token_service)):
    token_service.delete_refresh_token(refresh_token=token)


@router.post("/verify/{token}", status_code=204)
def verify_email(token: str = Path(...), token_service: TokenService = Depends(get_token_service)):
    token_service.verify_email_by_token(email_token=token)


@router.post("/refresh", status_code=200, response_model=RefreshResponse)
def refresh_token(token: str = Form(...), token_service: TokenService = Depends(get_token_service)):
    user_id = token_service.check_refresh_token(refresh_token=token)

    return {"access_token": token_service.create_access_token(user_id), "token_type": "bearer"}
