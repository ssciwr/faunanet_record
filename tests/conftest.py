from pathlib import Path
import pytest
import shutil
import yaml
import iSparrowRecord.set_up as spf

DATA = None
CONFIG = None


# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
@pytest.fixture(autouse=True)
def install(request):
    custom_cfgdir = (
        Path(__file__).resolve().parent.parent / Path("tests") / "test_configs"
    )

    spf.set_up(
        cfg_path=str(custom_cfgdir),
    )

    global DATA, CONFIG
    DATA = spf.DATA
    CONFIG = spf.CONFIG

    # remove again after usage

    def teardown():
        shutil.rmtree(str(DATA))
        shutil.rmtree(str(CONFIG))

    request.addfinalizer(teardown)


@pytest.fixture()
def empty_data_folder(request):
    global DATA

    def teardown():
        for thing in Path(DATA).iterdir():
            shutil.rmtree(str(thing))

    request.addfinalizer(teardown)


@pytest.fixture()
def folders():
    custom_cfgdir = Path(__file__).resolve().parent / Path("test_configs")
    global DATA, CONFIG
    return str(CONFIG), str(DATA), str(custom_cfgdir)


@pytest.fixture()
def audio_recorder_fx():
    filepath = Path(__file__).resolve()
    testpath = filepath.parent
    with open(testpath / Path("test_configs") / "cfg_test.yml", "r") as file:
        default_cfg = yaml.safe_load(file)

    return str(testpath), default_cfg
