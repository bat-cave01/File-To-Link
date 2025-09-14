from os import environ as env

class Telegram:
    API_ID = int(env.get("TELEGRAM_API_ID", 545))
    API_HASH = env.get("TELEGRAM_API_HASH", "cc0")
    OWNER_ID = int(env.get("OWNER_ID", 1223296516))
    ALLOWED_USER_IDS = env.get("ALLOWED_USER_IDS", "").split()
    BOT_USERNAME = env.get("TELEGRAM_BOT_USERNAME", "File_to_Link_Bat_bot")
    BOT_TOKEN = env.get("TELEGRAM_BOT_TOKEN", "7523190604:A5454gdfgdgvg")
    CHANNEL_ID = int(env.get("TELEGRAM_CHANNEL_ID", -10545456464646))
    SECRET_CODE_LENGTH = int(env.get("SECRET_CODE_LENGTH", 24))
    FORCE_CHANNEL_ID = int(env.get("FORCE_CHANNEL_ID", -45464547757))
    FORCE_CHANNEL_LINK = env.get("FORCE_CHANNEL_LINK", "https://t.me/+CyoimDCsgfhghgfbhfghFuIzNDQ1")

class Server:
    BASE_URL = env.get("BASE_URL", "https://example.dev")
    BIND_ADDRESS = env.get("BIND_ADDRESS", "0.0.0.0")
    PORT = int(env.get("PORT", 8080))

# LOGGING CONFIGURATION
LOGGER_CONFIG_JSON = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'event-log.txt',
            'formatter': 'default'
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'uvicorn.error': {
            'level': 'WARNING',
            'handlers': ['file_handler', 'stream_handler']
        },
        'bot': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'hydrogram': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        }
    }
}
