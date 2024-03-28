import pytest
import shutil
from pathlib import Path
import yaml
import platform
import pyaudio

HOME = None
DATA = None
MODELS = None
OUTPUT = None
EXAMPLES = None


# README: the below will later land in setup.py...
def read_yaml(path: str):
    print(f"...reading config from {path}")
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

    if "models" not in base_cfg_dirs:
        raise KeyError(
            "The models folder for iSparrow must be given in the base config"
        )

    if "data" not in base_cfg_dirs:
        raise KeyError("The data folder for iSparrow must be given in the base config")

    if "output" not in base_cfg_dirs:
        raise KeyError(
            "The output folder for iSparrow must be given in the base config"
        )

    ish = Path(base_cfg_dirs["home"]).expanduser().resolve()
    ism = Path(base_cfg_dirs["models"]).expanduser().resolve()
    isd = Path(base_cfg_dirs["data"]).expanduser().resolve()
    iso = Path(base_cfg_dirs["output"]).expanduser().resolve()
    ise = (Path(base_cfg_dirs["home"]).expanduser() / Path("example")).resolve()

    print(ish, ism, isd, iso, ise)
    for p in [ish, ism, isd, iso, ise]:
        p.mkdir(parents=True, exist_ok=True)

    return ish, ism, isd, iso, ise


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
@pytest.fixture(scope="session", autouse=True)
def install(request):
    print("Creating iSparrow folders and downloading data... ")
    # user cfg can override stuff that the base cfg has. When the two are merged, the result has
    # the base_cfg values whereever user does not have anything

    cfg_path = Path(__file__).resolve().parent.parent / "config"

    cfg = read_yaml(cfg_path / Path("install_cfg.yml"))

    home, models, data, output, examples = make_directories(cfg["Directories"])

    shutil.copy(cfg_path / Path("install_cfg.yml"), home)

    global HOME, DATA, MODELS, OUTPUT, EXAMPLES
    HOME = home
    DATA = data
    MODELS = models
    OUTPUT = output
    EXAMPLES = examples

    print("Installation finished, check audio devices: ")

    p = pyaudio.PyAudio()

    n = p.get_device_count()

    for i in range(n):
        info = p.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']}")

    # remove again after usage
    def teardown():
        shutil.rmtree(str(HOME))
        shutil.rmtree(str(DATA))
        shutil.rmtree(str(OUTPUT))

    request.addfinalizer(teardown)


@pytest.fixture(scope="session")
def folders():
    global HOME, DATA, MODELS, OUTPUT, EXAMPLES
    return str(HOME), str(DATA), str(MODELS), str(OUTPUT), str(EXAMPLES)


@pytest.fixture
def audio_recorder_fx():
    filepath = Path(__file__).resolve()
    testpath = filepath.parent
    with open(testpath / Path("test_configs") / "cfg_default.yml", "r") as file:
        default_cfg = yaml.safe_load(file)
    return testpath, default_cfg
