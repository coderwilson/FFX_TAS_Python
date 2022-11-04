import copy
import datetime
import logging
import time

import config


# Used to reset time reference at start of run
def reset_logging_time_reference():
    logging._startTime = time.time()


# Python has a logging library that will do what we want.
# Basic documentation here:     https://docs.python.org/3/howto/logging.html
# Advanced documentation here:  https://docs.python.org/3/howto/logging-cookbook.html

# Create a custom formatter for the timestamp, adding the delta property to the record
# This will hold the time from the start of the program
class DeltaTimeFormatter(logging.Formatter):
    def format(self, record):
        # Create a timestamp we can use to parse, using the millisecond timestamp since start of program / 1000
        duration = datetime.datetime.utcfromtimestamp(record.relativeCreated / 1000)
        # Create the delta property, with the format 'HH:MM:SS.sss'
        # Latter part may be removed if we are not interested in milliseconds, or replaced with %f if we want microseconds.
        record.delta = f"{duration.strftime('%H:%M:%S')}.{int(duration.strftime('%f')) // 1000:03d}"
        return super().format(record)


# This should be called once in main, before any calls to the logging library
def initialize_logging():
    # Defines the format of the logs
    log_format = "[%(delta)s] %(name)-12s %(levelname)-8s %(message)s"
    formatter = DeltaTimeFormatter(fmt=log_format)
    # Get current time in order to create log file name
    timeNow = datetime.datetime.now()
    timeStr = f"{timeNow.year}{timeNow.month:02d}{timeNow.day:02d}_{timeNow.hour:02d}_{timeNow.minute:02d}_{timeNow.second:02d}"

    # Set up logging to file
    logging.basicConfig(
        filename=f"Logs/FFX_Log_{timeStr}.txt",
        filemode="w",  # Log everything in the file
        level=logging.DEBUG,
    )
    logging.getLogger("").root.handlers[0].setFormatter(formatter)
    # Apply DeltaTimeFormatter formatter

    # Get the visible log level for the console logger from config.yaml
    config_data = config.open_config()
    console_log_level = config_data.get("verbosity", "DEBUG")

    # Set up the console logger
    console = logging.StreamHandler()
    console.setLevel(console_log_level)  # Log the appropriate information to console
    console.setFormatter(formatter)  # Apply DeltaTimeFormatter formatter

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
