from .audio_recording import RecorderBase, register_recorder
from pathlib import Path
import subprocess
import signal 

class AlsaRecorder(RecorderBase):
    """
    _summary_

    Parameters
    ----------
    RecorderBase : _type_
        _description_

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    ValueError
        _description_
    ValueError
        _description_
    """
    def _make_command_list(self):
        """
        _summary_

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        ValueError
            _description_
        """
        self.arecord_command_list = [
            "arecord",
            "-f",
            f"{self.num_format}",
            f"-c{self.channels}",
            f"-r{self.sample_rate}",
            "-t",
            f"{self.file_type}",
            "--max-file-time",
            f"{self.length_s}",
            "--use-strftime",
        ]

    def _close(self):
        """
        _summary_

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        ValueError
            _description_
        """
        self.stop()

    def _handle_process(self, stop_condition: callable = lambda x: False):
        """
        _summary_

        Parameters
        ----------
        stop_condition : _type_, optional
            _description_, by default lambdax:False

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        ValueError
            _description_
        """
        # FIXME: add handling of sigterm and sigkill
        while True: 
            if stop_condition(self):
                self.stop()

    def __init__(
        self,
        output_dir: str | None = None,
        length_s: int = 15,
        sample_rate: int = 32000,
        file_type: str = "wav",
        channels: int = 1,
        num_format: str = "S16_LE",
        stream_target: str | None = None,
    ):
        """
        _summary_

        Parameters
        ----------
        output_dir : str | None, optional
            _description_, by default None
        length_s : int, optional
            _description_, by default 15
        sample_rate : int, optional
            _description_, by default 32000
        file_type : str, optional
            _description_, by default "wav"
        channels : int, optional
            _description_, by default 1
        num_format : str, optional
            _description_, by default "S16_LE"
        stream_target : str | None, optional
            _description_, by default None

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        ValueError
            _description_
        """
        self.length_in_s = length_s
        self.num_format = num_format
        self.sample_rate = sample_rate
        self.file_type = file_type
        self.channels = channels
        self.stream_target = stream_target
        self.output_dir = output_dir
        self.is_running = True

        if self.output_dir is not None and self.stream_target is not None:  
            raise ValueError("Only one of output_dir or stream_target can be specified.")   

        self.arecord_command_list = self._make_command_list()

        if output_dir is not None:
            self.arecord_command_list.extend(["-d", output_dir])
        else:
            self.arecord_command_list.extend(["|", f"nc {stream_target}"])

        self.p = None


    def stream_audio(self, stop_condition: callable = lambda x: False) -> None:
        """
        _summary_

        Parameters
        ----------
        stop_condition : _type_, optional
            _description_, by default lambdax:False

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        self.p = subprocess.Popen(self.arecord_command_list)

        self.handle_process(stop_condition=stop_condition) 

    def start(self, stop_condition: callable = lambda x: False) -> None:
        """
        _summary_

        Parameters
        ----------
        stop_condition : _type_, optional
            _description_, by default lambdax:False

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        self.p = subprocess.Popen(self.arecord_command_list)

        self.handle_process(stop_condition=stop_condition)

    def stop(self):
        """
        _summary_

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        self.p.terminate()
        self.p.wait(timeout=15)
        print("timeout expired, killing arecord recorder process ")
        self.p.kill()



    @classmethod
    def from_cfg(cls, cfg: dict):
        """
        _summary_

        Parameters
        ----------
        cfg : dict
            _description_

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        if "output_dir" not in cfg["Output"]:
            raise ValueError(
                "Output folder must be given in config node for PyAudioRecorder."
            )

        directory = Path(cfg["Output"]["output_dir"]).expanduser()

        default = {
        "length_s": 15,
        "sample_rate": 32000,
        "file_type": "wav",
        "channels": 1,
        "num_format": "S16_LE",
        }

        cfg["Recording"] = default | cfg["Recording"] 

        return cls(directory, **cfg["Recording"])


register_recorder("alsa", AlsaRecorder)
