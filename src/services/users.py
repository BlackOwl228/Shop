import os

from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    InvalidEmailError,
    SellerAlreadyExistsError,
    SellerNotFoundError,
    UserAlreadyExistsError,
)
from src.models.users import Seller, User
from src.repos.users import UserRepo


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepo(db)

    def user_by_email(self, email: str):
        user = self.repo.get_by_email(email=email)
        if not user:
            raise InvalidEmailError()

        return user

    def check_existing(self, email: str):
        exist_user = self.repo.get_by_email(email=email)
        if exist_user:
            raise UserAlreadyExistsError(email=email)

    def create_user(self, name: str, email: str, hashed_password: str):
        user = User(name=name, email=email, hashed_password=hashed_password)

        self.repo.create(user)
        self.repo.flush()

        return user

    def change_name(self, user: User, new_name: str):
        user.name = new_name
        self.repo.commit()

    def change_password(self, user: User, hashed_password: str):
        user.hashed_password = hashed_password
        self.repo.commit()

    def create_path_to_avatar(self, user: User, avatar):
        img_path = os.path.join("media", "avatar", str(user.id))
        ext = avatar.filename.split(".")[-1]
        path = f"{img_path}.{ext}"
        user.avatar = path
        self.repo.commit()

        return path

    def check_old_seller_request(self, user: User):
        old_request = self.repo.get_seller_request(user_id=user.id)
        if old_request:
            raise SellerAlreadyExistsError(user_id=user.id)

    def create_seller_request(self, user: User, company_name: str):
        request = Seller(user_id=user.id, company_name=company_name)
        self.repo.create_seller(request)
        self.repo.commit()

    def get_seller(self, seller_id: int):
        seller = self.repo.get_seller(seller_id=seller_id)
        if not seller:
            raise SellerNotFoundError(seller_id=seller_id)

        return seller
