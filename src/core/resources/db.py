from collections.abc import Generator

from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.core.resources.redis import RedisClient
from src.core.settings import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


redis = Redis(host="redis", port=6379, decode_responses=True)
redis_client = RedisClient(redis)


def get_redis() -> RedisClient:
    return redis_client
