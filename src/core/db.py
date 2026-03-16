import os
from collections.abc import Generator

from dotenv import load_dotenv
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.core.redis import RedisClient

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
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
