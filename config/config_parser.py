import toml


class Configuration:
    def __init__(self, database_path, show_mode):
        self.database = database_path
        self.show_mode = show_mode


def parse_config(config_path: str):
    """
    Reads the config placed at config_path and returns a 
    Configuration object filled.
    """
    conf = toml.load(config_path)
    return Configuration(
        conf["database"]["path"],
        conf["show_mode"])
