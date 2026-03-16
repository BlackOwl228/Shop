import os

from sqlalchemy.orm import Session

from src.models.users import User


class UserService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def change_name(self, new_name: str):
        self.user.name = new_name
        self.db.commit()

    def create_path_to_avatar(self, avatar):
        img_path = os.path.join("media", "avatar", str(self.user.id))
        ext = avatar.filename.split(".")[-1]
        path = f"{img_path}.{ext}"
        self.user.avatar = path
        self.db.commit()

        return path
