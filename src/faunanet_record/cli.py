from .utils import read_yaml, update_dict_recursive, dict_from_string
from .runner import Runner
from . import set_up as sus

from pathlib import Path
import warnings
import click
from platformdirs import user_config_dir


@click.group()
def cli():
    # empty because everything is done in subcommands
    pass


@cli.command()
@click.argument(
    "cfg_dir",
    type=str,
)
def install(cfg_dir: str):
    "The directory given must contain 'default.yml' and 'install.yml'. Check out the defaults provided in the code repository under './config'."
    sus.set_up(cfg_dir)


@cli.command()
@click.option("--cfg", help="custom configuration file", default="")
@click.option("--debug", help="Enable debug output", is_flag=True)
@click.option(
    "--defaults",
    help="Path to where the install and default configs are",
    default=str(user_config_dir("iSparrowRecord")),
)
@click.option(
    "--replace",
    help="Replace any entry in the config with a different value. Mostly useful for debugging or testing purposes.",
    default="{}",
)
def run(cfg: str, debug: bool, replace: str, defaults: str):
    # raise warning that no logging is there yet
    print("start data collection")
    if debug:
        warnings.warn(
            "Debug output currently not yet implemented. Will run, but without any debug output."
        )

    print("...preparing config")

    install_path = Path(defaults).expanduser() / "install.yml"

    if install_path.is_file() is False:
        raise FileNotFoundError(
            f"No install config file found at {install_path}. Has the system be set up by using the 'install' command line option first?"
        )

    # read install file and check if the system has been set up, raise if not
    install_cfg = read_yaml(str(Path(defaults).expanduser() / "install.yml"))

    data_folder = Path(install_cfg["Directories"]["data"]).expanduser()

    if data_folder.is_dir() is False:
        raise FileNotFoundError(
            f"Folder {data_folder} not found. Has the system be set up by using the 'install' command line option first?"
        )

    replace_dict = dict_from_string(replace)

    if cfg != "":
        custom_filepath = Path(cfg).expanduser()

        print("... ...using custom run config: ", custom_filepath)

        custom_cfg = read_yaml(custom_filepath)

        # when custom_cfg and replace have no top level nodes, they are merged, otherwise the leaves of custom_cfg is updated with replace.
        if len(set(custom_cfg.keys()).intersection(set(replace_dict.keys()))) > 0:
            update_dict_recursive(custom_cfg, replace_dict)
        else:
            custom_cfg = custom_cfg | replace_dict
    else:
        custom_cfg = replace_dict

    print("...creating runner")
    runner = Runner(custom_cfg, config_folder=defaults)

    runner.run()
