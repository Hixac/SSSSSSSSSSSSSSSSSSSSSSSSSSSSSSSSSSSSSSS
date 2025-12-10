from collections.abc import Generator

from .config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
    Session
)

class Base(DeclarativeBase):
    pass

engine = create_engine(settings.DATABASE_URL)
session_instance = sessionmaker(engine)

def get_db() -> Generator[Session]:
    with session_instance() as db:
        yield db
