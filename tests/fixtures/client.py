import pytest
from fastapi.testclient import TestClient

from src.app.auth.security import get_current_admin, get_current_seller, get_current_user
from src.core.db import get_db
from src.main import app


@pytest.fixture()
def client(db_session, buyer, seller, admin):
    def _get_db():
        yield db_session

    def override_get_current_user():
        return buyer

    def override_get_current_seller():
        return seller

    def override_get_current_admin():
        return admin

    app.dependency_overrides[get_db] = _get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_current_seller] = override_get_current_seller
    app.dependency_overrides[get_current_admin] = override_get_current_admin

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
