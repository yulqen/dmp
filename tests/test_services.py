import dmp.service
import pytest
from dmp.adaptors.repository import EventRepository
from dmp.domain.models import Calendar, Inspector, ScopeDate

# ensure that the 'mappers' fixture from conftest runs for each test
pytestmark = pytest.mark.usefixtures("mappers")


def test_add_event_for_item_with_no_calendar(sqlite_session_factory):
    class _nocal:
        def __repr__(self):
            return "_nocal()"

    c = _nocal()
    session = sqlite_session_factory()
    a, b = (1, 2)
    with pytest.raises(dmp.service.ServiceException) as exc_info:
        dmp.service.add_calendar_event(c, "Illegal", a, b, session)
    assert exc_info.value.args[0] == "_nocal() does not have a Calendar attribute."


def test_add_single_event_for_inspector(sqlite_session_factory):
    session = sqlite_session_factory()
    i = Inspector("Harold Chroma")
    i.add_calendar(2020)
    session.add(i)
    session.commit()
    start = (2020, 2, 14)  # in scope
    dmp.service.add_calendar_event(i, "Harold's Day Off", start, session)
    repo = EventRepository(session)
    events = repo.list()
    assert events[0][0].dates[0] == ScopeDate(2020, 2, 14)


def test_add_span_for_inspector(sqlite_session_factory):
    session = sqlite_session_factory()
    i = Inspector("Harold Chroma")
    i.add_calendar(2020)
    session.add(i)
    session.commit()
    start = (2020, 2, 14)  # in scope
    end = (2020, 3, 2)  # in scope
    dmp.service.add_calendar_event(i, "Harold's Holidays", start, session, end)
    repo = EventRepository(session)
    events = repo.list()
    for e in events:
        assert ScopeDate(*start) in e[0].dates
        assert ScopeDate(*end) in e[0].dates


@pytest.mark.skip("TODO")
def test_add_span_includes_noworking_date(sqlite_session_factory):
    # TODO: should throw exception if one or both dates are non isworking
    pass


def test_date_span_no_weekend(sqlite_session_factory):
    session = sqlite_session_factory()
    c = Calendar(2022)
    c.calendar_creator()
    session.add(c)
    session.commit()
    # event from Monday 14th Feb to Thursday 17th Feb
    # we don't know if these span a weekend
    start = ScopeDate(2022, 2, 14)
    end = ScopeDate(2022, 2, 17)
    valid_dates = dmp.service._date_span(start, end, session)
    assert len(valid_dates) == 4  # no intervening non-working days
    assert valid_dates[0].year == 2022
    assert valid_dates[0].month == 2
    assert valid_dates[0].day == 14
    assert valid_dates[-1].year == 2022
    assert valid_dates[-1].month == 2
    assert valid_dates[-1].day == 17


def test_date_span_over_weekend(sqlite_session_factory):
    session = sqlite_session_factory()
    c = Calendar(2022)
    c.calendar_creator()
    session.add(c)
    session.commit()
    # event from Friday 3rd June to Friday 10th June
    # we don't know if these span a weekend
    start = ScopeDate(2022, 6, 3)
    end = ScopeDate(2022, 6, 10)
    valid_dates = dmp.service._date_span(start, end, session)
    assert len(valid_dates) == 6  # no intervening non-working days
    assert valid_dates[0].year == 2022
    assert valid_dates[0].month == 6
    assert valid_dates[0].day == 3
    assert valid_dates[-1].year == 2022
    assert valid_dates[-1].month == 6
    assert valid_dates[-1].day == 10
