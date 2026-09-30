# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Holdings Tracker Desktop is a personal PySide6 desktop app (Python 3.12+, Poetry) for tracking investment holdings, backed by SQLite via SQLAlchemy 2 + Alembic, with Pydantic v2 schemas.

## Commands

```bash
poetry install                 # install deps (dev group includes pyinstaller)
poetry run app                 # run the app (holdings_tracker_desktop.main:main)
poetry run build-app           # wipe build/ and dist/, then run PyInstaller on HoldingsTracker.spec
poetry run pytest              # run tests (tests/ is currently empty; pytest is not a declared dependency)
poetry run pytest tests/test_x.py::test_name   # single test
poetry run python scripts/test_splash.py       # preview the splash screen in isolation
```

Migrations (Alembic, config in `alembic.ini`, scripts in `src/holdings_tracker_desktop/alembic/versions/`):

```bash
poetry run alembic revision --autogenerate -m "create foo"
poetry run alembic upgrade head
```

- `alembic/env.py` uses the app's own `engine` (from `config.database_url`), not the `sqlalchemy.url` in `alembic.ini`.
- Revision IDs are hand-numbered sequential strings (`'001'` ... `'011'`), and files are named `NNN_description.py`. Keep that pattern: set `revision`/`down_revision` manually instead of keeping Alembic's random hash.
- New models must be imported in `models/__init__.py` so autogenerate picks them up.

## Configuration / environments

- `config/config.py`: when not frozen, `APP_ENV` defaults to `development` and `.env.development` is loaded (in dev it sets `DATABASE_URL=sqlite:///./holdings_tracker_dev.db` and `SQL_ECHO=true`, relative to the CWD). The file is gitignored.
- When frozen (PyInstaller) or without `DATABASE_URL`, the DB lives at `%APPDATA%/HoldingsTracker/holdings_tracker.db`.
- The UI language is persisted with `QSettings` (`ui/core/app_settings.py`) and defaults to `pt_BR`.

## Startup flow

`main.py` shows `SplashScreen` first and imports heavy modules lazily. It then runs `database/bootstrap.py::Bootstrap`, which:
1. runs `alembic upgrade head` programmatically if the DB is behind. When frozen, it reads migrations from `sys._MEIPASS/alembic`, which `HoldingsTracker.spec` bundles through `datas`.
2. runs `database/seed.py::run_initial_seeds` once, guarded by the `seed_executed` row in `app_metadata`.
3. stores `app_version` (from installed package metadata, i.e. `pyproject.toml` version) and `schema_version` in `app_metadata`.

After that, `MainWindow` starts. Bumping the version means editing `pyproject.toml` and running `poetry install` again so `importlib.metadata` sees the new value.

## Architecture (layered)

`ui` → `services` → `repositories/base_repository.py` → `models`, with `schemas` as the boundary types.

