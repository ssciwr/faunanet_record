import yaml
from platformdirs import user_config_dir
from pathlib import Path
import argparse
from datetime import datetime
from iSparrowRecord import Recorder
from set_up_fake_sparrow import set_up
import warnings

parser = argparse.ArgumentParser(description="iSparrowRecord CLI")

parser.add_argument(
    "--cfg",
    default="default",
    help="Optional user defined yaml file providing arguments for data collection. (default: %(default)s)",
)

parser.add_argument(
    "--standalone",
    help="Whether SparrowRecorder runs alone or in conjunction with other Sparrow modules. (default: False)",
    action="store_true"
)

args = parser.parse_args()


def _merge_dict_recursive(base, augment):
    """
    _merge_dict_recursive Merge recursively two arbitrarily nested dictionaries such that only those leaves of 'base' are upated with the content of 'augment'
    for which the given path in 'augment' fully exists in 'base'.

    This function assumes that nodes in 'base' are only replaced, and 'augment' does not add new nodes.
    
    Args:
        base (dict): Base dictionary to update.
        augment (dict): dictionary to update 'base' with.
    """
    # basic assumption: augment is a sub-tree of base with unknown entry point.
    if isinstance(base, dict) and isinstance(augment, dict):

        for kb, vb in base.items():
            if kb in augment:
                # overlapping element branch found
                if isinstance(vb, dict) and isinstance(augment[kb], dict):
                    # follow branch if possible
                    _merge_dict_recursive(vb, augment[kb])
                else:
                    # assign if not
                    base[kb] = augment[kb]
            else:
                _merge_dict_recursive(vb, augment)  # find entrypoint
    else:
        pass  # not found and no dictionaries - pass


def _process_configs():
    """
    _process_configs _summary_

    _extended_summary_

    Returns:
        _type_: _description_
    """

    # get config files, then run
    default_filepath = Path(user_config_dir("iSparrowRecord")) / "default.yml"
    install_filepath = Path(user_config_dir("iSparrowRecord")) / "install.yml"

    # get install config for paths
    with open(install_filepath, "r") as cfgfile:
        sparrow_config = yaml.safe_load(cfgfile)

    # get default config
    with open(default_filepath, "r") as cfgfile:
        default_cfg = yaml.safe_load(cfgfile)

    custom_filepath = args.cfg

    if custom_filepath != "default":
        custom_filepath = Path(custom_filepath).expanduser()
        with open(custom_filepath, "r") as cfgfile:
            custom_cfg = yaml.safe_load(cfgfile)

    config = {**default_cfg, **custom_cfg}

    # dump complete config
    config["install"] = sparrow_config

    time = datetime.now()
    with open(Path(sparrow_config["Directories"]["data"].expanduser()) / f"config_{time.strftime("%y%m%d_%H%M%S")}.yml", "w") as outfile:
        yaml.safe_dump(config, outfile)

    return config 

def _process_runtime(config: dict); 
    run_until = config["Output"]["run_until"] if "run_until" in config["Output"] else None

    runtime = config["Output"]["runtime"] if "runtime" in config["Output"] else None

    if run_until is not None and runtime is not None:
        warnings.warn(
            "Warning, both 'runtime' and 'run_until' set. 'run_until' will be ignored"
        )
        run_until = None
        end_time = runtime
    elif run_until is not None:
        run_until = datetime.strptime(run_until, "%Y-%m-%d_%H:%M:%S")
        end_time = run_until
    elif runtime is not None:
        end_time = runtime
    else:
        end_time = None

    return end_time 

def main():
    """
    main Collect data until a certain datetime has been reached, 
    or for a certain amount of seconds or indefinitely. 
    Uses a yaml user supplied yaml file to update the default arguments and stores it together with the data.
    """
    runs_standalone = args.standalone

    if runs_standalone:
        print("setting up sparrow")
        set_up()

    config = _process_configs()

    end_time = _process_runtime(config)

    output = str(Path(config["Output"]["output_folder"]).expanduser())

    # create recorder, then start
    recorder = Recorder(output_folder=str(Path(output).expanduser()), **config["Recording"])

    if end_time is None:
        # run forever
        recorder.start(lambda x: False)

    if runtime is not None:
        begin_time = time.time()
        # run until time passed
        recorder.start(lambda x: time.time() > begin_time + end_time)

    if run_until is not None:
        # run until date is reached
        recorder.start(lambda x: datetime.now() > end_time)


if __name__ == "__main__":
    main()
