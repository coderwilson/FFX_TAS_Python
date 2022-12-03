import logging

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

logger = logging.getLogger(__name__)

# TODO: Make this be set by an argument instead
CONFIG_FILE_PATH = "config.yaml"


# TODO: It's not ideal to open this file many times over, but also not a huge problem
def open_config():
    # Open the config file and parse the yaml contents
    try:
        with open(CONFIG_FILE_PATH) as config_file:
            try:
                return yaml.load(config_file, Loader=Loader)
            except Exception as E:
                logger.error(f"Error: Failed to parse config file {CONFIG_FILE_PATH}")
                logger.exception(E)
                return {}
    except Exception:
        logger.info(
            f"Didn't find config file {CONFIG_FILE_PATH}, using default values for run."
        )
        return {}
