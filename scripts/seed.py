import secrets
import uuid
from random import randint

from faker import Faker

from src.core.resources.db import SessionLocal
from src.models.products import Product, ProductVariant
from src.models.users import Seller, User

fake = Faker("ru_RU")


def seed_users(count, batch_size=1000):
    db = SessionLocal()

    try:
        for i in range(0, count, batch_size):
            batch = []

            for _ in range(min(batch_size, count - i)):
                batch.append(
                    User(
                        name=f"{fake.name()} {randint(1, 100)}",
                        email="fake" + secrets.token_hex(10) + "@gmail.com",
                        hashed_password=f"{uuid.uuid4()}",
                    )
                )
            db.bulk_save_objects(batch)

        db.commit()

        for i in range(0, count, batch_size):
            batch = []

            for j in range(min(batch_size, count - i)):
                batch.append(
                    Seller(
                        user_id=i + j + 1,
                        company_name=f"{fake.color_name()} {fake.word().capitalize()} {randint(1, 100)}",  # noqa: E501
                    )
                )
            db.bulk_save_objects(batch)

        db.commit()
    finally:
        db.close()


def seed_products(count, batch_size=5000):
    db = SessionLocal()

    try:
        for i in range(0, count, batch_size):
            batch = []

            for _ in range(min(batch_size, count - i)):
                batch.append(
                    Product(
                        name=f"{fake.word().capitalize()}",
                        seller_id=randint(1, 1000),
                    )
                )
            db.bulk_save_objects(batch)

        db.commit()
    finally:
        db.close()


def seed_variants(count, batch_size=5000):
    db = SessionLocal()

    try:
        for i in range(0, count, batch_size):
            batch = []

            for _ in range(min(batch_size, count - i)):
                batch.append(
                    ProductVariant(
                        name=f"{fake.word().capitalize()} {randint(1, 100)}",
                        price=randint(50, 20000),
                        product_id=randint(1, 10000),
                    )
                )
            db.bulk_save_objects(batch)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_users(1000)
    seed_products(10000)
    seed_variants(100000)
