from dataclasses import dataclass, field
from sqlalchemy import Table, Column, String, Integer, create_engine
from sqlalchemy.orm import registry, sessionmaker

engine = create_engine("sqlite+pysqlite:///dmp.db", echo=True, future=True)
Session = sessionmaker(engine)

mapper_registery = registry()


# models
@dataclass
class Inspector:
    id: int = field(init=False)
    name: str


metadata = mapper_registery.metadata


inspector = Table(
    "inspector",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)

mapper_registery.map_imperatively(Inspector, inspector)

metadata.create_all(engine)


def insert_inspector():
    with Session() as session:
        session.add(Inspector(name="Colin Brabham"))
        session.add(Inspector(name="Charl Schnitzel"))
        session.commit()
