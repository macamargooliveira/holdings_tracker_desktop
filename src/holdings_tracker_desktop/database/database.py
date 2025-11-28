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

    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
