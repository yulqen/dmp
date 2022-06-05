import dmp.service
import pytest
from dmp.domain.models import Calendar, ScopeDate

# ensure that the 'mappers' fixture from conftest runs for each test
pytestmark = pytest.mark.usefixtures("mappers")


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
    valid_dates = dmp.service.date_span(start, end, session)
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
    valid_dates = dmp.service.date_span(start, end, session)
    assert len(valid_dates) == 6  # no intervening non-working days
    assert valid_dates[0].year == 2022
    assert valid_dates[0].month == 6
    assert valid_dates[0].day == 3
    assert valid_dates[-1].year == 2022
    assert valid_dates[-1].month == 6
    assert valid_dates[-1].day == 10