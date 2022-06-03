import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        in_repo = InspectorRepository(session)
        in_repo.add(Inspector(name="Colin Brabham"))
        in_repo.add(Inspector(name="Charl Schnitzel"))
        rc = RegulatoryCycle(2021)
        session.add(rc)
        session.commit()


if __name__ == "__main__":
    bootstrap_db()
