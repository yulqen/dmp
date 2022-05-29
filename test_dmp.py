import pytest
from .dmp import RegulatoryCycle
from datetime import date


@pytest.fixture
def cycle():
    return RegulatoryCycle(2022)


def test_reg_cycle_model_object(cycle):
    assert cycle.start_date == date(2022, 1, 1)


def test_reg_cycle_repr(cycle):
    assert str(cycle) == "RegulatoryCycle(2022)"


def test_reg_cycle_calendar():
    cycle = RegulatoryCycle(2023)
    assert list(cycle.calendar_month(1))[0] == date(2023, 1, 2)
    assert list(cycle.calendar_month(2))[0] == date(2023, 1, 30)
    assert list(cycle.calendar_month(3))[0] == date(2023, 2, 27)
    cycle = RegulatoryCycle(2024)
    assert list(cycle.calendar_month(1))[0] == date(2024, 1, 1)
    assert list(cycle.calendar_month(2))[0] == date(2024, 1, 29)
    assert list(cycle.calendar_month(3))[0] == date(2024, 3, 4)
    cycle = RegulatoryCycle(2025)
    assert list(cycle.calendar_month(1))[0] == date(2025, 1, 6)
    cycle = RegulatoryCycle(2026)
    assert list(cycle.calendar_month(1))[0] == date(2026, 1, 5)
