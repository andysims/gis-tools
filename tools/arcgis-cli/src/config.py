import os
from pathlib import Path
import logging
from dotenv import load_dotenv


def load_env(source: str, env_file: Path | None = None) -> dict:
    log = logging.getLogger(__name__)

    default_env = Path(__file__).resolve().parent.parent / ".env"
    env_path = Path(env_file) if env_file else default_env

    # Validate and load .env file
    if not env_path.exists():
        log.error(f".env file does not exist: {env_path}")
        return {}

    if not env_path.name.endswith(".env"):
        log.error(f"File provided is not a .env file: {env_path}")
        return {}

    try:
        load_dotenv(env_path)
        log.info(f"Successfully loaded .env file: {env_path}")
    except Exception as e:
        log.error(f"Error loading .env file: {e}")
        return {}

    source = source.lower().strip()

    if source == "portal":
        # Load/get portal info
        username = os.getenv("PORTAL_USERNAME")
        password = os.getenv("PORTAL_PASSWORD")
        url = os.getenv("PORTAL_URL")
    elif source == "agol":
        # Load/get agol info
        username = os.getenv("AGOL_USERNAME")
        password = os.getenv("AGOL_PASSWORD")
        url = os.getenv("AGOL_URL")
    else:
        log.error(f"Provided source {source} is not contained in .env")
        return {}

    creds = {"username": username, "password": password, "url": url}

    return creds
