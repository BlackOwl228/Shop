from fastapi import Depends

from src.core.logs.exceptions import TooManyRequestError
from src.core.resources.db import get_redis
from src.core.resources.redis import RedisClient, RedisKeys
from src.core.settings import settings

RATE_LIMIT_PER_MINUTE = settings.rate_limit_per_minute


def rate_limit_redis(user_id: int, redis: RedisClient = Depends(get_redis)):
    key = RedisKeys.rate_limit_user(user_id=user_id)
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, 60)
    if current > RATE_LIMIT_PER_MINUTE:
        raise TooManyRequestError()
