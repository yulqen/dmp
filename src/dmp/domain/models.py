import calendar
import datetime
import itertools
from typing import List, Optional, Tuple


class ModelException(Exception):
    pass


class ScopeDate:
    """
    A ScopDate represents a date object. ScopeDate.isworking allows
    a client to designate working and non-working days.
    """

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.isworking = True
        self.calendar = Calendar(self.year)

    def weekday(self) -> int:
        return datetime.date(self.year, self.month, self.day).weekday()

    def __repr__(self):
        return f"ScopeDate({self.year}, {self.month}, {self.day})"

    def __eq__(self, other):
        if (
            self.day == other.day
            and self.month == other.month
            and self.year == other.year
        ):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.year, self.month, self.day))


class Calendar:
    def __init__(self, year: int, name: Optional[str] = None):
        self.year = year
        if name:
            self.name = name
        else:
            self.name = "default"
        self.scope_dates = []

    def __repr__(self):
        return f"Calendar({self.year}, {self.name})"

    def calendar_creator(self) -> List[ScopeDate]:
        """
        Given a Calendar object, returns a list of ScopeDate
        with weekend days removed.
        """
        if len(self.scope_dates) > 0:
            raise ModelException(
                f"Cannot create dates for {self} as the are already created."
            )
        out = []
        for month in range(1, 13):
            f, len_ = calendar.monthrange(self.year, month)
            if f == 5:  # first day of month is Sat
                true_first = 3
            elif f == 6:  # first day of month is Sun
                true_first = 2
            else:
                true_first = 1
            month_days_ = [
                ScopeDate(self.year, month, d)
                for d in list(range(true_first, len_ + 1))  # ignore
            ]
            for d in month_days_:
                if d.weekday() in [5, 6]:
                    d.isworking = False
            out.append([d for d in month_days_ if d.isworking is True])
        self.scope_dates = list(itertools.chain.from_iterable(out))


class Inspector:
    def __init__(self, name):
        self.name = name
        self.calendar = None

    def add_calendar(self, year: int):
        self.calendar = Calendar(year)
        self.calendar.calendar_creator()

    def __eq__(self, other):
        # TODO: This is not great - there may be two of same name
        return self.name == other

    def __repr__(self):
        return f'Inspector("{self.name}")'


class RegulatoryCycle:
    def __init__(self, year: int):
        self.year = year
        self.calendar = Calendar(self.year, "regulatory cycle")
        self.calendar.calendar_creator()

    def __repr__(self):
        return f"RegulatoryCycle({self.year})"


class Event:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Event({self.name})"
