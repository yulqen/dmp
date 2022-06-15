from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from dmp.adaptors.repository import EventRepository, ScopeDateRepository
from dmp.domain.models import Calendar, Event, ScopeDate


class ServiceException(Exception):
    pass


class MatchException(Exception):
    pass


def assoc_dates_with_event(event, calendar, dates, session):
    """
    Given an Event and a calendar, ensure that the dates (tuples)
    are assigned.
    """
    out_dates = []
    for d in dates:
        try:
            out_dates.append(
                session.execute(
                    select(ScopeDate).filter_by(
                        year=d[0], month=d[1], day=d[2], calendar_id=calendar.id
                    )
                ).one()
            )
        except NoResultFound:
            raise MatchException(
                f"Cannot find ScopeDate({d[0]}, {d[1]}, {d[2]}) in {calendar}"
            )
    event.dates = [d[0] for d in out_dates]
    session.add(event)
    session.commit()


def _date_span(start, end, session):
    """
    Given start and end dates, returns a list of tuples representing
    ScopeDate objects,inclusive of those dates, that span the period.
    This list can be passed to EventRepository.add().
    """
    repo = ScopeDateRepository(session)
    dates = repo.list()
    start_id = [
        d.id
        for d in dates
        if (d.year == start[0] and d.month == start[1] and d.day == start[2])
    ][0]
    end_id = [
        d.id
        for d in dates
        if (d.year == end[0] and d.month == end[1] and d.day == end[2])
    ][0]
    idx = (start_id - 1, end_id - 1)
    scs = dates[idx[0] : idx[1] + 1]
    return [(d.year, d.month, d.day) for d in scs]


def add_calendar_event(owner, name, start, session, end=None):
    """
    If owner has a Calendar object, add event name with start and end dates
    provided.
    """
    repo = EventRepository(session)
    try:
        owner.calendar
    except AttributeError:
        raise ServiceException(f"{owner} does not have a Calendar attribute.")
    repo.add(name, owner.calendar)
    if end:
        dates = _date_span(start, end, session)
        # FIXME - need to fetch unique Event object here!
        ev_ = session.execute(select(Event).where(Event.name == name)).fetchone()
        assoc_dates_with_event(ev_[0], owner.calendar, dates, session)
        session.commit()
    else:
        # FIXME - need to fetch unique Event object here!
        ev_ = session.execute(select(Event).where(Event.name == name)).fetchone()
        assoc_dates_with_event(ev_[0], owner.calendar, [start], session)
        session.commit()
