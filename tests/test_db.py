import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..db import mapper_registery
from ..models import Inspector

test_db_url = "sqlite+pysqlite:///:memory:"


@pytest.fixture(scope="function")
def session_factory():
    engine = create_engine(test_db_url, echo=True, future=True)
    metadata = mapper_registery.metadata
    metadata.create_all(engine)
    yield sessionmaker(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def session(session_factory):
    return session_factory()


def test_bootstrap_calendar(session):
    i = Inspector(name="Clint")
    session.add(i)
    session.commit()
    assert session.query(Inspector.name).first()[0] == "Clint"
