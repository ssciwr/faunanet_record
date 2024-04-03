from iSparrowRecord import Runner
from iSparrowRecord import utils
from pathlib import Path
from datetime import datetime
import pytest


def test_config_processing(install, folders):
    _, _, cfgdir = folders
    config = utils.read_yaml(Path(cfgdir) / "custom_example.yml")

    runner = Runner(config, dump_config=True)

    cfg = runner._process_configs(config)
    assert cfg["Output"]["runtime"] == 8
    assert cfg["Output"]["output_folder"] == "~/iSparrow_data"
    assert cfg["Recording"]["sample_rate"] == 32000
    assert cfg["Recording"]["length_s"] == 4
    assert cfg["Recording"]["channels"] == 1
    assert cfg["Recording"]["mode"] == "record"
    assert cfg["Install"]["Directories"]["home"] == str(Path.home() / "iSparrow")
    assert cfg["Install"]["Directories"]["data"] == str(Path.home() / "iSparrow_data")
    assert cfg["Install"]["Directories"]["output"] == str(
        Path.home() / "iSparrow_output"
    )

    part_of_name = datetime.now().strftime("%y%m%d_%H%M")

    # check that yaml is written to data folder
    yaml_counter = 0
    for filename in (Path.home() / Path("iSparrow_data")).iterdir():
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

    runner = Runner(config)

    cfg = runner._process_configs(config)

    end_time = runner._process_runtime(cfg["Output"])

    assert end_time == 8

    del end_time
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


def test_runner_creation(install, folders):
    _, _, cfgdir = folders

    config = utils.read_yaml(Path(cfgdir) / "custom_example.yml")

    runner = Runner(config)

    assert runner.end_time == 8
    assert "Install" in runner.config
    assert "Output" in runner.config
    assert "Recording" in runner.config
    assert runner.output == str(Path("~/iSparrow_data").expanduser())
    assert runner.recorder.is_running is False  # not yet running
