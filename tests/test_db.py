import pytest
from dmp.adaptors.repository import CalendarRepository, InspectorRepository
from dmp.domain.models import (
    Calendar,
    Inspector,
    ModelException,
    RegulatoryCycle,
    ScopeDate,
)

# from https://www.fullstackpython.com/sqlalchemy-orm-session-examples.html

# ensure that the 'mappers' fixture from conftest runs for each test
pytestmark = pytest.mark.usefixtures("mappers")


def test_regulatory_cycle(sqlite_session_factory):
    session = sqlite_session_factory()
    rc = RegulatoryCycle(2020)
    session.add(rc)
    session.commit()
    res = session.query(RegulatoryCycle).first()
    assert ScopeDate(2020, 1, 17) in res.calendar.scope_dates
    assert ScopeDate(2020, 1, 18) not in res.calendar.scope_dates


def test_bootstrap_inspector(sqlite_session_factory):
    session = sqlite_session_factory()
    i = Inspector(name="Clint")
    session.add(i)
    session.commit()
    assert session.query(Inspector.name).first()[0] == "Clint"


def test_inspector_has_a_calendar(sqlite_session_factory):
    i = Inspector("Ian Shuffletone")
    i.add_calendar(2020)
    session = sqlite_session_factory()
    session.add(i)
    session.commit()
    res = session.query(Inspector).first()
    assert ScopeDate(2020, 1, 17) in res.calendar.scope_dates
    assert ScopeDate(2020, 1, 18) not in res.calendar.scope_dates


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


# **** Repository tests ****


def test_calendar_repository_list(sqlite_session_factory):
    session = sqlite_session_factory()
    session.execute(
        "INSERT INTO calendar (id, year, name)" "VALUES(1, 2021, 'test cal')"  # noqa
    )
    repo = CalendarRepository(session)
    res = repo.list()
    assert res[0].name == "test cal"
    assert res[0].year == 2021


def test_calendar_repository_get(sqlite_session_factory):
    session = sqlite_session_factory()
    session.execute(
        "INSERT INTO calendar (id, year, name)" "VALUES(1, 2021, 'test cal')"  # noqa
    )
    [[c_id]] = session.execute(
        "SELECT id FROM calendar WHERE name=:name AND year=:year",
        dict(name="test cal", year=2021),
    )
    session.execute(
        "INSERT INTO scope_date (id, year, month, day, isworking, calendar_id)"
        "VALUES(:id, :year, :month, :day, :isworking, :calendar_id)",
        dict(id=1, year=2021, month=1, day=1, isworking=1, calendar_id=c_id),
    )
    repo = CalendarRepository(session)
    res = repo.get(2021, "test cal")
    assert res.name == "test cal"
    assert res.year == 2021
    assert res.scope_dates[0].day == 1
    assert res.scope_dates[0].year == 2021
    assert res.scope_dates[0].month == 1
    assert res.scope_dates[0].isworking is True


def test_calendar_repository_add(sqlite_session_factory):
    c = Calendar(2019, "testes")
    session = sqlite_session_factory()
    repo = CalendarRepository(session)
    repo.add(c)
    session.commit()
    rows = session.execute("SELECT id, year, name FROM calendar")
    dates = session.execute(
        "SELECT year, month, day FROM scope_date WHERE year=:year AND month=:month AND day=:day",
        dict(year=2019, month=1, day=10),
    )
    assert list(rows) == [(1, 2019, "testes")]
    assert list(dates) == [(2019, 1, 10)]


def test_inspector_respository_add(sqlite_session_factory):
    i = Inspector("Ramon Chuffo")
    i.add_calendar(2020)
    session = sqlite_session_factory()
    repo = InspectorRepository(session)
    repo.add(i)
    session.commit()
    rows = session.execute("SELECT id, name FROM inspector")
    assert list(rows) == [(1, "Ramon Chuffo")]


def test_inspector_respository_get(sqlite_session_factory):
    session = sqlite_session_factory()
    session.execute("INSERT INTO inspector (name) VALUES('Sandy Bolstun')")
    repo = InspectorRepository(session)
    res = repo.get("Sandy Bolstun")
    assert res[0] == Inspector("Sandy Bolstun")


def test_inspector_respository_list(sqlite_session_factory):
    session = sqlite_session_factory()
    session.execute("INSERT INTO inspector (name) VALUES('Sandy Bolstun')")
    session.execute("INSERT INTO inspector (name) VALUES('Hayden McLeslo')")
    repo = InspectorRepository(session)
    insprs = repo.list()
    assert Inspector("Hayden McLeslo") in insprs
    assert Inspector("Sandy Bolstun") in insprs
