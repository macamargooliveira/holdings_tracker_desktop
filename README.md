# Holdings Tracker Desktop

[![Python Version](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Holdings Tracker Desktop is a **personal Python project** created for learning and practicing Python development.<br>
It allows you to manage and track financial holdings in a simple desktop interface.<br>
This application was created for study purposes and personal use.

## Features

### Asset Management
- Manage countries, currencies, asset types, brokers, and asset sectors.
- Track assets, asset events, broker notes, and ticker histories.

### Analytics
- Generate position snapshots.

### Application
- Desktop UI built with PySide6.
- Database migration and seeding scripts using Alembic.
- Utility scripts for development and testing.

## Project Structure

```
├── src/
│   └── holdings_tracker_desktop/
│       ├── alembic/      # Database migration files
│       ├── database/     # DB connection & scripts
│       ├── models/       # SQLAlchemy models
│       ├── repositories/ # DB operations
│       ├── schemas/      # Pydantic schemas
│       ├── services/     # Business logic
│       ├── ui/           # Desktop UI components
│       └── utils/        # Utility functions & exception handling
└── tests/                # Unit tests
```

## Requirements

- Python 3.12+
- SQLite (default database)
- Poetry (for dependency management and script execution)

## Setup

1. Install Poetry (if not already installed):
   ```bash
   pip install poetry
   ```

2. Install project dependencies and create virtual environment:
   ```bash
   poetry install
   ```

3. Run database migrations:
   ```bash
   poetry run migrations
   ```

4. Seed the database:
   ```bash
   poetry run seeds
   ```

## Usage

Run the desktop application:
```bash
poetry run app
```

## Testing

Run the test suite:
```bash
poetry run pytest
```

## Contributing
This is a personal project, but contributions are welcome!<br>
If you find bugs or have suggestions, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
