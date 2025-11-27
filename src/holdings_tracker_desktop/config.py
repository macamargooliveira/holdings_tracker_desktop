import os
from dotenv import load_dotenv

# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------
ENV = os.getenv("APP_ENV", "development")
env_file = f".env.{ENV}"

if not os.path.exists(env_file):
    raise FileNotFoundError(f"Config file '{env_file}' not found.")

load_dotenv(env_file)

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def str_to_bool(value: str, default=False) -> bool:
    return value.lower() in ("1", "true", "yes", "on") if value else default

# ---------------------------------------------------------
# PUBLIC CONFIGURATION VALUES
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
SQL_ECHO = str_to_bool(os.getenv("SQL_ECHO"), default=False)
