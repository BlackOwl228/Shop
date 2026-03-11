import json
import os
from collections.abc import Generator

from dotenv import load_dotenv
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

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


def cache_get(key: str):
    data = redis.get(key)
    if data:
        return json.loads(data)
    return None


def cache_set(key: str, value: dict, ttl: int = 600):
    redis.set(key, json.dumps(value), ex=ttl)


def redis_get(key: str):
    data = redis.get(key)
    return data


def redis_set(key: str, value: str, ttl: int = 600):
    redis.set(key, value, ex=ttl)


def redis_delete(key: str):
    redis.delete(key)
