import os

from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    NotYourReviewError,
    ProductNotFoundError,
    ReviewConflictError,
    ReviewNotFoundError,
)
from src.models.products import Product
from src.models.reviews import Review
from src.repos.products import ProductRepo
from src.repos.review import ReviewRepo


class ReviewService:
    def __init__(self, db: Session):
        self.repo = ReviewRepo(db)

    def _review_by_id_and_author_id(self, review_id: int, author_id: int):
        review = self.repo.get_with_product(review_id=review_id)
        if review.author_id != author_id:
            raise NotYourReviewError(review_id=review_id, user_id=author_id)
        if not review:
            raise ReviewNotFoundError(review_id=review_id)

        return review

    def _create_image_path(self, review: Review, image):
        img_path = os.path.join("media", "review", str(review.id))
        ext = image.filename.split(".")[-1]
        path = f"{img_path}.{ext}"
        review.image = path

    def _update_rating(self, product: Product, new_rating: int):
        total = product.rating * product.reviews_count
        total += new_rating

        product.reviews_count += 1
        product.rating = total / product.reviews_count

    def _patch_rating(self, product: Product, old_rating: int, new_rating: int):
        product.rating = (
            product.rating * product.reviews_count - old_rating + new_rating
        ) / product.reviews_count

    def _delete_rating(self, product: Product, review_rating: int):
        product.reviews_count -= 1
        if product.reviews_count == 0:
            product.rating = 0
        else:
            product.rating = (
                product.rating * (product.reviews_count + 1) - review_rating
            ) / product.reviews_count

    def create_review(self, author_id: int, product_id: int, rating: int, text: str | None, image):
        product = ProductRepo(self.repo.db).get_product(product_id=product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        ex_review = self.repo.get_by_author_and_product(author_id=author_id, product_id=product_id)
        if ex_review:
            raise ReviewConflictError(author_id=author_id)

        review = Review(product_id=product_id, author_id=author_id, rating=rating, text=text)
        self._update_rating(product, rating)
        self.repo.create(review)
        self.repo.flush()
        if image is not None:
            self._create_image_path(review=review, image=image)
        self.repo.commit()

        return review

    def get(self, review_id: int):
        review = self.repo.get(review_id=review_id)
        if not review:
            raise ReviewNotFoundError(review_id=review_id)
        return review

    def get_reviews_to_product(self, product_id: int, page: int, size: int):
        product = ProductRepo(self.repo.db).get_product(product_id=product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)

        reviews = self.repo.get_reviews_to_product(product_id=product_id, page=page, size=size)
        has_more = True if len(reviews) > size else False

        return reviews[:size], has_more

    def change_review(self, author_id: int, review_id: int, rating: int, text: str | None, image):
        review = self._review_by_id_and_author_id(review_id=review_id, author_id=author_id)

        if text is not None:
            review.text = text
        if image is not None:
            self._create_image_path(review=review, image=image)
        if rating != review.rating:
            self._patch_rating(product=review.product, old_rating=review.rating, new_rating=rating)
            review.rating = rating
        self.repo.commit()

        return review

    def delete_review(self, author_id: int, review_id: int):
        review = self._review_by_id_and_author_id(review_id=review_id, author_id=author_id)

        self._delete_rating(review.product, review.rating)
        self.repo.delete(review)
        self.repo.commit()

        return review.image
