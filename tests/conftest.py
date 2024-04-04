from pathlib import Path
import pytest
import shutil
import yaml
from iSparrowRecord import set_up_sparrow as spf

DATA = None
CONFIG = None


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
@pytest.fixture(scope="module", autouse=True)
def install(request):
    custom_cfgdir = Path(__file__).resolve().parent.parent / Path("config")

    spf.set_up(custom_cfgdir)

    global DATA, CONFIG
    DATA = spf.SPARROW_RECORD_DATA
    CONFIG = spf.SPARROW_RECORD_CONFIG

    # remove again after usage

    def teardown():
        shutil.rmtree(str(DATA))
        shutil.rmtree(str(CONFIG))

    request.addfinalizer(teardown)


@pytest.fixture(scope="module")
def folders():
    custom_cfgdir = Path(__file__).resolve().parent.parent / Path("config")
    global DATA, CONFIG
    return str(CONFIG), str(DATA), str(custom_cfgdir)


@pytest.fixture(scope="module")
def audio_recorder_fx():
    filepath = Path(__file__).resolve()
    testpath = filepath.parent
    with open(testpath / Path("test_configs") / "cfg_test.yml", "r") as file:
        default_cfg = yaml.safe_load(file)

    return str(testpath), default_cfg
