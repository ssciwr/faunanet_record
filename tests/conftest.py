import pytest
import shutil
from pathlib import Path
import yaml
import pyaudio

HOME = None
DATA = None
OUTPUT = None


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

    if "data" not in base_cfg_dirs:
        raise KeyError("The data folder for iSparrow must be given in the base config")

    if "output" not in base_cfg_dirs:
        raise KeyError(
            "The output folder for iSparrow must be given in the base config"
        )

    ish = Path(base_cfg_dirs["home"]).expanduser().resolve()
    isd = Path(base_cfg_dirs["data"]).expanduser().resolve()
    iso = Path(base_cfg_dirs["output"]).expanduser().resolve()

    for p in [ish, isd, iso]:
        p.mkdir(parents=True, exist_ok=True)

    return ish, isd, iso


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
@pytest.fixture(scope="session", autouse=True)
def install(request):
    print("Creating iSparrow folders and downloading data... ")
    # user cfg can override stuff that the base cfg has. When the two are merged, the result has
    # the base_cfg values whereever user does not have anything

    cfg_path = Path(__file__).resolve().parent.parent / "config"

    cfg = read_yaml(cfg_path / Path("default.yml"))

    home, data, output = make_directories(cfg["Directories"])

    shutil.copy(cfg_path / Path("default.yml"), home)

    global HOME, DATA, OUTPUT
    HOME = home
    DATA = data
    OUTPUT = output

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
    global HOME, DATA, OUTPUT
    return str(HOME), str(DATA), str(OUTPUT)


@pytest.fixture
def audio_recorder_fx():
    filepath = Path(__file__).resolve()
    testpath = filepath.parent
    with open(testpath / Path("test_configs") / "cfg_default.yml", "r") as file:
        default_cfg = yaml.safe_load(file)

    return testpath, default_cfg
