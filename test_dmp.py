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


def test_reg_cycle_working_days():
    years = {2022: [(1, 8), (1, 9), (5, 1)], 2023: [(1, 1), (2, 18), (9, 16)]}
    for y, v in years.items():
        cycle = RegulatoryCycle(y)
        we1 = date(y, v[0][0], v[0][1])
        we2 = date(y, v[1][0], v[1][1])
        we3 = date(y, v[2][0], v[2][1])
        _working = cycle.base_working_days
        assert we1 not in _working
        assert we2 not in _working
        assert we3 not in _working
