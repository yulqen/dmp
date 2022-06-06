import logging

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import dmp.service
from dmp.adaptors import orm
from dmp.adaptors.repository import InspectorRepository
from dmp.domain.models import Inspector, RegulatoryCycle

logger = logging.getLogger(__name__)
engine = create_engine("sqlite+pysqlite:///app.db", echo=True, future=True)
Session = sessionmaker(engine)


def bootstrap_db():
    logger.info("Bootstrapping database")
    orm.start_mappers()
    with Session() as session:
        i1 = Inspector(name="Colin Brabham")
        i2 = Inspector(name="Charl Schnitzel")
        i1.add_calendar(2021)
        i2.add_calendar(2021)
        session.add(i1)
        session.add(i2)
        session.commit()
        dmp.service.add_calendar_event(
            i1, "Colin at Christmas", (2021, 12, 15), session, (2021, 12, 24)
        )
        rc = RegulatoryCycle(2021)
        session.add(rc)
        session.commit()


if __name__ == "__main__":
    bootstrap_db()
