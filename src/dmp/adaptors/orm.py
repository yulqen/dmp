import logging

from dmp.domain.models import Calendar, Inspector, RegulatoryCycle, ScopeDate
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

logger = logging.getLogger(__name__)

engine = create_engine("sqlite+pysqlite:///app.db", echo=False, future=True)
Session = sessionmaker(engine)

mapper_registry = registry()
metadata = mapper_registry.metadata

regulatory_cycle = Table(
    "regulatory_cycle",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("year", Integer),
    Column("calendar_id", Integer, ForeignKey("calendar.id")),
)

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


calendar = Table(
    "calendar",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("year", Integer),
    Column("name", String(50)),
)


inspector = Table(
    "inspector",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("calendar_id", ForeignKey("calendar.id")),
)


def start_mappers():
    logger.info("Starting mappers")
    mapper_registry.map_imperatively(ScopeDate, scope_date)
    mapper_registry.map_imperatively(
        RegulatoryCycle,
        regulatory_cycle,
        properties={
            "calendar": relationship(
                Calendar,
                backref="regulatory_cycle",
                cascade="all, delete",
                order_by=calendar.c.id,
            )
        },
    )
    mapper_registry.map_imperatively(
        Inspector,
        inspector,
        properties={
            "calendar": relationship(
                Calendar,
                backref="inspector",
                cascade="all, delete",
                order_by=calendar.c.id,
            )
        },
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
    metadata.create_all(engine)
