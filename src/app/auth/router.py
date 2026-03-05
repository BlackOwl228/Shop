from fastapi import APIRouter,BackgroundTasks, Form, Depends, Path
from fastapi.security import OAuth2PasswordRequestForm

from integrations.gmail import send_message
from services.auth import AuthService
from services.tokens import TokenService
from services.email import EmailService
from core.depends import get_auth_service, get_token_service, get_email_service
from .schemas import UserEmail, UserName, UserPassword, LoginResponse, RefreshResponse

router = APIRouter(tags=["Auth"])

@router.post('/reg', status_code=202)
def registration(backgrond_tasks: BackgroundTasks,
                 name: UserName = Form(...),
                 email: UserEmail = Form(...),
                 password: UserPassword = Form(...),
                 auth_service: AuthService = Depends(get_auth_service),
                 token_service: TokenService = Depends(get_token_service)
                 ):
    auth_service.check_existing(email)
    
    user = auth_service.create_user(name=name, email=email, password=password)

    token = token_service.create_email_token(user.id)

    #backgrond_tasks.add_task(send_message, user.email, token.id)

    return {"status": "created", "message": "Verify your email by magic link"}

@router.post('/login', status_code=201, response_model=LoginResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               auth_service: AuthService = Depends(get_auth_service),
               token_service: TokenService = Depends(get_token_service)
               ):
    email, password = auth_service.check_login_data(form_data)

    user = auth_service.user_by_email(email)

    auth_service.verify_password(password, user.hashed_password)

    return {"access_token": token_service.create_access_token(user.id),
            "refresh_token": token_service.create_refresh_token(user.id),
            "token_type": "bearer"}

@router.delete('/logout', status_code=204)
def logout_user(token: str = Form(...),
                token_service: TokenService = Depends(get_token_service)
                ):
    token_service.delete_refresh_token(token)

@router.post('/verify/{token}', status_code=204)
def verify_email(token: str = Path(...),
                 email_service: EmailService = Depends(get_email_service)
                 ):
    email_service.verify_email_by_token(token)

@router.post('/refresh', status_code=201, response_model=RefreshResponse)
def refresh_token(token: str = Form(...),
                  token_service: TokenService = Depends(get_token_service)):
    user_id = token_service.check_refresh_token(token)
    
    return {"access_token": token_service.create_access_token(user_id),
            "token_type": "bearer"}