from importlib.metadata import version, PackageNotFoundError

def get_app_version() -> str:
    try:
        return version("holdings-tracker-desktop")
    except PackageNotFoundError:
        return "0.0.0-dev"
