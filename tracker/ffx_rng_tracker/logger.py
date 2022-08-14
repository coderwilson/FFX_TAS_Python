import logging
from functools import wraps
from traceback import format_tb
from types import TracebackType

from .data.file_functions import get_version


def log_exceptions(logger: logging.Logger | None = None):
    """Decorator used to log unhandled exceptions."""
    if logger is None:
        logger = logging.getLogger(LOGGER_NAME)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                issue = 'exception in '+func.__name__+'\n\n'
                logger.exception(issue)
                raise
        return wrapper
    return decorator


def setup_logger(logger: logging.Logger | None = None) -> None:
    """Setup for a logger, defaults to the root logger."""
    if logger is None:
        logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logfile = logging.FileHandler('ffx_rng_tracker_errors.log')
    logger.addHandler(logfile)
    fmt = '=============\n%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logfile.setFormatter(logging.Formatter(fmt))


def log_tkinter_error(error: Exception,
                      message: tuple[str],
                      tb: TracebackType,
                      ) -> None:
    """Receives an error from Tkinter, prints it
    and logs it to the root logger.
    """
    error_message = (f'Exception in Tkinter callback\n'
                     f'Traceback (most recent call last):\n'
                     f'{"".join(format_tb(tb))}'
                     f'{error.__name__}: {message}')
    logger = logging.getLogger(LOGGER_NAME)
    logger.error(error_message)
    print(error_message)


LOGGER_NAME = f'{__name__} v{".".join(map(str, get_version()))}'
