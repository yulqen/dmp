import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dmp.adaptors import orm
from dmp.domain.models import Inspector

logger = logging.getLogger(__name__)
engine = create_engine("sqlite+pysqlite:///app.db", echo=True, future=True)
Session = sessionmaker(engine)


def bootstrap_db():
    logger.info("Bootstrapping database")
    orm.start_mappers()
    with Session() as session:
        session.add(Inspector(name="Colin Brabham"))
        session.add(Inspector(name="Charl Schnitzel"))
        session.commit()


if __name__ == "__main__":
    bootstrap_db()
