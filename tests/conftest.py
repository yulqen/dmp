import pytest
from dmp.adaptors.orm import metadata, start_mappers
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:", echo=False, future=True
    )  # noqa
    metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()
