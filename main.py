from pathlib import Path
from iSparrowRecord import set_up_sparrow as sus

from iSparrowRecord.runner import Runner
from iSparrowRecord.cli import cli

if __name__ == "__main__":

    # # hardcoded paths and args will be replaced with commandline arguments later,
    # # or optionally with config node
    # cfgdir = Path(__file__).resolve().parent / Path("config")

    # runs_standalone = True

    # if runs_standalone:
    #     print("setting up sparrow")
    #     sus.set_up()

    # runner = Runner(cfgdir / "custom_example.yml")

    # runner.run()
    cli()