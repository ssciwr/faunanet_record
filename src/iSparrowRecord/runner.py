from pathlib import Path
from datetime import datetime
import time
import warnings
from copy import deepcopy
from iSparrowRecord import Recorder


class RecordingRunner:
    """
    RecordingRunner Wrapper around the Recorder class that allows data collection for a specified time (in seconds) or until a specified timestamp (format: yyyy-mm-dd_hh:MM:ss)

    Methods:
    --------
    run: Run the recorder for a specified number of seconds or until a specified timestamp
    from_cfg (classmethod): Build a new instance of this class from a dictionary, usually obtained by reading a yaml config.
    output_folder: get the output folder used to put the wave files to

    """

    def __init__(
        self,
        output_folder: str,
        runtime: int = None,
        run_until: datetime = None,
        recorder_kwargs: dict = {
            "sample_rate": 48000,
            "length_s": 3,
            "channels": 1,
        },
    ):
        """
        __init__ Create a new RecordingRunner. If both 'runtime' and 'run_until' are 'None', data collection runs indefinitely.

        Args:
            output_folder (str): Folder to save audio files to
            runtime (int, optional): Time for which data collection should run. Defaults to None.
            run_until (datetime, optional): Time until the data collection should run. Ignored if 'runtime' is given. Defaults to None.
        """
        self.runtime = runtime

        self.run_until = run_until

        if self.run_until is not None and self.runtime is not None:
            warnings.warn(
                "Warning, both 'runtime' and 'run_until' set. 'run_until' will be ignored"
            )
            self.run_until = None
            self.end_time = self.runtime
        elif self.run_until is not None:
            self.end_time = self.run_until
        elif self.runtime is not None:
            self.end_time = self.runtime
        else:
            self.end_time = None

        self.recorder = Recorder(
            output_folder=str(Path(output_folder).expanduser()), **recorder_kwargs
        )

    @property
    def output_folder(self) -> str:
        """
        output_folder Get the folder where the recorded audio files are written to.


        Returns:
            str: Path to the data folder.
        """
        return self.recorder.output_folder

    def run(self):
        """
        run Run collection of audio data. Data is saved into wav files by default.

        """
        if self.end_time is None:
            # run forever
            self.recorder.start(lambda x: False)

        if self.runtime is not None:
            begin_time = time.time()
            # run until time passed
            self.recorder.start(lambda x: time.time() > begin_time + self.end_time)

        if self.run_until is not None:
            # run until date is reached
            self.recorder.start(lambda x: datetime.now() > self.end_time)

    @classmethod
    def from_cfg(cls, run_config: dict, recorder_config: dict):
        """
        from_cfg Build a new RecordingRunner instance from dictionaries, typically obtained from reading yaml files.

        Args:
            run_config (dict): Config node for the Runner. Must contain keyword arguments used by this class.
            recorder_config (dict): Config node for the underlyin `Recorder` instance.

        Raises:
            e: When datetime format is not yyyy-mm-dd_hh:MM:ss or anything goes wrong while converting string timestamp to datetime.

        Returns:
            RecordingRunner: New `RecordingRunner` instance.
        """
        run_config = deepcopy(run_config)

        recorder_config = deepcopy(recorder_config)

        if recorder_config is None:
            # warn when there is no recorder config that we use defaults. These may not be
            # suitable for all purposes
            warnings.Warn(
                "No recorder configuration node given, using default keyword arguments for recorder"
            )
            recorder_config = {}

        if "run_until" in run_config:
            try:
                run_config["run_until"] = datetime.strptime(
                    run_config["run_until"], "%Y-%m-%d_%H:%M:%S"
                )

            except Exception as e:
                print(
                    "The datetime string for the config node 'run_until' must adhere to the format 'yyyy-mm-dd_hh:MM:ss'"
                )
                raise e

        run_config["recorder_kwargs"] = recorder_config

        return cls(**run_config)
