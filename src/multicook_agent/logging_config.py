import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOG_LEVEL = os.getenv("MULTICOOK_LOG_LEVEL", "INFO").upper()
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s\n"
    "    %(pathname)s:%(lineno)d in %(funcName)s()\n"
    "    pid=%(process)d tid=%(thread)d | %(message)s"
)
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "multicook_agent.log")


def configure_logging(level: str | None = None) -> None:
    """Configure root logging once for the whole project, writing to stdout and logs/."""
    level = level or LOG_LEVEL
    os.makedirs(LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[stream_handler, file_handler],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger."""
    return logging.getLogger(name)
