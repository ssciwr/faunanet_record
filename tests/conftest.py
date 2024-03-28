import pytest
import shutil

from . import set_up_sparrow_env

# add a fixture with session scope that emulates the result of a later to-be-implemented-install-routine
@pytest.fixture(scope="session", autouse=True)
def install(request):
    print("Creating iSparrow folders and downloading data... ")
    set_up_sparrow_env.install()
    print("Installation finished")

    # remove again after usage
    def teardown():
        shutil.rmtree(str(set_up_sparrow_env.HOME))
        shutil.rmtree(str(set_up_sparrow_env.DATA))
        shutil.rmtree(str(set_up_sparrow_env.OUTPUT))

    request.addfinalizer(teardown)


@pytest.fixture(scope="session")
def folders():
    global HOME, DATA, MODELS, OUTPUT, EXAMPLES
    return str(HOME), str(DATA), str(MODELS), str(OUTPUT), str(EXAMPLES)
