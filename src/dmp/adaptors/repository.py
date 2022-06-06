import abc
import logging
from typing import Tuple

from dmp.domain.models import Calendar, Event, Inspector, ScopeDate
from sqlalchemy import select

logger = logging.getLogger(__name__)


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


class ScopeDateRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, date: ScopeDate):
        self.session.add(date)

    def get(self, date: Tuple):
        year, month, day = date
        return self.session.execute(
            select(ScopeDate).filter_by(year=year, month=month, day=day)
        ).one()

    def list(self):
        res = self.session.execute(select(ScopeDate)).all()
        return [r[0] for r in res]


class EventRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, name: str, cal: Calendar):
        self.session.add(Event(name))
        logger.info(f"Created Event({name}) to {cal}")

    def get(self, name: str, cal: Calendar):
        pass

    def list(self):
        return self.session.execute(select(Event)).all()
