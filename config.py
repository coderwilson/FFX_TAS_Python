import yaml

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

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
                print(f"Error: Failed to parse config file {CONFIG_FILE_PATH}: {E}")
                return {}
    except Exception as E:
        print(f"Didn't find config file {CONFIG_FILE_PATH}, using default values for run.")
        return {}
