from iSparrowRecord import Runner
from iSparrowRecord import utils
from pathlib import Path
from datetime import datetime
import pytest


def test_config_processing(install, folders):
    _, _, cfgdir = folders
    config = utils.read_yaml(Path(cfgdir) / "custom_example.yml")

    runner = Runner(config)

    cfg = runner._process_configs(config)
    assert cfg["Output"]["runtime"] == 8
    assert cfg["Output"]["output_folder"] == "~/iSparrow_data"
    assert cfg["Recording"]["sample_rate"] == 32000
    assert cfg["Recording"]["length_s"] == 4
    assert cfg["Recording"]["channels"] == 1
    assert cfg["Recording"]["mode"] == "record"
    assert cfg["Install"]["Directories"]["data"] == str(Path.home() / "iSparrow_data")

    # test that the timestamp is correct at least to the minute. Seconds can be too short...
    part_of_name = datetime.now().strftime("%y%m%d_%H%M")

    # check that yaml is written to data folder
    yaml_counter = 0
    for filename in Path(runner.output_path).iterdir():
        if filename.suffix == ".yml":
            yaml_counter += 1

    assert yaml_counter == 1
    assert part_of_name in str(filename)

    assert "Output" in cfg
    assert "Recording" in cfg
    assert "Install" in cfg


def test_condition_creation(install, folders):
    _, _, cfgdir = folders

    config = utils.read_yaml(Path(cfgdir) / "custom_example.yml")

    # modify config with a suffix unique for this test case
    config["Output"]["data_folder_suffix"] = "_condition_creation"

    runner = Runner(config)

    cfg = runner._process_configs(config)

    end_time = runner._process_runtime(cfg["Output"])

    assert end_time == 8

    cfg["Output"]["run_until"] = "2024-04-04_12:05:24"

    with pytest.warns(UserWarning) as warning_info:
        end_time = runner._process_runtime(cfg["Output"])

    assert (
        str(warning_info[0].message)
        == "Warning, both 'runtime' and 'run_until' set. 'run_until' will be ignored"
    )

    assert end_time == 8

    del cfg["Output"]["runtime"]
    end_time = runner._process_runtime(cfg["Output"])

    assert end_time == datetime.strptime("2024-04-04_12:05:24", "%Y-%m-%d_%H:%M:%S")

    del cfg["Output"]["run_until"]
    end_time = runner._process_runtime(cfg["Output"])
    assert end_time is None

    cfg["Output"]["runtime"] = "inf"
    end_time = runner._process_runtime(cfg["Output"])
    assert end_time is None


def test_runner_creation(install, folders):
    _, _, cfgdir = folders

    config = utils.read_yaml(Path(cfgdir) / "custom_example.yml")
    # modify config with a suffix unique for this test case
    config["Output"]["data_folder_suffix"] = "_runner_creation"

    runner = Runner(config)

    assert runner.end_time == 8
    assert "Install" in runner.config
    assert "Output" in runner.config
    assert "Recording" in runner.config
    assert runner.output_path == str(
        Path("~/iSparrow_data").expanduser()
        / (datetime.now().strftime("%y%m%d_%H%M%S") + "_runner_creation")
    )
    assert runner.recorder.is_running is False  # not yet running
