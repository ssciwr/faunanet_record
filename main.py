from pathlib import Path
from set_up_fake_sparrow import set_up

from iSparrowRecord import Runner

if __name__ == "__main__":

    # hardcoded paths and args will be replaced with commandline arguments later,
    # or optionally with config node
    cfgdir = Path(__file__).resolve().parent / Path("config")

    runs_standalone = True

    if runs_standalone:
        print("setting up sparrow")
        set_up()

    runner = Runner(cfgdir / "custom_example.yml")

    runner.run()
