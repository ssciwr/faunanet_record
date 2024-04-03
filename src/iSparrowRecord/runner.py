import yaml
from pathlib import Path
from platformdirs import user_config_dir
from datetime import datetime
import warnings
import time

from iSparrowRecord.utils import update_dict_recursive
from iSparrowRecord.audio_recording import Recorder


class Runner:
    """
    Class that runs data collection.

    Attributes:
    -----------
    config (dict): Configuration parameters for data collection
    end_time (int or datetime): Limit for how long or until when to collect data
    recorder (iSparroRecord.Recorder): Recorder to collect data. See iSparrow.Recorder documentation

    Methods:
    --------
    output Get the output data folder
    run Run data collection
    """

    def _process_configs(self, custom_cfg: dict) -> dict:
        """
        _process_configs _summary_

        Args:
            custom_cfg (dict): _description_

        Returns:
            dict: _description_
        """

        # get config files, then run. Their existence is guaranteed by the install
        default_filepath = Path(user_config_dir("iSparrowRecord")) / "default.yml"

        install_filepath = Path(user_config_dir("iSparrowRecord")) / "install.yml"

        # get install config for paths
        with open(install_filepath, "r") as cfgfile:
            sparrow_config = yaml.safe_load(cfgfile)

        for k, v in sparrow_config["Directories"].items():
            sparrow_config["Directories"][k] = str(Path(v).expanduser())

        # get default config
        with open(default_filepath, "r") as cfgfile:
            default_cfg = yaml.safe_load(cfgfile)

        update_dict_recursive(default_cfg, custom_cfg)

        # dump complete config
        default_cfg["Install"] = sparrow_config

        return default_cfg

    def _process_runtime(self, config: dict):
        """
        _process_runtime Prcoess the runtime limit as a precondition for collecting data.

        Args:
            config (dict): Config containing 'runtime' or 'run_until' data nodes

        Returns:
            int or datetime or None: If 'runtime' is given: the number of seconds to collect data. If 'run_until' is given: the timestamp (accurate to the second) until which data shall be collected. If none of both is given: None, meaning data collection runs indefinitely
        """
        if "run_until" in config:
            run_until = config["run_until"]
        else:
            run_until = None

        if "runtime" in config:
            runtime = config["runtime"]
        else:
            runtime = None

        if run_until is not None and runtime is not None:
            warnings.warn(
                "Warning, both 'runtime' and 'run_until' set. 'run_until' will be ignored"
            )
            run_until = None
            return runtime

        elif run_until is None and runtime is None:
            return None

        elif run_until is not None and runtime is None:
            run_until = datetime.strptime(run_until, "%Y-%m-%d_%H:%M:%S")
            return run_until

        else:
            return runtime

    def __init__(self, custom_config: dict = {}, dump_config: bool = False):
        """
        __init__ Create a new 'Runner' instance. A custom configpath can be supplied to update the default config with.
                 Merges the updated config with the installation info and dumps everything to the same folder where
                 the data is recorded to.
        Args:
            custom_config (dict, optional): A custom configuration dictionary containing key-value pairs that correspond to arguments used by this class or by the Recorder. Defaults to {}.
            dump_config (bool, optional): Wether to write the full config file to disk together with the data. Defaults to False.
        """

        self.config = self._process_configs(custom_config)

        self.end_time = self._process_runtime(self.config["Output"])

        output = str(Path(self.config["Output"]["output_folder"]).expanduser())

        # dump the config alongside the data
        if dump_config:
            time = datetime.now().strftime("%y%m%d_%H%M%S")

            with open(
                Path(Path(output).expanduser()) / f"config_{time}.yml",
                "w",
            ) as outfile:
                yaml.safe_dump(self.config, outfile)

        # create recorder, then start
        self.recorder = Recorder(
            output_folder=str(Path(output).expanduser()), **self.config["Recording"]
        )

    @property
    def output(self) -> str:
        """
        output Get the absolute path the data is recorded to

        Returns:
            str: Absolute path the data is recorded to
        """
        return self.recorder.output_folder

    def run(self):
        """
        run Collect data until a certain datetime has been reached,
        or for a certain amount of seconds or indefinitely.
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

    def stop(self):
        """
        stop Stop the data collection process

        """
        self.recorder.stop()
