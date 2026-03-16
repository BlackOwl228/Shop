import json


class RedisClient:
    def __init__(self, redis):
        self.redis = redis

    def get_json(self, key):
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def set_json(self, key, value, ttl=600):
        self.redis.set(key, json.dumps(value), ex=ttl)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, ttl=600):
        self.redis.set(key, value, ex=ttl)

    def delete(self, key):
        self.redis.delete(key)


class RedisKeys:
    @staticmethod
    def product(product_id: int) -> str:
        return f"products:{product_id}"

    @staticmethod
    def refresh_token(token: str) -> str:
        return f"token:refresh:{token}"

    @staticmethod
    def email_token(token: str) -> str:
        return f"token:email:{token}"
