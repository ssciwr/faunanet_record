import shutil
from pathlib import Path
from platformdirs import user_config_dir
from .utils import read_yaml

SPARROW_RECORD_DATA = None
SPARROW_RECORD_CONFIG = None


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
    print("...making directories")

    if "data" not in base_cfg_dirs:
        raise KeyError("The data folder for iSparrow must be given in the base config")

    isd = Path(base_cfg_dirs["data"]).expanduser().resolve()
    isc = Path(user_config_dir("iSparrowRecord")).expanduser().resolve()
    for p in [isd, isc]:
        p.mkdir(parents=True, exist_ok=True)

    return isd, isc


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
def set_up(
    cfg_path: str,
):
    print("Creating iSparrow folders and downloading data")
    # user cfg can override stuff that the base cfg has. When the two are merged, the result has
    # the base_cfg values whereever user does not have anything

    print("...using install config", cfg_path)
    cfg = read_yaml(Path(cfg_path) / "install.yml")

    data, config = make_directories(cfg["Directories"])

    shutil.copy(Path(cfg_path) / "install.yml", config)

    shutil.copy(Path(cfg_path) / "default.yml", config)

    global SPARROW_RECORD_DATA, SPARROW_RECORD_CONFIG
    SPARROW_RECORD_DATA = data
    SPARROW_RECORD_CONFIG = config

    print("Installation finished")
