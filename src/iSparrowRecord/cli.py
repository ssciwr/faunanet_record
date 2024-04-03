import click
import iSparrowRecord.set_up_sparrow as sus
from iSparrowRecord import Runner
from iSparrowRecord.utils import read_yaml
from datetime import datetime
from pathlib import Path


@click.group()
def cli():
    pass


@cli.command()
@click.option("--cfg", help="custom configuration file", default="")
@click.option(
    "--suffix",
    help="Folder suffix for data collection",
    default="",
)
@click.option(
    "--standalone",
    help="Whether the package runs in standalone mode or as part of iSparrow",
    default=True,
)
def run(cfg: str, suffix: str, standalone: bool):

    if standalone:
        # test if the setup has been done already and if not do again
        sus.set_up()

    custom_cfg = {"Output": {"output_folder": sus.SPARROW_RECORD_DATA}}
    if cfg != "":
        custom_filepath = Path(cfg).expanduser()
        custom_cfg = read_yaml(custom_filepath)

    foldername = datetime.now().strftime("%y%m%d_%H%M%S") + "_" + suffix
    folderpath = Path(sus.SPARROW_RECORD_DATA).expanduser() / foldername
    folderpath.mkdir()

    # update config
    custom_cfg["Output"]["output_folder"] = str(folderpath)

    runner = Runner(custom_cfg)

    runner.run()


@cli.command()
def stop():
    click.echo("stop running shit")


if __name__ == "__main__":
    cli()
