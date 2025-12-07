import os
from alembic.config import Config
from alembic import command

def run_migrations():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    alembic_ini = os.path.join(PROJECT_ROOT, "alembic.ini")

    alembic_cfg = Config(alembic_ini)
    alembic_cfg.set_main_option("script_location",
        "src/holdings_tracker_desktop/alembic"
    )

    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()
