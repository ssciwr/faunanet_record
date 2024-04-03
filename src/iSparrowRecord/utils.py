import yaml
from pathlib import Path
from platformdirs import user_config_dir
from datetime import datetime
import warnings


def merge_dict_recursive(base, augment):
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
                    merge_dict_recursive(vb, augment[kb])
                else:
                    # assign if not
                    base[kb] = augment[kb]
            else:
                merge_dict_recursive(vb, augment)  # find entrypoint
    else:
        pass  # not found and no dictionaries - pass


def process_configs(custom_filepath: str):
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

    if custom_filepath != "default":
        custom_filepath = Path(custom_filepath).expanduser()
        with open(custom_filepath, "r") as cfgfile:
            custom_cfg = yaml.safe_load(cfgfile)

    config = {**default_cfg, **custom_cfg}

    # dump complete config
    config["install"] = sparrow_config

    time = datetime.now().strftime("%y%m%d_%H%M%S")
    with open(
        Path(sparrow_config["Directories"]["data"].expanduser()) / f"config_{time}.yml",
        "w",
    ) as outfile:
        yaml.safe_dump(config, outfile)

    return config


def process_runtime(config: dict):
    """
    _process_runtime _summary_

    _extended_summary_

    Args:
        config (dict): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    run_until = (
        config["Output"]["run_until"] if "run_until" in config["Output"] else None
    )

    runtime = config["Output"]["runtime"] if "runtime" in config["Output"] else None

    if run_until is not None and runtime is not None:
        warnings.warn(
            "Warning, both 'runtime' and 'run_until' set. 'run_until' will be ignored"
        )
        run_until = None
        return runtime
    elif run_until is None and runtime is None:
        raise ValueError("'run_until' and 'runtime' must not both be None.")
        return None
    elif run_until is not None:
        run_until = datetime.strptime(run_until, "%Y-%m-%d_%H:%M:%S")
        return run_until
    elif runtime is not None:
        return runtime
    else:
        return None
