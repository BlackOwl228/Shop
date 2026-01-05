'''
from core.db import SessionLocal
from faker import Faker

fake = Faker()

from models.users import User
from core.security import hash_password


def seed_users(count):
    db = SessionLocal()
    users = []

    for _ in range(count):
        password=fake.password(length=10, special_chars=False)
        users.append(
            User(
                email=fake.unique.email(),
                name=fake.name(),
                hash=hash_password(password)
            )
        )

    db.bulk_save_objects(users)
    db.commit()
    db.close()

import random

def seed_products(count):
    from models.products import Product
    db = SessionLocal()
    products = []

    for _ in range(count):
        products.append(
            Product(
                name=fake.word(),
                price=random.randint(100, 5000),
                seller_id=random.randint(1, 200), 
            )
        )

    db.bulk_save_objects(products)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_products(200)
    print("Users seeded")'''