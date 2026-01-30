from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from holdings_tracker_desktop.config import config

# SQLite requires check_same_thread=False in GUI applications.
engine = create_engine(
    config.database_url,
    echo=config.sql_echo,
    connect_args=(
        {"check_same_thread": False}
        if config.database_url.startswith("sqlite")
        else {}
    ),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
