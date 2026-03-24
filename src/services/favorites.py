from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    ProductAlreadyInFavoritesError,
    ProductNotInFavoritesError,
)
from src.models.favorites import Favorite
from src.repos.favorites import FavoritesRepo


class FavoritesService:
    def __init__(self, db: Session):
        self.repo = FavoritesRepo(db)

    def add_to_favorites(self, user_id: int, product_id: int):
        old_item = self.repo.get(user_id=user_id, product_id=product_id)
        if old_item:
            raise ProductAlreadyInFavoritesError()

        item = Favorite(user_id=user_id, product_id=product_id)
        self.repo.create(item)
        self.repo.commit()

    def get_favorites(self, user_id: int):
        return self.repo.get_all(user_id=user_id)

    def delete_from_favorites(self, user_id: int, product_id: int):
        item = self.repo.get(user_id=user_id, product_id=product_id)
        if not item:
            raise ProductNotInFavoritesError()

        self.repo.delete(item)
        self.repo.commit()
