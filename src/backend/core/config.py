import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig:
    HOST = os.getenv("APP_HOST", "localhost")
    PORT = int(os.getenv("APP_PORT", 8000))
    DEBUG = os.getenv("APP_DEBUG", "true").lower() in ("true", "1", "t")
    TITLE = os.getenv("APP_TITLE", "Concesionaria API")
    DESCRIPTION = os.getenv(
        "APP_DESCRIPTION", "API para gestionar vehículos en una concesionaria"
    )
    VERSION = os.getenv("APP_VERSION", "1.0.0")
    STATIC_DIR = f"{BASE_DIR}/static"
    STATIC_URL = "/static"
    IMAGES_DIR = f"{STATIC_DIR}/data"
    IMAGES_URL = f"{STATIC_URL}/data"


class DatabaseConfig:
    DB_FILE_NAME = "database.db"
    DB_DIR = f"{BASE_DIR}/data"
    DB_PATH = f"{DB_DIR}/{DB_FILE_NAME}"
    SQLITE_URL = f"sqlite:///{DB_PATH}"
    CLEAR_DB_ON_STARTUP = os.getenv("CLEAR_DB_ON_STARTUP", "false").lower() in (
        "true",
        "1",
        "t",
    )


class LoggerConfig:
    LOG_NAME = os.getenv("LOG_NAME", "app")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LIBRARY_LOGS_PREFIXES = ("uvicorn", "fastapi", "sqlalchemy", "sqlmodel")
    LOG_COLORS = {
        "DEBUG": "blue",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }


class EmailConfig:
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    # Email que figura como remitente en los correos enviados.
    FROM_EMAIL = os.getenv("FROM_EMAIL", "contacto@alejoide.com")
    # Email que recibe los mensajes de contacto, mail de la concesionaria.
    TO_EMAIL = os.getenv("TO_EMAIL", "contacto@alejoide.com")
