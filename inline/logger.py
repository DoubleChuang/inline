import logging
import logging.config
import sys

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "inline.root": {"level": "INFO", "handlers": ["console"]},
        "inline.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "inline.error",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
    },
    "formatters": {
        "generic": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
}

logging.config.dictConfig(LOGGER_CONFIG)

logger = logging.getLogger("inline.root")
error_logger = logging.getLogger("inline.error")
