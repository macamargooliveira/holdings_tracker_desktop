import os
import sys

from pathlib import Path
from dotenv import load_dotenv

class Config:
    IS_FROZEN = getattr(sys, "frozen", False)
    APP_ENV = (
        "production"
        if getattr(sys, "frozen", False)
        else os.getenv("APP_ENV", "development")
    )

    def __init__(self) -> None:
        self._load_env()
        self._init_paths()
        self._init_database()
        self._init_flags()

    def _load_env(self) -> None:
        if self.IS_FROZEN or self.APP_ENV != "development":
            return

        env_file = Path(f".env.{self.APP_ENV}")
        if env_file.exists():
            load_dotenv(env_file)

    def _init_paths(self) -> None:
        self.app_data_dir = self._get_app_data_dir()
        self.app_data_dir.mkdir(parents=True, exist_ok=True)

    def _init_database(self) -> None:
        env_db_url = os.getenv("DATABASE_URL")

        if env_db_url:
            self.database_url = env_db_url
            self.database_path = None
        else:
            self.database_path = self.app_data_dir / "holdings_tracker.db"
            self.database_url = f"sqlite:///{self.database_path}"

    def _init_flags(self) -> None:
        self.sql_echo = self._str_to_bool(os.getenv("SQL_ECHO"), False)

    @staticmethod
    def _get_app_data_dir() -> Path:
        if os.name == "nt":
            base = Path(os.environ["APPDATA"])
        else:
            base = Path.home() / ".local" / "share"
        return base / "HoldingsTracker"

    @staticmethod
    def _str_to_bool(value: str | None, default=False) -> bool:
        if value is None:
            return default
        return value.lower() in ("1", "true", "yes", "on")
