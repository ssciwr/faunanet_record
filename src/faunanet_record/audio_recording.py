from abc import ABC, abstractmethod
from pathlib import Path

RECORDER = {}


class RecorderBase(ABC):
    """
    RecorderBase Abstract base class for any audio recording functionality that shall be used with faunanet.


    Methods:
    --------
    start(stop_condition = lambda x: False):  Abstract method that needs to be implemented by derived class. Should make the caller start generate data. Runs until 'stop_condition(self)' returns True.
    stream_audio(): Abstract method that needs to be implemented by derived class. Should get a chunk of recorded data corresponding to 'length_in_s' seconds of recording.
    stop(): Abstract method that needs to be implemented by derived class. Should stop the recorder's data collecting process and release resources.
    """

    def __init__(
        self,
        output_folder: str = None,
        length_s: int = 15,
        sample_rate: int = 32000,
        file_type: str = "wave",
        channels: int = 1,
        mode: str = "record",
        num_format: int = None,
    ):
        """
        __init__ Create a new instance. This class should not be instantiated on its own, but only as part of a child class.


        Args:
            output_folder (str, optional): Output folder to write files to. Defaults to None.
            length_s (int, optional): Lenght of each recorded chunk of data in seconds. Defaults to 15.
            sample_rate (int, optional): Sample rate of recording. Defaults to 32000.
            file_type (str, optional): File type to save files as. Defaults to "wav".
            channels (int, optional): Number of used channels for recording. Defaults to 1.
            mode (str, optional): Mode of operation. Can be 'record' or 'stream'. Defaults to "record".
            num_format (optional): Numerical format for each sample that is recorded. Depends on the library used for implementing the recording process. Defaults to None.

        Raises:
            ValueError: _description_
        """
        self.length_in_s = length_s
        self.sample_rate = sample_rate
        self.output_folder = str(Path(output_folder).expanduser())
        self.file_type = file_type
        self.channels = channels
        self.num_format = num_format

        if mode not in ["record", "stream"]:
            raise ValueError("Unknown mode. Must be 'record', 'stream'")

        self.mode = mode

    @property
    def output(self):
        return str(Path(self.output_folder).absolute())

    @abstractmethod
    def is_running(self):
        pass

    @abstractmethod
    def _close(self):
        pass

    @abstractmethod
    def start(self, stop_condition: callable = lambda x: False):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def stream_audio(self):
        pass


def register_recorder(key: str, recorder_class: RecorderBase):
    """
    register_recorder Register a new recorder class to be used with faunanet.


    Args:
        key (str): Key to be used to identify the recorder class.
        recorder_class (RecorderBase): Class to be registered as a recorder.
    """
    RECORDER[key] = recorder_class
