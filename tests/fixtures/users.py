import pytest

from src.models.users import Seller, User
from src.rules.seller_rules import SellerStatus


@pytest.fixture()
def buyer(db_session):
    user = User(
        name="Test_user",
        email="example@gmail.com",
        email_verified=True,
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$QaGnhV0t/MpNt/BYEOdHXg$VbWTD9QFxNS38hb5WezcHWF9ad+wqm3pNK0Z1gvCIKk",  # Test_password #noqa
        is_admin=False,
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture()
def seller(db_session):
    user = User(
        name="Test_seller",
        email="example2@gmail.com",
        email_verified=True,
        hashed_password="password",
        is_admin=False,
    )
    db_session.add(user)
    db_session.flush()
    seller = Seller(user_id=user.id, company_name="Test", status=SellerStatus.ACTIVE)
    db_session.add(seller)
    db_session.flush()
    return seller


@pytest.fixture()
def admin(db_session):
    admin = User(
        name="Test_admin",
        email="example3@gmail.com",
        email_verified=True,
        hashed_password="admin",
        is_admin=True,
    )
    db_session.add(admin)
    db_session.flush()
    return admin
