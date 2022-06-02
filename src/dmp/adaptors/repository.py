import abc

from dmp.domain.models import Calendar
from sqlalchemy import select


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
        self.session.add(cal)

    def list(self):
        return self.session.query(Calendar).all()

    def get(self, year, name):
        return self.session.execute(
            select(Calendar).filter_by(year=year, name=name).filter_by(name=name)
        ).one()[0]