- **models/**: SQLAlchemy 2 declarative (`Mapped`/`mapped_column`). Inherit `IdentifiedModel` (id) or `AuditableModel` (id + `created_at`/`updated_at` + `*_local` hybrid props). Models may define `from_create_schema`, `update_from_schema` and `validate_for_deletion`; the repository and services call these hooks when they exist.
- **schemas/**: Pydantic per entity, following the `XCreate` / `XUpdate` / `XResponse` pattern on `BaseSchema` (`from_attributes=True`, strips whitespace).
- **repositories/**: there is only one generic `BaseRepository[Model, Create, Update]`, and no per-entity repositories. It **commits on every write** and turns SQLAlchemy errors into `utils/exceptions.py` types (`NotFoundException`, `ConflictException`, `DatabaseException`, `ValidationException`, all `AppException`).
- **services/**: one class per entity, built with a `Session` (`XService(db)`), which creates a `BaseRepository` inside. Services hold the business rules (uniqueness checks, deletion guards). They return `XResponse` schemas, plus `list_all_for_ui(...)` methods that return plain dicts ready for tables.
- **Position snapshots are derived data.** `PositionSnapshotService.rebuild_from(asset_id, from_date)` deletes and recomputes snapshots (quantity, total cost) from the timeline of `AssetEvent`s and `BrokerNote`s. `AssetEventService` and `BrokerNoteService` call it after every create/update/delete. Any new operation that affects positions must trigger a rebuild too.
- **Sessions:** UI code opens a session per action with `with get_db() as db:` from `database/database.py`. It commits on exit and rolls back on exception.

## UI structure (`ui/`)

- `MainWindow` has two panels: `OperationsWidget` (left; a menu from `MENU_CONFIG` that swaps the content widget via `show_widget`/`navigate_to`) and `ChartsWidget` (right; matplotlib pie charts of allocation by asset/sector).
- **CRUD screens** subclass `widgets/entity_manager_widget.py::EntityManagerWidget` and override `load_data`, `open_new_form`, `open_edit_form(id)`, `delete_record(id)`, `open_details(id)`, `supports_details`, `get_enabled_actions`, `get_extra_buttons` and `get_toolbar_filters`. `add_grouped_total_rows` adds subtotal rows. Forms (`forms/`, based on `base_form_dialog.py`) and details dialogs (`dialogs/`, based on `base_details_dialog.py`) are imported lazily inside methods. Comboboxes that load their options from services are in `comboboxes/` (based on `base_combobox.py`).
- **i18n:** `ui/core/translations.py` has a `TRANSLATIONS` dict for `en_US` and `pt_BR`, plus `t(key)`, which falls back to the key itself. Add each new key to **both** languages. Widgets extend `TranslatableWidget` and put all user-visible text in `translate_ui()`. Changing the language calls `translate_ui()` on registered widgets and does not rebuild them. Date and number formats also depend on the language (`ui/core/formatters.py`).
- **Cross-widget refresh:** `ui/core/global_signals.py` has Qt signals (`asset_events_updated`, `asset_types_updated`, `broker_notes_updated`). Emit one after a mutation that other widgets or comboboxes depend on, such as the year comboboxes and charts.
- Styles live in `ui/styles/base.py`. Icons use `qtawesome` (`fa5s.*`). Flag SVGs load through `importlib.resources` from the `ui/flags` package (also listed in `pyproject.toml` `include`).

## Packaging notes

`HoldingsTracker.spec` bundles the `alembic/` directory and `alembic.ini`, and declares `hiddenimports`. If you add a migration dependency or a dynamically imported module, check the spec as well.

# Project conventions

## Language
- Write all code in English: identifiers, comments, docstrings, log messages and commit messages.
- Replies to the user in chat can stay in Portuguese.

## Commit messages
Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<optional scope>): <description>

<optional body>

<optional footer(s)>
```

- **Types:**
  - `feat`: a new feature
  - `fix`: a bug fix
  - `refactor`: a code change that neither fixes a bug nor adds a feature
  - `perf`: a performance improvement
  - `style`: formatting only, with no change in behavior
  - `test`: adding or updating tests
  - `docs`: documentation only
  - `build`: changes to packaging, dependencies, the PyInstaller spec or version bumps
  - `ci`: CI configuration
  - `chore`: other maintenance
- **Scope** is optional and names the area touched, matching the package layout under `src/holdings_tracker_desktop/`: `ui`, `models`, `repositories`, `services`, `schemas`, `database`, `alembic`, `config`, `utils`. It can also name a specific widget, e.g. `feat(assets-widget): ...`.
- **Description:** imperative mood, lowercase first letter, no trailing period, at most about 72 characters (e.g. `fix(ui): keep table header sizes after refresh`).
- **Body** (optional): explain what changed and why, wrapped at 72 characters and separated from the header by a blank line.
- **Breaking changes:** add `!` after the type/scope (`feat(models)!: ...`) and a `BREAKING CHANGE: <explanation>` footer.
- One logical change per commit. Commit a version bump on its own as `build: bump version to X.Y.Z` instead of mixing it into a feature commit.
