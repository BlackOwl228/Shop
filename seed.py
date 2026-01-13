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

'''
import requests, os
from random import randint
from core.db import SessionLocal
from models import Product
from core import save_product_image

def seed_products():
    db = SessionLocal()
    data = requests.get("https://fakestoreapi.com/products").json()
    try:
        for item in data:
            product = Product(
                name=item["title"],
                price=int(item["price"]),
                description=item["description"],
                rating=item["rating"]["rate"],
                seller_id=randint(1, 100)
            )
            db.add(product)
            db.flush()
            url = item["image"]
            ext = url.split('.')[-1].split("?")[0]
            folder = os.path.join("media", "product")
            os.makedirs(folder, exist_ok=True)
            filename = f"{product.id}.{ext}"
            full_path = os.path.join(folder, filename)

            r = requests.get(url)
            with open(full_path, "wb") as f:
                f.write(r.content)

            product.image = filename

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
'''