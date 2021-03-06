import logging

from dmp.domain.models import Calendar, Event, Inspector, RegulatoryCycle, ScopeDate
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
    Column("day", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("year", Integer, nullable=False),
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
    Column("year", Integer, nullable=False),
    Column("name", String(50)),
)


inspector = Table(
    "inspector",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("calendar_id", ForeignKey("calendar.id")),
)

event_date_assoc = Table(
    "event_date_assoc",
    metadata,
    Column("event_id", ForeignKey("event.id"), primary_key=True),
    Column("scope_date_id", ForeignKey("scope_date.id"), primary_key=True),
)

event = Table(
    "event",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("date_id", ForeignKey("scope_date.id")),
)


def start_mappers():
    logger.info("Starting mappers")
    mapper_registry.map_imperatively(
        ScopeDate,
        scope_date,
        properties={
            "events": relationship(
                Event,
                back_populates="dates",
                secondary=event_date_assoc,
            )
        },
    )
    mapper_registry.map_imperatively(
        Event,
        event,
        properties={
            "dates": relationship(
                ScopeDate,
                back_populates="events",
                secondary=event_date_assoc,
            )
        },
    )
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
    # doing this as a transaction as advised by in sqlalchemy
    # video at https://www.youtube.com/channel/UCCul-BKVL5EcAles3YW63yQ
    # at 46min
    with engine.begin() as conn:
        metadata.create_all(conn)
