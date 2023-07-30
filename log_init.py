import datetime
import logging
import time
from typing import Optional

import config


# Used to reset time reference at start of run
def reset_logging_time_reference():
    logging._start_time = time.time()


_MANIP_LEVEL = logging.DEBUG + 5


# Python has a logging library that will do what we want.
# Basic documentation here:     https://docs.python.org/3/howto/logging.html
# Advanced documentation here:  https://docs.python.org/3/howto/logging-cookbook.html


# Create a custom formatter for the timestamp, adding the delta property to the record
# This will hold the time from the start of the program
class DeltaTimeFormatter(logging.Formatter):
    white = "\x1b[0m"
    green = "\x1b[32;40m"
    blue = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    COLOR = {
        logging.DEBUG: blue,
        _MANIP_LEVEL: green,
        logging.INFO: white,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red,
    }

    def format(self, record):
        # Create a timestamp we can use to parse,
        # using the millisecond timestamp since start of program / 1000
        duration = datetime.datetime.utcfromtimestamp(record.relativeCreated / 1000)
        # Create the delta property, with the format 'HH:MM:SS'
        record.delta = duration.strftime("%H:%M:%S")
        # Create the delta_ms property, with the format 'HH:MM:SS.sss'
        record.delta_ms = (
            f"{duration.strftime('%H:%M:%S')}."
            + f"{int(duration.strftime('%f')) // 1000:03d}"
        )
        record.color = self.COLOR.get(record.levelno)
        record.color_reset = self.reset
        return super().format(record)


# This should be called once in main, before any calls to the logging library
def initialize_logging():
    # Adds a new log level for manipulation/predictions
    _add_log_level("MANIP", _MANIP_LEVEL)

    # Defines the format of the colored logs
    color_log_fmt = (
        "%(color)s[%(delta)s] %(name)-14s %(levelname)-5s %(message)s%(color_reset)s"
    )
    color_log_formatter = DeltaTimeFormatter(fmt=color_log_fmt)
    # Same format, but without the coloring
    bw_log_fmt = "[%(delta)s] %(name)-14s %(levelname)-5s %(message)s"
    bw_log_formatter = DeltaTimeFormatter(fmt=bw_log_fmt)
    # Log file specific format
    file_log_fmt = "[%(delta_ms)s] %(name)-16s %(levelname)-8s %(message)s"
    file_log_formatter = DeltaTimeFormatter(fmt=file_log_fmt)
    # Get current time in order to create log file name
    time_now = datetime.datetime.now()
    time_str = (
        f"{time_now.year}{time_now.month:02d}{time_now.day:02d}_"
        + f"{time_now.hour:02d}_{time_now.minute:02d}_{time_now.second:02d}"
    )

    # Set up logging to file
    logging.basicConfig(
        filename=f"Logs/FFX_Log_{time_str}.txt",
        filemode="w",  # Log everything in the file
        level=logging.DEBUG,
    )
    # Apply non-colored, file-specific formatter to file output
    logging.getLogger("").root.handlers[0].setFormatter(file_log_formatter)

    # Get the visible log level for the console logger from config.yaml
    config_data = config.open_config()
    config_logging = config_data.get("logging", {})
    console_log_level = config_logging.get("verbosity", "DEBUG")
    color_log = config_logging.get("color_log", False)

    # Set up the console logger
    console = logging.StreamHandler()
    console.setLevel(console_log_level)  # Log the appropriate information to console

    # Apply black&white formatter by default
    formatter_to_use = bw_log_formatter
    if color_log:
        formatter_to_use = color_log_formatter  # Apply color formatter
    console.setFormatter(formatter_to_use)

    # Add the handlers to the root logger
    logging.getLogger("").addHandler(console)

    # Turn off logging in specific sublibraries to prevent even more spam
    logging.getLogger("comtypes").setLevel(logging.WARNING)  # For pyttsx3

    # Now the logging to file/console is configured!


# Examples of using logging:
#
# import logging
#
# logging.debug('Log level: DEBUG')
# logging.info('Log level: INFO')
# logging.warning('Log level: WARNING')
# logging.error('Log level: ERROR')
# logging.critical('Log level: CRITICAL')
#
# logging.info(f"Some variable {some_var}")

# Examples with defining specific sources of log messages:
#
# import logging
#
# #setting up named logger
# logger = logging.getLogger(__name__)
#
# logger.info('In the submodule')


# Method for adding a custom log level. Adapted from:
# https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
def _add_log_level(level_name: str, level_num: int, method_name: Optional[str] = None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `level_name` becomes an attribute of the `logging` module with the value
    `level_num`. `method_name` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `method_name` is not specified, `level_name.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> _add_log_level('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """

    method_name = method_name or level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError(f"{level_name} already defined in logging module")
    if hasattr(logging, method_name):
        raise AttributeError(f"{method_name} already defined in logging module")
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError(f"{method_name} already defined in logger class")

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)
