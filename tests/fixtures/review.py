import pytest

from src.models.reviews import Review


@pytest.fixture()
def review(db_session, buyer, product):
    review = Review(author_id=buyer.id, product_id=product.id, rating=5)
    db_session.add(review)
    db_session.flush()
    return review
