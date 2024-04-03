import yaml
from pathlib import Path
from platformdirs import user_config_dir
from datetime import datetime
import warnings
from iSparrowRecord import Recorder
import time


class Runner:

    def update_dict_recursive(self, base, update):
        """
        _update_dict_recursive Merge recursively two arbitrarily nested dictionaries such that only those leaves of 'base' are upated with the content of 'update'
        for which the given path in 'update' fully exists in 'base'.

        This function assumes that nodes in 'base' are only replaced, and 'update' does not add new nodes.

        Args:
            base (dict): Base dictionary to update.
            update (dict): dictionary to update 'base' with.
        """
        # basic assumption: update is a sub-tree of base with unknown entry point.
        if isinstance(base, dict) and isinstance(update, dict):

            for kb, vb in base.items():
                if kb in update:
                    # overlapping element branch found
                    if isinstance(vb, dict) and isinstance(update[kb], dict):
                        # follow branch if possible
                        self.update_dict_recursive(vb, update[kb])
                    else:
                        # assign if not
                        base[kb] = update[kb]
                else:
                    self.update_dict_recursive(vb, update)  # find entrypoint
        else:
            pass  # not found and no dictionaries - pass

    def process_configs(self, custom_filepath: str):
        """
        _process_configs _summary_

        _extended_summary_

        Returns:
            _type_: _description_
        """

        # get config files, then run. Their existence is guaranteed by the install
        default_filepath = Path(user_config_dir("iSparrowRecord")) / "default.yml"
        
        install_filepath = Path(user_config_dir("iSparrowRecord")) / "install.yml"

        # get install config for paths
        with open(install_filepath, "r") as cfgfile:
            sparrow_config = yaml.safe_load(cfgfile)

        # get default config
        with open(default_filepath, "r") as cfgfile:
            default_cfg = yaml.safe_load(cfgfile)

        custom_filepath = Path(custom_filepath).expanduser()
        with open(custom_filepath, "r") as cfgfile:
            custom_cfg = yaml.safe_load(cfgfile)

        self.update_dict_recursive(default_cfg, custom_cfg)

        # dump complete config
        default_cfg["Install"] = sparrow_config

        time = datetime.now().strftime("%y%m%d_%H%M%S")
        with open(
            Path(Path(sparrow_config["Directories"]["data"]).expanduser())
            / f"config_{time}.yml",
            "w",
        ) as outfile:
            yaml.safe_dump(default_cfg, outfile)

        return default_cfg

    def process_runtime(self, config: dict):
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
            raise ValueError(
                "'run_until' or 'runtime' must be given in 'Output' node of config."
            )
            return None

        elif run_until is not None:
            run_until = datetime.strptime(run_until, "%Y-%m-%d_%H:%M:%S")
            return run_until

        elif runtime is not None:
            return runtime

    def __init__(self, custom_configpath: str):
        """
        __init__ _summary_

        Args:
            custom_configpath (str): _description_
        """

        self.config = self.process_configs(custom_configpath)

        self.end_time = self.process_runtime(self.config)

        output = str(Path(self.config["Output"]["output_folder"]).expanduser())

        # create recorder, then start
        self.recorder = Recorder(
            output_folder=str(Path(output).expanduser()), **self.config["Recording"]
        )

    def run(self):
        """
        run Collect data until a certain datetime has been reached,
        or for a certain amount of seconds or indefinitely.
        Uses a yaml user supplied yaml file to update the default arguments and stores it together with the data.
        """

        if self.end_time is None:
            # run forever
            self.recorder.start(lambda x: False)

        if isinstance(self.end_time, int):
            begin_time = time.time()
            # run until time passed
            self.recorder.start(lambda x: time.time() > begin_time + self.end_time)

        if isinstance(self.end_time, datetime):
            # run until date is reached
            self.recorder.start(lambda x: datetime.now() > self.end_time)

    @classmethod
    def from_cfg(cls, cfg_node: dict):
        pass
