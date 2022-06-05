from typing import List, Optional

from dmp.adaptors.repository import EventRepository, ScopeDateRepository
from dmp.domain.models import ScopeDate


class ServiceException(Exception):
    pass


def _date_span(start: ScopeDate, end: ScopeDate, session) -> List[ScopeDate]:
    """
    Given start and end dates, returns a list of ScopeDate objects,
    inclusive of those dates, that span the period. This list can be
    passed to EventRepository.add().
    """
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


def add_calendar_event(
    owner, name: str, start: ScopeDate, session, end: Optional[ScopeDate] = None
):
    """
    If owner has a Calendar object, add event name with start and end dates
    provided.
    """
    repo = EventRepository(session)
    try:
        owner.calendar
    except AttributeError:
        raise ServiceException(f"{owner} does not have a Calendar attribute.")
    if end:
        dates = _date_span(start, end, session)
        for d in dates:
            repo.add(name, owner.calendar, dates)
        session.commit()
    else:
        repo.add(name, owner.calendar, [start])
