import yaml
from pathlib import Path
from platformdirs import user_config_dir
from datetime import datetime, timedelta
import warnings
from time import sleep

from .audio_recording import Recorder
from .utils import update_dict_recursive


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

        default_cfg["Install"] = sparrow_config

        # README: make sure this is always last, such that the custom config can modify everything
        update_dict_recursive(default_cfg, custom_cfg)

        return default_cfg

    def _process_runtime(self, config: dict):
        """
        _process_runtime Prcoess the runtime limit as a precondition for collecting data.

        Args:
            config (dict): Config containing 'runtime' or 'run_until' data nodes

        Returns:
            int or datetime or None: If 'runtime' is given: the number of seconds to collect data.
                                    If 'run_until' is given: the timestamp (accurate to the second)
                                    until which data shall be collected. If none of both is given:
                                    None, meaning data collection runs indefinitely.
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

    def _define_starting_time(self) -> datetime:
        """
        _define_starting_time Get next full second of the starting time


        Returns:
            datetime: current time rounded to the NEXT full second
        """
        return (datetime.now() + timedelta(seconds=1)).replace(microsecond=0)

    def __init__(self, custom_config: dict = {}):
        """
        __init__ Create a new 'Runner' instance. A custom configpath can be supplied to update the default config with.
                 Merges the updated config with the installation info and dumps everything to the same folder where
                 the data is recorded to.
        Args:
            custom_config (dict, optional): A custom configuration dictionary containing key-value pairs that correspond to arguments used by this class or by the Recorder. Defaults to {}.
            suffix (str, optional): Suffix to add to run folder
        """

        self.config = self._process_configs(custom_config)

        # make new folder for data dumping
        foldername = (
            datetime.now().strftime("%y%m%d_%H%M%S")
            + self.config["Output"]["data_folder_suffix"]
        )

        folderpath = (
            Path(self.config["Install"]["Directories"]["data"]).expanduser()
            / foldername
        )

        folderpath.mkdir()

        self.output_path = str(folderpath)

        # update config
        self.config["Output"]["output_folder"] = self.output_path

        # determine for how long the runner should collect data
        self.end_time = self._process_runtime(self.config["Output"])

        # dump the config alongside the data
        if self.config["Output"]["dump_config"] is True:
            time = datetime.now().strftime("%y%m%d_%H%M%S")

            with open(
                folderpath / f"config_{time}.yml",
                "w",
            ) as outfile:
                yaml.safe_dump(self.config, outfile)

        # create recorder
        self.recorder = Recorder(
            output_folder=str(folderpath), **self.config["Recording"]
        )

    def run(self):
        """
        run Collect data until a certain datetime has been reached,
        or for a certain amount of seconds or indefinitely. Recorded audio data
        is saved to .wav files in the given output folder.
        """

        if self.end_time is None:
            print("start collecting data indefinitely")
            # run forever
            self.recorder.start(lambda x: False)

        if isinstance(self.end_time, int):

            # run until time has passed
            print(
                "start collecting data for ",
                self.end_time,
                " seconds with ",
                self.recorder.length_in_s,
                "seconds per file",
            )

            start = self._define_starting_time()

            stop = (start + timedelta(seconds=self.end_time)).replace(microsecond=0)

            while datetime.now() < start:
                sleep(0.001)

            self.recorder.start(lambda x: datetime.now() >= stop)

        if isinstance(self.end_time, datetime):

            # run until date is reached
            print(
                "start collecting data until ",
                self.end_time,
                "with ",
                self.recorder.length_in_s,
                "seconds per file",
            )

            start = self._define_starting_time()

            while datetime.now() < start:
                sleep(0.01)

            self.recorder.start(lambda x: datetime.now() >= self.end_time)
