import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from traceback import format_exc
from typing import *


class LoggerAdapter(logging.LoggerAdapter):
    """Logger with prefix if necessary"""

    def __init__(self, logger: Logger, prefix: Union[str, Tuple]=None):
        super(LoggerAdapter, self).__init__(logger, {})
        if isinstance(prefix, str):
            prefix = (prefix,)
        prefix = ''.join([f'[{item}]' for item in prefix])
        self.prefix = prefix

    def process(self, msg, kwargs):
        if self.prefix is not None:
            msg = f'{self.prefix} {msg}'
        return msg, kwargs


def _default_logger(name: str) -> Logger:
    logger = Logger(name)
    logger.setLevel(logging.INFO)
    return logger


def _default_formatter() -> logging.Formatter:
    return logging.Formatter('[{asctime}][{levelname}] {message}', '%Y-%m-%d %H:%M:%S', style='{')


def silent_logger() -> Logger:
    """No logging"""
    logger = logging.getLogger('silent')
    logger.setLevel(logging.CRITICAL + 1)
    return logger


def console_logger(name: str, prefix: Union[str, Tuple]=None) -> Union[LoggerAdapter, Logger]:
    """Simple console logger"""
    logger = _default_logger(name)
    formatter = _default_formatter()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    if prefix is not None:
        logger = LoggerAdapter(logger=logger,  prefix=prefix)
    return logger


def file_logger(
        name: str, log_path: Path, console: bool=False, prefix: Union[str, Tuple]=None) -> Union[LoggerAdapter, Logger]:
    """Simple file logger"""
    from pysimple.io import ensure_filedir
    log_path = ensure_filedir(log_path)
    logger = console_logger(name) if console else _default_logger(name)
    formatter = _default_formatter()
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if prefix is not None:
        logger = LoggerAdapter(logger=logger, prefix=prefix)
    return logger


def daily_file_logger(
        name: str, log_path: Path, console: bool=False, prefix: Union[str, Tuple]=None) -> Union[LoggerAdapter, Logger]:
    """Logger that recreates log files per day"""
    from pyjooble.io import ensure_filedir
    log_path = ensure_filedir(log_path)
    logger = console_logger(name) if console else _default_logger(name)
    formatter = _default_formatter()
    file_handler = TimedRotatingFileHandler(log_path, when='midnight', interval=1)
    file_handler.suffix = '%Y-%m-%d'
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if prefix is not None:
        logger = LoggerAdapter(logger=logger, prefix=prefix)
    return logger


def report_err(logger: logging.Logger, msg: str):
    """Report error message with traceback"""
    logger.error(msg)
    logger.error(format_exc())


# Deprecated naming
file_logger_per_day = daily_file_logger
