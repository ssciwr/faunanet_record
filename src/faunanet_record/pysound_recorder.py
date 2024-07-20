from .audio_recording import RecorderBase, register_recorder
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import wave


class SoundDeviceRecorder(RecorderBase):
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
        pass

    def _close(self):
        pass

    def start(self, stop_condition: callable = lambda x: False):
        pass

    def stop(self):
        pass

    def stream_audio(self):
        pass

    @classmethod
    def from_cfg(cls, cfg: dict):
        pass


register_recorder("sounddevice", SoundDeviceRecorder)
