import yaml
from pathlib import Path
from platformdirs import user_config_dir


def read_yaml(path: str):
    """
    read_yaml Read the yaml basic config file for iSparrow from path.
            It contains the install directory, data directory and other things used
            by iSparrow internally.

    Args:
        path (str): Path to the yaml base config.

    Returns:
        dict: read base config file.
    """

    if Path(path).exists() is False:
        raise FileNotFoundError(f"The folder {path} does not exist")

    with open(Path(path)) as file:
        cfg = yaml.safe_load(file)

    return cfg
