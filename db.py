from sqlalchemy import Boolean, Column, Integer, String, Table, create_engine
from sqlalchemy.orm import registry, sessionmaker

from .models import Inspector, ScopeDate

engine = create_engine("sqlite+pysqlite:///app.db", echo=True, future=True)
Session = sessionmaker(engine)

mapper_registery = registry()
metadata = mapper_registery.metadata

inspector = Table(
    "inspector",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)

mapper_registery.map_imperatively(Inspector, inspector)

scope_date = Table(
    "scope_date",
    metadata,
    Column("day", Integer, primary_key=True),
    Column("month", Integer, primary_key=True),
    Column("year", Integer, primary_key=True),
    Column("isworking", Boolean),
)

mapper_registery.map_imperatively(ScopeDate, scope_date)


def bootstrap_db():
    metadata.create_all(engine)
    with Session() as session:
        session.add(Inspector(name="Colin Brabham"))
        session.add(Inspector(name="Charl Schnitzel"))
        session.commit()


if __name__ == "__main__":
    bootstrap_db()
