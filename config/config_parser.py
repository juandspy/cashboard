import toml

from .config import Configuration

def parse_config(config_path: str):
    """
    Reads the config placed at config_path and returns a 
    Configuration object filled.
    """
    conf = toml.load(config_path)
    return Configuration(conf["database"]["path"])