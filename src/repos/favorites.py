from sqlalchemy.orm import Session, joinedload

from src.models.favorites import Favorite


class FavoritesRepo:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def get(self, user_id, product_id):
        return (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.product_id == product_id)
            .first()
        )

    def create(self, item: Favorite):
        self.db.add(item)

    def get_all(self, user_id: int):
        return (
            self.db.query(Favorite)
            .options(joinedload(Favorite.product))
            .filter(Favorite.user_id == user_id)
            .all()
        )

    def delete(self, item: Favorite):
        self.db.delete(item)
