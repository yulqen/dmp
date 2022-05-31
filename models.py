import calendar
import datetime
import itertools
from dataclasses import dataclass, field
from typing import List


# models
@dataclass
class Inspector:
    id: int = field(init=False)
    name: str


class ScopeDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.isworking = True

    def weekday(self):
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
    def __init__(self, year: int):
        self.year = year

    def __repr__(self):
        return f"Calendar({self.year})"

    @property
    def base_working_days(self) -> List[ScopeDate]:
        """
        Return a list of date objects for the year. Weekend days omitted.
        """
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
                for d in list(range(true_first, len_ + 1))
            ]
            for d in month_days_:
                if d.weekday() in [5, 6]:
                    d.isworking = False
            out.append([d for d in month_days_ if d.isworking is True])
        return list(itertools.chain.from_iterable(out))


class RegulatoryCycle:
    def __init__(self, year: int):
        self.year = year
        self.calendar = Calendar(self.year)

    @property
    def base_working_days(self) -> List[ScopeDate]:
        """
        Return a list of date objects for the year. Weekend days omitted.
        """
        return self.calendar.base_working_days

    def __repr__(self):
        return f"RegulatoryCycle({self.year})"
