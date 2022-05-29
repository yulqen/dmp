# DNSyR Management Platform - prototype
import calendar
import itertools
from calendar import Calendar
from typing import List
from datetime import date


class ScopeDate(date):
    def __new__(cls, *args):
        d = date.__new__(cls, *args)
        d.isworking = True
        return d


class RegulatoryCycle:
    def __init__(self, year: int):
        self.year = year

    @property
    def start_date(self):
        return date(self.year, 1, 1)

    @property
    def base_working_days(self) -> List[date]:
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
                date(self.year, month, d) for d in list(range(true_first, len_ + 1))
            ]
            out.append([d for d in month_days_ if d.weekday() not in [5, 6]])
        return itertools.chain.from_iterable(out)

    def __repr__(self):
        return f"RegulatoryCycle({self.year})"
