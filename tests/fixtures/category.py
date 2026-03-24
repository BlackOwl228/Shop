import pytest

from src.models.category import Category


@pytest.fixture()
def category(db_session):
    category = Category(name="Test_Category")
    db_session.add(category)
    db_session.flush()
    return category
