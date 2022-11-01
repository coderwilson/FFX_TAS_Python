import logging
import datetime
import config

# Python has a logging library that will do what we want.
# Basic documentation here:     https://docs.python.org/3/howto/logging.html
# Advanced documentation here:  https://docs.python.org/3/howto/logging-cookbook.html

# This should be called once in main, before any calls to the logging library
def initialize_logging():
    # Defines the format of the logs
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    # Get current time in order to create log file name
    timeNow = datetime.datetime.now()
    timeStr = f"{timeNow.year}{timeNow.month}{timeNow.day}_{timeNow.hour}_{timeNow.minute}_{timeNow.second}"
    # Set up logging to file
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        filename=f"Logs/FFX_Log_{timeStr}.txt",
        filemode='w'
    )

    # Set up the console logger, which may have different visible log level
    config_data = config.open_config()
    console_log_level = config_data.get("verbosity", "DEBUG")

    console = logging.StreamHandler()
    console.setLevel(console_log_level)
    # Set up the format of the console output
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    console.setFormatter(formatter)
    # Add the console handler to the root logger
    logging.getLogger('').addHandler(console)

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
# battle_log = logging.getLogger('battle')
#
# battle_log.info('In the battle module')
