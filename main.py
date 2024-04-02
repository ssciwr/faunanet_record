import yaml
from iSparrowRecord import RecordingRunner
from platformdirs import user_config_dir
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="iSparrowRecord CLI")

parser.add_argument(
    "--cfg",
    default="default",
    help="Optional user defined yaml file providing arguments for data collection. (default: %(default)s)",
)

parser.add_argument(
    "--standalone",
    default=False,
    help="Whether SparrowRecorder runs alone or in conjunction with other Sparrow modules. (default: False)",
)


args = parser.parse_args()


def main():

    runs_standalone = args.standalone

    # get config files, then run
    default_filepath = Path(user_config_dir("iSparrowRecord")) / "default.yml"

    # get default config
    with open(default_filepath, "r") as cfgfile:
        default_cfg = yaml.safe_load(cfgfile)

    custom_filepath = args.cfg


    if custom_filepath != "default":
        custom_filepath = Path(custom_filepath).expanduser()
        with open(custom_filepath, "r") as cfgfile:
            custom_cfg = yaml.safe_load(cfgfile)

    print(custom_filepath, type(custom_filepath))

    config = default_cfg | custom_cfg

    # save total user config to file for documentation purposes

    # build Recordingrunner instance, then run
    runner = RecordingRunner.from_cfg(
        config["Data"]["Output"], config["Data"]["Recording"]
    )

    runner.run()


if __name__ == "__main__":
    main()
