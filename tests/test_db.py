import pytest
from dmp.domain.models import Calendar, Inspector, ModelException, ScopeDate

# from https://www.fullstackpython.com/sqlalchemy-orm-session-examples.html

pytestmark = pytest.mark.usefixtures("mappers")


def test_bootstrap_inspector(sqlite_session_factory):
    session = sqlite_session_factory()
    i = Inspector(name="Clint")
    session.add(i)
    session.commit()
    assert session.query(Inspector.name).first()[0] == "Clint"


def test_can_add_scope_date_to_db(sqlite_session_factory):
    session = sqlite_session_factory()
    d = ScopeDate(2022, 1, 1)
    session.add(d)
    session.commit()
    assert session.query(ScopeDate.day).first()[0] == 1


def test_can_add_calendar_to_db(sqlite_session_factory):
    session = sqlite_session_factory()
    c = Calendar(2022)
    assert c.scope_dates == []
    # let's add some dates to this calendar
    c.calendar_creator()
    session.add(c)
    session.commit()
    res = session.query(Calendar).first()
    assert ScopeDate(2022, 1, 8) not in res.scope_dates


def test_cannot_create_dates_twice_for_calendar(sqlite_session_factory):
    session = sqlite_session_factory()
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


def test_can_delete_calendar(sqlite_session_factory):
    session = sqlite_session_factory()
    c = Calendar(2002)
    # c.scope_dates = _calendar_creator(c)
    session.add(c)
    session.commit()
    res = session.query(Calendar).first()
    session.delete(res)
    assert len(session.query(Calendar).all()) == 0
    assert len(session.query(ScopeDate).all()) == 0


# Repository tests
def test_calendar_repository_add(sqlite_session_factory):
    session = sqlite_session_factory()
    assert False
