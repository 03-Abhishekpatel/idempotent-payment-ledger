# tests/conftest.py

import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  testcontainers.community.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:18") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def db_url(postgres_container):
    return postgres_container.get_connection_url()


@pytest.fixture(scope="session")
def engine(db_url, run_migration):
    eng = create_engine(db_url)
    yield eng
    eng.dispose()


@pytest.fixture(scope="session")
def run_migration(db_url):
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_config, "head")


@pytest.fixture
def session(engine):
    """Each test gets a session bound to an outer transaction that is
    ALWAYS rolled back at teardown — guarantees isolation regardless
    of whether the code under test calls commit() or flush()."""
    connection = engine.connect()
    outer_transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    db_session = SessionLocal()

    yield db_session

    db_session.close()
    outer_transaction.rollback()   
    connection.close()