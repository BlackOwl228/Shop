import os
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from src.app.auth.schemas import LoginData
from src.core.logs.exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidRequestFormatError,
    SellerAlreadyExistsError,
    UserAlreadyExistsError,
)
from src.core.security import check_password, hash_password
from src.models.users import Seller, User


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        email_timedelta = int(os.getenv("VERIFICATION_EMAIL_TOKEN_HOURS"))
        self.verify_email_time = datetime.now(UTC) + timedelta(hours=email_timedelta)

    def user_by_email(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise InvalidEmailError()

        return user

    def verify_password(self, user: User, password: str):
        if not check_password(password, user.hashed_password):
            raise InvalidPasswordError()

    def check_if_passwords_match(self, password: str, new_password: str):
        if password == new_password:
            return True

    def change_password(self, user: User, new_password: str):
        user.hashed_password = hash_password(new_password)
        self.db.commit()

    def check_existing(self, email: str):
        exist_user = self.db.query(User).filter(User.email == email).first()
        if exist_user:
            raise UserAlreadyExistsError(email=email)

    def create_user(self, name: str, email: str, password: str):
        hashed_password = hash_password(password)
        user = User(name=name, email=email, hashed_password=hashed_password)

        self.db.add(user)
        self.db.flush()

        return user

    def check_login_data(self, login_data) -> tuple:
        try:
            login_data = LoginData.model_validate(
                {"username": login_data.username, "password": login_data.password}
            )
            email = login_data.username
            password = login_data.password
        except Exception as e:
            raise InvalidRequestFormatError() from e

        return email, password

    def check_old_seller_request(self, user: User):
        old_request = self.db.query(Seller).filter(Seller.user_id == user.id).first()
        if old_request:
            raise SellerAlreadyExistsError(user_id=user.id)

    def create_seller_request(self, user: User, company_name: str):
        request = Seller(user_id=user.id, company_name=company_name)
        self.db.add(request)
        self.db.commit()
