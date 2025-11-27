from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from holdings_tracker_desktop.config import DATABASE_URL, SQL_ECHO

# SQLite requires check_same_thread=False in GUI applications.
engine = create_engine(
    DATABASE_URL,
    echo=SQL_ECHO,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    from holdings_tracker_desktop.models.base import Base
    from holdings_tracker_desktop.models import (
        asset_event,
        asset_type,
        asset,
        broker_note,
        broker,
        country,
        currency,
        position_snapshot
    )

    Base.metadata.create_all(bind=engine)
