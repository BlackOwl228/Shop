from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile

from src.core.dependencies.services import get_auth_service, get_user_service
from src.core.dependencies.users import get_current_user
from src.models.users import User
from src.services.auth import AuthService
from src.services.media import save_image
from src.services.users import UserService

from ..auth.schemas import UserName, UserPassword
from .schemas import ProfilePesponse

router = APIRouter(prefix="/me", tags=["Profile"])


@router.get("", status_code=200, response_model=ProfilePesponse)
def get_profile(user: User = Depends(get_current_user)):
    return user


@router.patch("/name", status_code=200)
def change_name(
    new_name: UserName = Form(...),
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.change_name(user=user, new_name=new_name)

    return {"status": "Name was changed", "new_name": new_name}


@router.patch("/avatar", status_code=202)
async def change_avatar(
    background_tasks: BackgroundTasks,
    avatar: UploadFile = File(..., max_length=15 * 1024 * 1024, media_type=["image/png", "image/jpeg"]),
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    path = user_service.create_path_to_avatar(user=user, avatar=avatar)

    background_tasks.add_task(save_image, avatar, path)


@router.patch("/password", status_code=200)
def change_password(
    password: UserPassword = Form(...),
    new_password: UserPassword = Form(...),
    user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
):
    if auth_service.check_if_passwords_match(password=password, new_password=new_password):
        return {"status": "Passwords match"}

    auth_service.verify_password(user=user, password=password)

    hashed_password = auth_service.hash_password(password=password)

    user_service.change_password(user=user, hashed_password=hashed_password)

    return {"status": "Password was changed"}


@router.get("/orders", status_code=200)
def get_my_orders(user: User = Depends(get_current_user)):
    return user.orders


@router.post("/seller-request", status_code=201)
def create_seller_request(
    company_name: str = Form(..., max_length=128),
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.check_old_seller_request(user=user)

    user_service.create_seller_request(user=user, company_name=company_name)

    return {"status": "Request was created, wait for approve"}
