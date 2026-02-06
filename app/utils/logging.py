"""
Configuração de logging para a aplicação.
"""

import logging
import logging.handlers
from pathlib import Path

from utils.settings import get_settings

settings = get_settings()

_logging_configured = False


def setup_logging():
    """
    Configura o sistema de logging com handlers para console e arquivo rotativo.

    Args:
        None
    Returns:
        None
    """
    global _logging_configured
    if _logging_configured:
        return

    log_dir = Path(get_settings().LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, get_settings().LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(
        getattr(logging, get_settings().LOG_CONSOLE_LEVEL, logging.INFO)
    )
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        get_settings().LOG_FILE,
        maxBytes=get_settings().LOG_MAX_BYTES,
        backupCount=get_settings().LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(
        getattr(logging, get_settings().LOG_FILE_LEVEL, logging.WARNING)
    )
    logger.addHandler(file_handler)

    logging.getLogger("httpx").setLevel(logging.WARNING)

    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger com o nome especificado, configurando o logging se necessário.
    """
    setup_logging()
    return logging.getLogger(name)
