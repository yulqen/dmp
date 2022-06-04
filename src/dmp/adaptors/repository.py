import abc
import logging
from typing import List

from dmp.domain.models import Calendar, Event, Inspector, ScopeDate
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

logger = logging.getLogger(__name__)


class MatchException(Exception):
    pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, year, name):
        raise NotImplementedError


class CalendarRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, cal: Calendar):
        cal.calendar_creator()
        self.session.add(cal)

    def list(self):
        return self.session.query(Calendar).all()

    def get(self, year, name):
        return self.session.execute(
            select(Calendar).filter_by(year=year, name=name).filter_by(name=name)
        ).one()[0]


class InspectorRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, name: str):
        self.session.add(name)

    def get(self, name: str):
        return self.session.execute(select(Inspector).filter_by(name=name)).one()

    def list(self):
        return self.session.query(Inspector).all()


class EventRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, name: str, cal: Calendar, dates: List[ScopeDate]):
        # TODO: fix this to iterate through all dates
        # try:
        #     self.session.execute(
        #         select(ScopeDate).filter_by(
        #             calendar_id=cal.id, year=year, month=month, day=day
        #         )
        #     ).one()
        # except NoResultFound:
        #     raise MatchException(
        #         f"Cannot find ScopeDate({year}, {month}, {day}) in {cal}"
        #     )
        self.session.add(Event(name, dates))
        logger.info(f"Created Event({name}) to {cal}")

    def get(self, name: str, cal: Calendar):
        pass

    def list(self):
        pass
