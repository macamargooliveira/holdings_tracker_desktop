import sys

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from pathlib import Path

from holdings_tracker_desktop.config import config
from holdings_tracker_desktop.database import engine, SessionLocal
from holdings_tracker_desktop.models.app_metadata import AppMetadata

class BootstrapError(Exception):
    pass

class Bootstrap:

    def run(self):
        try:
            final_revision = self._run_migrations_if_needed()
            self._initialize_metadata(final_revision)
        except Exception as e:
            raise BootstrapError(str(e)) from e

    def _run_migrations_if_needed(self):
        alembic_cfg = self._get_alembic_config()
        script = ScriptDirectory.from_config(alembic_cfg)

        head_rev = script.get_current_head()

        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current_rev = context.get_current_revision()

        if current_rev != head_rev:
            command.upgrade(alembic_cfg, "head")
            return head_rev or "unknown"

        return current_rev or "unknown"

    def _get_alembic_config(self) -> Config:
        base_path = self._get_base_path()
        alembic_path = base_path / "alembic"

        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", str(alembic_path))
        alembic_cfg.set_main_option("sqlalchemy.url", config.database_url)

        return alembic_cfg

    def _get_base_path(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys._MEIPASS)
        return Path(__file__).resolve().parent.parent

    def _initialize_metadata(self, final_revision: str):
        with SessionLocal() as session:
            try:
                self._ensure_seed(session)
                self._update_app_version_if_changed(session)
                self._update_schema_version_if_changed(session, final_revision)
                session.commit()
            except:
                session.rollback()
                raise

    def _ensure_seed(self, session):
        from holdings_tracker_desktop.database.seed import run_initial_seeds

        if self._get_metadata(session, "seed_executed"):
            return

        run_initial_seeds(session)

        session.add(AppMetadata(key="seed_executed", value="true"))

    def _update_app_version_if_changed(self, session):
        from holdings_tracker_desktop.version import get_app_version

        app_version = get_app_version()
        meta = self._get_metadata(session, "app_version")

        if not meta:
            session.add(AppMetadata(key="app_version", value=app_version))
            return

        if meta.value != app_version:
            meta.value = app_version

    def _update_schema_version_if_changed(self, session, final_revision):
        meta = self._get_metadata(session, "schema_version")

        if not meta:
            session.add(AppMetadata(key="schema_version", value=final_revision))
            return

        if meta.value != final_revision:
            meta.value = final_revision

    def _get_metadata(self, session, key: str):
        from sqlalchemy import select

        return session.execute(
            select(AppMetadata).where(AppMetadata.key == key)
        ).scalar_one_or_none()
