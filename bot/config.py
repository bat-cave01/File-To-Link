from dotenv import load_dotenv
from os import environ as env

load_dotenv()


class Telegram:
    API_ID = int(env.get("TELEGRAM_API_ID", 0))
    API_HASH = env.get("TELEGRAM_API_HASH", "")
    OWNER_ID = int(env.get("OWNER_ID", 0))
    ALLOWED_USER_IDS = env.get("ALLOWED_USER_IDS", "").split()
    BOT_USERNAME = env.get("TELEGRAM_BOT_USERNAME", "")
    BOT_TOKEN = env.get("TELEGRAM_BOT_TOKEN", "")
    CHANNEL_ID = int(env.get("TELEGRAM_CHANNEL_ID", 0))
    SECRET_CODE_LENGTH = int(env.get("SECRET_CODE_LENGTH", 16))
    FORCE_CHANNEL_ID = int(env.get("FORCE_CHANNEL_ID", 0))
    FORCE_CHANNEL_LINK = env.get("FORCE_CHANNEL_LINK", "")


class Server:
    # Base URL (direct server URL, e.g. Render or local)
    BASE_URL = env.get("BASE_URL", "https://example.dev")

    # Optional Cloudflare Worker base URL (used as reverse proxy)
    CF_BASE_URL = env.get("CF_BASE_URL", "").strip()

    BIND_ADDRESS = env.get("BIND_ADDRESS", "0.0.0.0")
    PORT = int(env.get("PORT", 8080))

    @classmethod
    def get_public_url(cls):
        """
        Returns Cloudflare Worker URL if set, otherwise BASE_URL.
        This ensures generated download/stream links go through Cloudflare.
        """
        return cls.CF_BASE_URL or cls.BASE_URL


# LOGGING CONFIGURATION
LOGGER_CONFIG_JSON = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s",
            "datefmt": "%d/%m/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "event-log.txt",
            "formatter": "default",
        },
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "uvicorn": {"level": "INFO", "handlers": ["file_handler", "stream_handler"]},
        "uvicorn.error": {
            "level": "WARNING",
            "handlers": ["file_handler", "stream_handler"],
        },
        "bot": {"level": "INFO", "handlers": ["file_handler", "stream_handler"]},
        "hydrogram": {"level": "INFO", "handlers": ["file_handler", "stream_handler"]},
    },
}
