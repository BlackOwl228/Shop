import os

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.products import Product
from models.reviews import Review
from models.users import User


class ReviewService:
    def __init__(self, db: Session, author: User):
        self.db = db
        self.author = author

    def _review_by_id_and_author_id(self, review_id: int):
        review = (
            self.db.query(Review)
            .options(joinedload(Review.product))
            .filter(Review.id == review_id, Review.author_id == self.author.id)
            .first()
        )
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        return review

    def _create_image_path(review: Review, image):
        img_path = os.path.join("media", "review", str(review.id))
        ext = image.filename.split(".")[-1]
        path = f"{img_path}.{ext}"
        review.image = path

        return path

    def _update_rating(product: Product, new_rating: int):
        total = product.rating * product.reviews_count
        total += new_rating

        product.reviews_count += 1
        product.rating = total / product.reviews_count

    def _patch_rating(product: Product, old_rating: int, new_rating: int):
        product.rating = (
            product.rating * product.reviews_count - old_rating + new_rating
        ) / product.reviews_count

    def _delete_rating(product: Product, review_rating: int):
        product.reviews_count -= 1
        if product.reviews_count == 0:
            product.rating = 0
        else:
            product.rating = (
                product.rating * (product.reviews_count + 1) - review_rating
            ) / product.reviews_count

    def create_review(self, product_id: int, rating: int, text: str | None, image):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        ex_review = (
            self.db.query(Review)
            .filter(Review.author_id == self.author.id, Review.product_id == product_id)
            .first()
        )
        if ex_review:
            raise HTTPException(status_code=400, detail="You cannot create more than 1 review")

        review = Review(product_id=product_id, author_id=self.author.id, rating=rating, text=text)
        self._update_rating(product, rating)
        self.db.add(review)
        self.db.flush()
        if image is not None:
            image_path = self._create_image_path(review=review, image=image)
        self.db.commit()

        return review, image_path

    def change_review(self, review_id: int, rating: int, text: str | None, image):
        review = self._review_by_id_and_author_id(review_id)

        if text is not None:
            review.text = text
        if image is not None:
            image_path = self._create_image_path(review=review, image=image)
        if rating != review.rating:
            self._patch_rating(product=review.product, old_rating=review.rating, new_rating=rating)
            review.rating = rating
        self.db.commit()

        return image_path

    def delete_review(self, review_id: int):
        review = self._review_by_id_and_author_id(review_id)

        self._delete_rating(review.product, review.rating)
        self.db.delete(review)
        self.db.commit()

        return review.image
