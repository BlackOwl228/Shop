import pytest

from src.models.orders import Order


@pytest.fixture()
def order(db_session, buyer):
    order = Order(buyer_id=buyer.id, total_price=1000, payment_intent="1wq2defrtg6y7ui")
    db_session.add(order)
    db_session.flush()
    return order
