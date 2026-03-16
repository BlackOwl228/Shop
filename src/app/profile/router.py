from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile

from src.app.auth.security import get_current_user
from src.core.depends import get_auth_service, get_user_service
from src.core.media import save_image
from src.models.users import User
from src.services.auth import AuthService
from src.services.users import UserService

from ..auth.schemas import UserName, UserPassword
from .schemas import ProfilePesponse

router = APIRouter(prefix="/me", tags=["Profile"])


@router.get("", status_code=200, response_model=ProfilePesponse)
def get_profile(user: User = Depends(get_current_user)):
    return user


@router.patch("/name", status_code=200)
def change_name(new_name: UserName = Form(...), user_service: UserService = Depends(get_user_service)):
    user_service.change_name(new_name)

    return {"status": "Name was changed", "new_name": new_name}


@router.patch("/avatar", status_code=202)
async def change_avatar(
    background_tasks: BackgroundTasks,
    avatar: UploadFile = File(..., max_length=15 * 1024 * 1024, media_type=["image/png", "image/jpeg"]),
    user_service: UserService = Depends(get_user_service),
):
    path = user_service.create_path_to_avatar(avatar)

    background_tasks.add_task(save_image, avatar, path)


@router.patch("/password", status_code=200)
def change_password(
    password: UserPassword = Form(...),
    new_password: UserPassword = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
    user: User = Depends(get_current_user),
):
    auth_service.check_if_passwords_match(password=password, new_password=new_password)

    auth_service.verify_password(user=user, password=password)

    auth_service.change_password(user=user, new_password=new_password)

    return {"status": "Password was changed"}


@router.get("/orders", status_code=200)
def get_my_orders(user: User = Depends(get_current_user)):
    return user.orders


@router.post("/seller-request", status_code=201)
def create_seller_request(
    company_name: str = Form(..., max_length=128),
    auth_service: AuthService = Depends(get_auth_service),
    user: User = Depends(get_current_user),
):
    auth_service.check_old_seller_request(user)

    auth_service.create_seller_request(user=user, company_name=company_name)

    return {"status": "Request was created, wait for approve"}
