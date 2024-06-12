import shutil
from pathlib import Path
from platformdirs import user_config_dir
from .utils import read_yaml

DATA = None
CONFIG = None


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
        tuple: created folders: ( datafolder, configfolder)
    """
    print("...making directories")
    if "data" not in base_cfg_dirs:
        raise KeyError("The data folder for faunaanet must be given in the base config")

    if "config" not in base_cfg_dirs:
        base_cfg_dirs["config"] = "faunanet_record"

    isd = Path(base_cfg_dirs["data"]).expanduser().resolve()
    isc = Path(user_config_dir(base_cfg_dirs["config"])).expanduser().resolve()

    for p in [isd, isc]:
        p.mkdir(parents=True, exist_ok=True)

    return isd, isc


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
def set_up(cfg_path: str = ""):
    """
    set_up set up the faunanet-record system to be ready for running and recording data. Makes data and config folders and copies the default configs there.

    Args:
        cfg_path (str): Path to a folder containing "default.yml" (the default parameters) and "install.yml" (the install parameters).
        for_tests (bool, optional): Whether a special 'test' directory should be created for testing.
                                    Used in unit tests to not interfer with base installation mostly. Defaults to False.
    """
    print("Creating faunanet folders...")
    # user cfg can override stuff that the base cfg has. When the two are merged, the result has
    # the base_cfg values whereever user does not have anything
    if cfg_path == "":
        cfg_path = Path(__file__).resolve().parent.parent.parent / "config"

    if Path(cfg_path).is_dir() is False:
        raise ValueError("Given directory for install configs not defined")

    install_cfg = read_yaml(Path(cfg_path) / "install.yml")

    data, config = make_directories(install_cfg["Directories"])

    shutil.copy(Path(cfg_path) / "install.yml", config)

    shutil.copy(Path(cfg_path) / "default.yml", config)

    global DATA, CONFIG
    DATA = data
    CONFIG = config

    print("Installation finished")
