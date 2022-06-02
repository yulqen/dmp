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


# legacy...

# @pytest.fixture(scope="function")
# def session_factory():
#     engine = create_engine(test_db_url, echo=False, future=True)
#     metadata = mapper_registry.metadata
#     metadata.create_all(engine)
#     yield sessionmaker(engine)
#     engine.dispose()


# @pytest.fixture(scope="function")
# def session(session_factory):
#     return session_factory()
