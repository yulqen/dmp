import logging

from dmp.domain.models import Calendar, Inspector, ScopeDate
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
)


def start_mappers():
    logger.info("Starting mappers")
    mapper_registry.map_imperatively(ScopeDate, scope_date)
    mapper_registry.map_imperatively(Inspector, inspector)
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
