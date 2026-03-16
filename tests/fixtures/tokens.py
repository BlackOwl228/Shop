import pytest

from src.core.redis import RedisKeys


@pytest.fixture
def refresh_token(buyer, fake_redis):
    token = "test_refresh_token"
    key = RedisKeys.refresh_token(token)
    fake_redis.set(key, buyer.id, ttl=3600)

    return token


@pytest.fixture
def email_token(buyer, fake_redis):
    token = "email_test_token"
    key = RedisKeys.email_token(token)
    fake_redis.set(key, buyer.id, ttl=3600)

    return token
