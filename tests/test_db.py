import pytest
from dmp.db import mapper_registry
from dmp.models import Calendar, Inspector, ModelException, ScopeDate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from https://www.fullstackpython.com/sqlalchemy-orm-session-examples.html

test_db_url = "sqlite+pysqlite:///:memory:"


@pytest.fixture(scope="function")
def session_factory():
    engine = create_engine(test_db_url, echo=False, future=True)
    metadata = mapper_registry.metadata
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


def test_can_add_calendar_to_db(session):
    c = Calendar(2022)
    assert c.scope_dates == []
    # let's add some dates to this calendar
    c.calendar_creator()
    session.add(c)
    session.commit()
    res = session.query(Calendar).first()
    assert ScopeDate(2022, 1, 8) not in res.scope_dates


def test_cannot_create_dates_twice_for_calendar(session):
    c = Calendar(2022)
    assert c.scope_dates == []
    # let's add some dates to this calendar
    c.calendar_creator()
    session.add(c)
    session.commit()
    res = session.query(Calendar).first()
    assert len(res.scope_dates) == 260
    # ensure we cannot create dates again
    with pytest.raises(ModelException):
        c.calendar_creator()


def test_can_delete_calendar(session):
    c = Calendar(2002)
    # c.scope_dates = _calendar_creator(c)
    session.add(c)
    session.commit()
    res = session.query(Calendar).first()
    session.delete(res)
    assert len(session.query(Calendar).all()) == 0
    assert len(session.query(ScopeDate).all()) == 0
