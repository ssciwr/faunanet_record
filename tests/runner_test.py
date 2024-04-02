from iSparrowRecord import RecordingRunner
from datetime import datetime
from pathlib import Path
from pyaudio import paInt16
import pytest
from copy import deepcopy


def test_runner_creation(folders, audio_recorder_fx):
    _, DATA, _ = folders

    _, cfg = audio_recorder_fx

    with pytest.warns(UserWarning) as warning_info:
        runner = RecordingRunner.from_cfg(
            cfg["Data"]["Output"], cfg["Data"]["Recording"]
        )

    assert (
        str(warning_info[0].message)
        == "Warning, both 'runtime' and 'run_until' set. 'run_until' will be ignored"
    )

    assert runner.output_folder == DATA
    assert runner.runtime == 9
    assert runner.run_until is None
    assert runner.end_time == 9  # run_until ignored when both given

    assert runner.recorder.chunk_size == 1000
    assert runner.recorder.output_folder == str(Path.home() / "iSparrow_data")
    assert runner.recorder.length_in_s == 3
    assert runner.recorder.sample_rate == 48000
    assert runner.recorder.file_type == "wave"
    assert runner.recorder.channels == 1
    assert runner.recorder.mode == "record"
    assert runner.recorder.num_format == paInt16

    cfg_endless = deepcopy(cfg)

    del cfg_endless["Data"]["Output"]["run_until"]
    del cfg_endless["Data"]["Output"]["runtime"]

    runner_endless = RecordingRunner.from_cfg(
        cfg_endless["Data"]["Output"], cfg_endless["Data"]["Recording"]
    )

    assert runner_endless.runtime is None
    assert runner_endless.run_until is None
    assert runner_endless.end_time is None

    cfg_timed = deepcopy(cfg)
    del cfg_timed["Data"]["Output"]["run_until"]

    runner_timed = RecordingRunner.from_cfg(
        cfg_timed["Data"]["Output"], cfg_timed["Data"]["Recording"]
    )

    assert runner_timed.runtime == 9
    assert runner_timed.run_until is None
    assert runner_timed.end_time == 9

    cfg_dated = deepcopy(cfg)
    print(cfg_dated)
    del cfg_dated["Data"]["Output"]["runtime"]

    runner_dated = RecordingRunner.from_cfg(
        cfg_dated["Data"]["Output"], cfg_timed["Data"]["Recording"]
    )

    assert runner_dated.runtime is None
    assert runner_dated.run_until == datetime(2024, 4, 2, 14, 35, 1)
    assert runner_dated.end_time == datetime(2024, 4, 2, 14, 35, 1)


def test_runner_usage(folders, audio_recorder_fx):
    _, DATA, _ = folders

    _, cfg = audio_recorder_fx

    runner = RecordingRunner.from_cfg(cfg["Data"]["Output"], cfg["Data"]["Recording"])

    runner.run()

    # read folder and check that everything works fine
    num_file = 0
    for item in Path(DATA).iterdir():
        assert item.suffix == ".wav"
        num_file += 1

    assert num_file == 3


