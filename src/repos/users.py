from sqlalchemy.orm import Session

from src.models.users import Seller, User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def flush(self):
        self.db.flush()

    def create(self, user: User):
        self.db.add(user)

    def create_seller(self, seller: Seller):
        self.db.add(seller)

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_seller_request(self, user_id: int):
        return self.db.query(Seller).filter(Seller.user_id == user_id).first()

    def get_seller(self, seller_id: int):
        return self.db.query(Seller).filter(Seller.id == seller_id).first()
