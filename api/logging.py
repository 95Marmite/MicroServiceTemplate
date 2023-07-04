import logging
import os
from typing import Optional

from api.config import Config

FILE_FORMAT = "%(asctime)s - [%(name)s | %(levelname)s]: %(message)s"
FILE_PATH = "log.log"

CONSOLE_FORMAT = "%(asctime)s [%(name)s | %(levelname)s]: %(message)s"


def _get_console_handler(level):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(CONSOLE_FORMAT)
    handler.setFormatter(formatter)

    return handler


def _get_file_handler(level, path):
    handler = logging.FileHandler(path)
    handler.setLevel(level)
    formatter = logging.Formatter(FILE_FORMAT)
    handler.setFormatter(formatter)

    return handler


file_handler: Optional[logging.FileHandler] = None
console_handler = _get_console_handler(logging.WARN)


def init(config: Config):
    global console_handler
    global file_handler

    log_destinations = config.logging.logdestinations
    log_console_level = None
    if "console" in log_destinations:
        log_console_level = config.logging.consoledebuglevel
    log_file_level = None
    log_file_path = None
    if "file" in log_destinations:
        log_file_path = os.path.join(config.logging.logdir, config.appname + ".log")
        log_file_level = config.logging.filedebuglevel

    if log_console_level:
        console_handler = _get_console_handler(log_console_level)
    if not file_handler and log_file_level and log_file_path:
        file_handler = _get_file_handler(log_file_level, log_file_path)

    # setup werkzeug logging
    werkzeug_log = logging.getLogger("werkzeug")
    werkzeug_log.setLevel(logging.DEBUG)


def get_logger(name):
    logger = logging.getLogger("{}".format(name))
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    while logger.handlers:
        logger.handlers.pop()

    if file_handler:
        logger.addHandler(file_handler)
    if console_handler:
        logger.addHandler(console_handler)

    return logger
