import pytest
import shutil
from pathlib import Path
import yaml
from platformdirs import user_config_dir

HOME = None
DATA = None
OUTPUT = None
CONFIG = None


# README: the below will later land in setup.py...
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
        base_cfg = yaml.safe_load(file)

    return base_cfg


def make_directories(base_cfg_dirs: dict):
    """
    make_directories Make all the directories for sparrow.


    Args:
        base_cfg_dirs (dict): Dictionary containing paths for the main install ("home"),
        the directory where models are stored ("models"), the one where data may be stored ("data")
        and the "output" directory to store inference results and potentially other data in ("output")

    Raises:
        KeyError: A folder given in the config does not exist

    Returns:
        tuple: created folders: (isparrow-homefolder, modelsfolder, datafolder, outputfolder, examplefolder)
    """
    print("...Making direcotries...")
    if "home" not in base_cfg_dirs:
        raise KeyError("The home folder for iSparrow must be given in the base config")

    if "data" not in base_cfg_dirs:
        raise KeyError("The data folder for iSparrow must be given in the base config")

    if "output" not in base_cfg_dirs:
        raise KeyError(
            "The output folder for iSparrow must be given in the base config"
        )

    ish = Path(base_cfg_dirs["home"]).expanduser().resolve()
    isd = Path(base_cfg_dirs["data"]).expanduser().resolve()
    iso = Path(base_cfg_dirs["output"]).expanduser().resolve()
    isc = Path(user_config_dir("iSparrowRecord")).expanduser().resolve()
    for p in [ish, isd, iso, isc]:
        p.mkdir(parents=True, exist_ok=True)

    return ish, isd, iso, isc


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
def set_up():
    print("Creating iSparrow folders and downloading data... ")
    # user cfg can override stuff that the base cfg has. When the two are merged, the result has
    # the base_cfg values whereever user does not have anything

    cfg_path = Path(__file__).resolve().parent.parent / "config"

    install_cfg = "install.yml"

    print("using install config", cfg_path / Path(install_cfg))
    cfg = read_yaml(cfg_path / Path(install_cfg))

    home, data, output, config = make_directories(cfg["Directories"])

    shutil.copy(cfg_path / Path(install_cfg), config)

    shutil.copy(cfg_path / Path("default.yml"), config)

    global HOME, DATA, OUTPUT, CONFIG
    HOME = home
    DATA = data
    OUTPUT = output
    CONFIG = config

    print("Installation finished")
