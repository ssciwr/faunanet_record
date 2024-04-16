import shutil
from pathlib import Path
from platformdirs import user_config_dir
from .utils import read_yaml

DATA = None
CONFIG = None


def make_directories(base_cfg_dirs: dict, for_tests: bool = False):
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

    isd = Path(base_cfg_dirs["data"]).expanduser().resolve()
    isc = Path(user_config_dir("iSparrowRecord")).expanduser().resolve()

    if for_tests:
        isd = isd / "tests"
        isc = isc / "tests"

    for p in [isd, isc]:
        p.mkdir(parents=True, exist_ok=True)

    return isd, isc


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
def set_up(for_tests: bool = False):
    print("Creating iSparrow folders and downloading data... ")
    # user cfg can override stuff that the base cfg has. When the two are merged, the result has
    # the base_cfg values whereever user does not have anything

    cfg_path = Path(__file__).resolve().parent.parent / "config"

    install_cfg = "install.yml"

    print("using install config", cfg_path / Path(install_cfg))
    cfg = read_yaml(cfg_path / Path(install_cfg))

    data, config = make_directories(cfg["Directories"], for_tests=for_tests)

    shutil.copy(cfg_path / Path(install_cfg), config)

    shutil.copy(cfg_path / Path("default.yml"), config)

    global DATA, CONFIG
    DATA = data
    CONFIG = config

    print("Installation finished")
