import fakeredis
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from src.core.db import Base, get_redis
from src.core.redis import RedisClient
from src.main import app
from tests.fixtures import *

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/test")
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture()
def connection():
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture()
def db_session(connection):

    session = SessionLocal(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()


@pytest.fixture()
def fake_redis():
    redis = fakeredis.FakeRedis(decode_responses=True)
    redis_client = RedisClient(redis)

    def _get_redis():
        return redis_client

    app.dependency_overrides[get_redis] = _get_redis

    yield redis_client

    redis.flushall()
    app.dependency_overrides.clear()
