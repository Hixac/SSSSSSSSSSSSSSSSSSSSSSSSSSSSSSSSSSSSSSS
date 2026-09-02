import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog

from src.core.config import settings


LOG_DIR = Path(__file__).parent.parent.parent.joinpath("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE_PATH = str(LOG_DIR.joinpath("app.log"))


pre_chain = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
]

file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=10 * 1024 * 1024, backupCount=5
)
file_handler.setLevel(settings.LOG_LEVEL)
file_handler.setFormatter(
    structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=False),
        foreign_pre_chain=pre_chain,
    )
)

console_handler = logging.StreamHandler()
console_handler.setLevel(settings.LOG_LEVEL)
console_handler.setFormatter(
    structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=True),
        foreign_pre_chain=pre_chain,
    )
)

logging.getLogger().handlers = [file_handler, console_handler]
logging.getLogger().setLevel(settings.LOG_LEVEL)

structlog.configure(
    processors=[*pre_chain, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)


__all__ = ["get_logger"]
