import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db import mapper_registery
from ..models import Inspector, ScopeDate

# from https://www.fullstackpython.com/sqlalchemy-orm-session-examples.html

test_db_url = "sqlite+pysqlite:///:memory:"


@pytest.fixture(scope="function")
def session_factory():
    engine = create_engine(test_db_url, echo=False, future=True)
    metadata = mapper_registery.metadata
    metadata.create_all(engine)
    yield sessionmaker(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def session(session_factory):
    return session_factory()


def test_bootstrap_inspector(session):
    i = Inspector(name="Clint")
    session.add(i)
    session.commit()
    assert session.query(Inspector.name).first()[0] == "Clint"


def test_can_add_scope_date_to_db(session):
    d = ScopeDate(2022, 1, 1)
    session.add(d)
    session.commit()
    assert session.query(ScopeDate.day).first()[0] == 1
