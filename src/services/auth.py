from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from src.app.auth.schemas import LoginData
from src.core.logs.exceptions import (
    InvalidPasswordError,
    InvalidRequestFormatError,
)
from src.core.security import check_password, hash_password
from src.core.settings import settings
from src.models.users import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        email_timedelta = settings.verification_email_token_hours
        self.verify_email_time = datetime.now(UTC) + timedelta(hours=email_timedelta)

    def hash_password(self, password: str):
        return hash_password(password=password)

    def verify_password(self, user: User, password: str):
        if not check_password(password, user.hashed_password):
            raise InvalidPasswordError()

    def check_if_passwords_match(self, password: str, new_password: str):
        if password == new_password:
            return True

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
