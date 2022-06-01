from datetime import date

import pytest
from dmp.models import Calendar, RegulatoryCycle, ScopeDate, _calendar_creator


@pytest.fixture
def cycle():
    return RegulatoryCycle(2022)


def test_reg_cycle_repr(cycle):
    assert str(cycle) == "RegulatoryCycle(2022)"


def test_calendar_creator():
    days = _calendar_creator(2022)
    first_day = ScopeDate(2022, 1, 3)
    assert days[0] == first_day
    # 8, 9 Jan 2022 is Saturday and Sunday respectively
    assert ScopeDate(2022, 1, 8) not in days
    assert ScopeDate(2022, 1, 9) not in days
    # 10 Jan 2022 is a Monday and is in scope
    assert ScopeDate(2022, 1, 10) in days


def test_reg_cycle_working_days():
    """
    The list of tuples are month, day dates representing weekends,
    which should not appear in the list of working days.
    """
    years = {2022: [(1, 8), (1, 9), (5, 1)], 2023: [(1, 1), (2, 18), (9, 16)]}
    for y, v in years.items():
        cycle = RegulatoryCycle(y)
        we1 = date(y, v[0][0], v[0][1])
        we2 = date(y, v[1][0], v[1][1])
        we3 = date(y, v[2][0], v[2][1])
        working = cycle.base_working_days
        assert we1 not in working
        assert we2 not in working
        assert we3 not in working


def test_our_date():
    d = ScopeDate(2022, 1, 3)
    assert d.isworking


def test_calendar():
    """
    A Calendar object can be used by various components in the system -
    the RegulatoryCycle, Inspectors, EPs, etc.
    """
    c = Calendar(2022, "test calendar")
    first_day = ScopeDate(2022, 1, 3)
    assert c.base_working_days[0] == first_day
    assert str(c) == "Calendar(2022, test calendar)"
    # 8, 9 Jan 2022 is Saturday and Sunday respectively
    assert ScopeDate(2022, 1, 8) not in c.base_working_days
    assert ScopeDate(2022, 1, 9) not in c.base_working_days
    # 10 Jan 2022 is a Monday and is in scope
    assert ScopeDate(2022, 1, 10) in c.base_working_days
