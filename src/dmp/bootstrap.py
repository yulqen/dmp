import logging

from dmp.adapters import orm

logger = logging.getLogger(__name__)


def bootstrap_db():
    logger.info("Bootstrapping database")
    orm.start_mappers()
    with Session() as session:
        session.add(Inspector(name="Colin Brabham"))
        session.add(Inspector(name="Charl Schnitzel"))
        session.commit()


if __name__ == "__main__":
    bootstrap_db()
