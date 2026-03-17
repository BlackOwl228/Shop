import os

from fastapi import Depends

from src.core.logs.exceptions import TooManyRequestError
from src.core.resources.db import get_redis
from src.core.resources.redis import RedisClient, RedisKeys

REDIS_LIMIT_PER_MINUTE = os.getenv("REDIS_LIMIT_PER_MINUTE")


def rate_limit_redis(user_id: int, redis: RedisClient = Depends(get_redis)):
    key = RedisKeys.rate_limit_user(user_id=user_id)
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, 60)
    if current > REDIS_LIMIT_PER_MINUTE:
        raise TooManyRequestError()
