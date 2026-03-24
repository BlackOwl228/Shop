from sqlalchemy.orm import Session

from src.models.category import Category


class CategoryRepo:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def get(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_all(self):
        return self.db.query(Category).all()
