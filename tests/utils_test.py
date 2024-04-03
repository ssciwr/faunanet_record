# from ..main import main
from iSparrowRecord import update_dict_recursive, process_configs, process_runtime

from pathlib import Path
from datetime import datetime
import pytest


def test_dict_merging():
    base = {
        "a": {"x": 3, "y": {"l": 2, "k": "hello"}},
        "b": {"p": "c", "d": {"v": 5, "w": 6}},
    }

    update = {
        "y": {"l": 8},
        "b": {
            "d": {
                "w": -5,
            }
        },
    }

    update_dict_recursive(base, update)

    # stuff not in 'custom_cfg' must stay, other stuff must go
    assert base["a"]["x"] == 3
    assert base["a"]["y"]["l"] == 8
    assert base["a"]["y"]["k"] == "hello"
    assert base["b"]["p"] == "c"
    assert base["b"]["d"]["v"] == 5
    assert base["b"]["d"]["w"] == -5

    # update with oneself and with empty dict do nothing
    base = {
        "a": {"x": 3, "y": {"l": 2, "k": "hello"}},
        "b": {"p": "c", "d": {"v": 5, "w": 6}},
    }

    update_dict_recursive(base, base)
    assert base["a"]["x"] == 3
    assert base["a"]["y"]["l"] == 2
    assert base["a"]["y"]["k"] == "hello"
    assert base["b"]["p"] == "c"
    assert base["b"]["d"]["v"] == 5
    assert base["b"]["d"]["w"] == 6

    update_dict_recursive(base, {})
    assert base["a"]["x"] == 3
    assert base["a"]["y"]["l"] == 2
    assert base["a"]["y"]["k"] == "hello"
    assert base["b"]["p"] == "c"
    assert base["b"]["d"]["v"] == 5
    assert base["b"]["d"]["w"] == 6

    # paths not in 'base' must be ignored
    update = {
        "y": {"l": 8},
        "b": {
            "s": {
                "k": -5,
            }
        },
    }

    update_dict_recursive(base, update)
    assert base["a"]["x"] == 3
    assert base["a"]["y"]["l"] == 8
    assert base["a"]["y"]["k"] == "hello"
    assert base["b"]["p"] == "c"
    assert base["b"]["d"]["v"] == 5
    assert "s" not in base["b"]


def test_config_processing():
    cfgdir = Path(__file__).resolve().parent.parent / Path("config")

    cfg = process_configs(cfgdir / "custom_example.yml")
    assert cfg["Output"]["runtime"] == 20
    assert cfg["Output"]["output_folder"] == "~/iSparrow_data"
    assert cfg["Recording"]["sample_rate"] == 32000
    assert cfg["Recording"]["length_s"] == 10
    assert cfg["Recording"]["channels"] == 1
    assert cfg["Recording"]["mode"] == "record"

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
    assert "install" in cfg


def test_condition_creation():
    cfgdir = Path(__file__).resolve().parent.parent / Path("config")

    cfg = process_configs(cfgdir / "custom_example.yml")

    end_time = process_runtime(cfg)

    assert end_time == 20

    del end_time
    cfg["Output"]["run_until"] = "2024-04-04_12:05:24"

    with pytest.warns(UserWarning) as warning_info:
        end_time = process_runtime(cfg)

    assert (
        str(warning_info[0].message)
        == "Warning, both 'runtime' and 'run_until' set. 'run_until' will be ignored"
    )

    assert end_time == 20

    del cfg["Output"]["runtime"]
    end_time = process_runtime(cfg)

    assert end_time == datetime.strptime("2024-04-04_12:05:24", "%Y-%m-%d_%H:%M:%S")

    del cfg["Output"]["run_until"]

    with pytest.raises(ValueError) as exc_info:
        end_time == process_runtime(cfg)

    assert (
        str(exc_info.value)
        == "'run_until' or 'runtime' must be given in 'Output' node of config."
    )

    cfg["Output"]["runtime"] = 20
    end_time = process_runtime(cfg)
    assert end_time == 20
