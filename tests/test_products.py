'''
import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.db import Base, get_db
from main import app

engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def db_session():
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
app.dependency_overrides[get_db] = db_session

from core.security import get_current_seller, get_current_user
from models.users import User, Seller

def override_get_current_seller():
    return Seller(id=1, company_name="test_seller", status="active")
def override_get_current_user():
    return User(id=2, name="test_user", is_admin=False)

app.dependency_overrides[get_current_seller] = override_get_current_seller
app.dependency_overrides[get_current_user] = override_get_current_user

from starlette.testclient import TestClient

client = TestClient(app)

#products
def test_create_product(client):
    response = client.post("/products", data={"name": "Test_product"})
    assert response.status_code == 201

def test_create_variant(client):
    response = client.post("/products/1/variants", data={"name": "Test_variant", "price": 10000})
    assert response.status_code == 201

def test_get_product(client):
    response = client.get("/products/1")
    assert response.status_code == 200

def test_change_product(client, seller):
    response = client.patch("/products/1", data={"name": "Test_product_v2"})
    assert response.status_code == 204

def test_change_variant(client, seller):
    response = client.patch("/products/1/variants/1", data={"name": "Test_variant_v2", "price": 15000})
    assert response.status_code == 204

def test_delete_variant(client, seller):
    response = client.delete("/products/1/variants/1")
    assert response.status_code == 204

#search
def test_search(client):
    response = client.get("/search?min_price=0")
    assert response.status_code == 200

#orders
def test_cancel_order(client):
    response = client.patch("/orders/1/cancel")
    assert response.status_code == 204

def test_complete_order(client):
    response = client.patch("/orders/1/complete")
    assert response.status_code == 204
'''

def test_login_success(client, buyer):
    response = client.post(
        "/login",
        data={
            "username": "example@gmail.com",
            "password": "password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 201