from typing import List

from dmp.adaptors.repository import EventRepository, ScopeDateRepository
from dmp.domain.models import ScopeDate


def date_span(start: ScopeDate, end: ScopeDate, session) -> List[ScopeDate]:
    repo = ScopeDateRepository(session)
    dates = repo.list()
    start_id = [
        d.id
        for d in dates
        if (d.year == start.year and d.month == start.month and d.day == start.day)
    ][0]
    end_id = [
        d.id
        for d in dates
        if (d.year == end.year and d.month == end.month and d.day == end.day)
    ][0]
    idx = (start_id - 1, end_id - 1)
    return dates[idx[0] : idx[1] + 1]


def add_calendar_event(owner, name: str, start: ScopeDate, end: ScopeDate, session):
    dates = date_span(start, end, session)
    repo = EventRepository(session)
    for d in dates:
        repo.add(name, owner.calendar, dates)
    session.commit()
