from sqlalchemy.orm import Session, joinedload

from src.models.reviews import Review


class ReviewRepo:
    def __init__(self, db: Session):
        self.db = db

    def flush(self):
        self.db.flush()

    def commit(self):
        self.db.commit()

    def create(self, review: Review):
        self.db.add(review)

    def get(self, review_id: int):
        return self.db.query(Review).filter(Review.id == review_id).first()

    def get_with_product(self, review_id: int):
        return (
            self.db.query(Review).options(joinedload(Review.product)).filter(Review.id == review_id).first()
        )

    def get_by_author_and_product(self, author_id: int, product_id: int):
        return (
            self.db.query(Review)
            .filter(Review.author_id == author_id, Review.product_id == product_id)
            .first()
        )

    def get_reviews_to_product(self, product_id: int, page: int, size: int):
        return (
            self.db.query(Review)
            .options(joinedload(Review.author))
            .filter(Review.product_id == product_id)
            .order_by(Review.created_at.desc())
            .limit(size + 1)
            .offset((page - 1) * size)
            .all()
        )

    def delete(self, review: Review):
        self.db.delete(review)
