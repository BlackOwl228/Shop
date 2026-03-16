import pytest

from src.models.products import Product, ProductVariant


@pytest.fixture()
def product(db_session, seller):
    product = Product(name="Test_product", seller_id=seller.id, reviews_count=1, status="active")
    db_session.add(product)
    db_session.flush()
    return product


@pytest.fixture()
def variant(db_session, product):
    variant = ProductVariant(product_id=product.id, name="Test_variant", price=10000, stock=10)
    db_session.add(variant)
    db_session.flush()
    return variant
