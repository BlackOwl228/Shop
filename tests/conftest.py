import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.db import Base, get_db
from main import app

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False},
                       poolclass=StaticPool)
Session = sessionmaker(bind=engine)

def reset_db(Base=Base):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

@pytest.fixture(scope="function")
def db_session():
    reset_db()
    session = Session()
    try:
        yield session
    finally:
        session.close()

from fastapi.testclient import TestClient
from core.security import get_current_seller, get_current_user, get_current_admin
from models.users import User, Seller
from rules.seller_rules import SellerStatus

@pytest.fixture(scope="function")
def client(db_session):
    def _get_db():
        yield db_session
    app.dependency_overrides[get_db] = _get_db

    yield TestClient(app)

@pytest.fixture
def buyer(db_session):
    user = User(name="Test_user",
                email="example@gmail.com",
                email_verified=True,
                hashed_password="$2b$12$jbYqnmH4Bl4.NnrM7QU7teUwQu.u9n/r6N061unUQPF4VVIFnSocq",
                is_admin=False)
    db_session.add(user)
    db_session.commit()

    def override_user():
        return user
    app.dependency_overrides[get_current_user] = override_user

    return user

@pytest.fixture
def seller(db_session):
    user = User(name="Test_seller",
                email="example2@gmail.com",
                email_verified=True,
                hashed_password="password",
                is_admin=False)
    seller = Seller(user_id=2,
                    company_name="Test",
                    status=SellerStatus.ACTIVE)
    db_session.add_all([user, seller])
    db_session.commit()
    def override_seller():
        return seller
    app.dependency_overrides[get_current_seller] = override_seller

    return seller

@pytest.fixture
def admin(db_session):
    admin = User(name="Test_admin",
                email="example3@gmail.com",
                email_verified=True,
                hashed_password="admin",
                is_admin=True)
    db_session.add(admin)
    db_session.commit()

    def override_admin():
        return admin
    app.dependency_overrides[get_current_admin] = override_admin

    return admin