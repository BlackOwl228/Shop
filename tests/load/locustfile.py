from random import randint

from faker import Faker
from locust import HttpUser, constant, task

"""
class ReadUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_endpoint(self):
        self.client.get("/products/1")
"""
"""
class WriteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post("/login", data={
            "username": "blackowl228@gmail.com",
            "password": "Owl228"
        })
        self.token = response.json()["access_token"]

    @task
    def create_order(self):
        self.client.post(
            "/orders",
            headers={"Authorization": f"Bearer {self.token}"},
            json=[{"variant_id": 1, "quantity": 1, "client_price": 1488.0}]
        )
"""


class CartUser(HttpUser):
    wait_time = constant(0)

    def on_start(self):
        self.products = {
            1: "Видеокарта",
            2: "Телефон",
            3: "Часы",
            4: "Холодильник",
            5: "Ноутбук",
            6: "Роутер",
            7: "Мышка",
            8: "Клавиатура",
            9: "Монитор",
            10: "Зеркало",
            11: "Вешалка",
            12: "Стул",
            13: "Стол",
            14: "Диван",
            15: "Пылесос",
            16: "Утюг",
            17: "Фен",
            18: "Бритва",
            19: "Консоль",
            20: "Телевизор",
        }
        self.fake = Faker("ru_RU")

        response = self.client.post(
            "/login", data={"username": "blackowl228@gmail.com", "password": "Owl228"}
        )
        self.token = response.json()["access_token"]

    @task
    def add_variant(self):
        product_id = randint(1, 20)
        self.client.post(
            f"/products/{product_id}/variants",
            headers={"Authorization": f"Bearer {self.token}"},
            data={
                "name": f"{self.fake.color_name().capitalize()} {self.products.get(product_id)} {randint(1, 100)}",  # noqa: E501
                "price": randint(100, 10000),
                "stock": randint(10000, 100000),
            },
        )


class SearchUser(HttpUser):
    wait_time = constant(0)

    @task
    def search_test(self):
        self.client.post("/search", data={"q": "лав"})
