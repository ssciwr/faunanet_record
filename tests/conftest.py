import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import pytest
import shutil
import yaml
import set_up_sparrow as spf

HOME = None
DATA = None
OUTPUT = None
CONFIG = None


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
@pytest.fixture(scope="module", autouse=True)
def install(request):

    spf.set_up()

    global HOME, DATA, OUTPUT, CONFIG
    HOME = spf.HOME
    DATA = spf.DATA
    OUTPUT = spf.OUTPUT
    CONFIG = spf.CONFIG

    print("folders: ", HOME, DATA, OUTPUT, CONFIG)

    # remove again after usage

    def teardown():
        shutil.rmtree(str(DATA))
        shutil.rmtree(str(OUTPUT))

    request.addfinalizer(teardown)


@pytest.fixture(scope="module")
def folders():
    custom_cfgdir = Path(__file__).resolve().parent.parent / Path("config")
    global HOME, DATA, OUTPUT, CONFIG
    return str(HOME), str(DATA), str(OUTPUT), str(CONFIG), str(custom_cfgdir)


@pytest.fixture(scope="module")
def audio_recorder_fx():
    filepath = Path(__file__).resolve()
    testpath = filepath.parent
    with open(testpath / Path("test_configs") / "cfg_test.yml", "r") as file:
        default_cfg = yaml.safe_load(file)

    return str(testpath), default_cfg
