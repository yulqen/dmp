# DNSyR Management Platform - prototype
from calendar import Calendar
from datetime import date


class RegulatoryCycle:
    def __init__(self, year: int):
        self.year = year

    @property
    def start_date(self):
        return date(self.year, 1, 1)

    def calendar_month(self, month: int):
        c = Calendar()
        res = list(c.itermonthdates(self.year, month))
        count = 0
        for d in res:
            if d.year == self.year - 1:
                count += 1
                continue
            else:
                if d.weekday() != 0:
                    count += 1
                    continue
                else:
                    break
        return res[count:] 

    def __repr__(self):
        return f"RegulatoryCycle({self.year})"
