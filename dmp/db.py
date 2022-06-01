from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import registry, relationship, sessionmaker

from dmp.models import Calendar, Inspector, ScopeDate

engine = create_engine("sqlite+pysqlite:///app.db", echo=True, future=True)
Session = sessionmaker(engine)

mapper_registry = registry()
metadata = mapper_registry.metadata

scope_date = Table(
    "scope_date",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("day", Integer),
    Column("month", Integer),
    Column("year", Integer),
    Column(
        "calendar_id",
        Integer,
        ForeignKey("calendar.id"),
    ),
    Column("isworking", Boolean),
)

mapper_registry.map_imperatively(ScopeDate, scope_date)

calendar = Table(
    "calendar",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("year", Integer),
    Column("name", String(50)),
)

mapper_registry.map_imperatively(
    Calendar,
    calendar,
    properties={
        "scope_dates": relationship(
            ScopeDate,
            backref="calendar",
            cascade="all, delete, delete-orphan",
            order_by=scope_date.c.id,
        )
    },
)

inspector = Table(
    "inspector",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)

mapper_registry.map_imperatively(Inspector, inspector)


def bootstrap_db():
    metadata.create_all(engine)
    with Session() as session:
        session.add(Inspector(name="Colin Brabham"))
        session.add(Inspector(name="Charl Schnitzel"))
        session.commit()


if __name__ == "__main__":
    bootstrap_db()
