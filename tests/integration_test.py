# from ..main import main
from iSparrowRecord import merge_dict_recursive, process_configs, process_runtime

from pathlib import Path
import yaml


def test_dict_merging():

    merge_dict_recursive(base, update)

    # stuff not in 'custom_cfg' must stay, other stuff must go
    assert base["Output"]["runtime"] == 20
    assert base["Output"]["output_folder"] == "~/iSparrow_data"
    assert base["Recording"]["sample_rate"] == 32000
    assert base["Recording"]["length_s"] == 10
    assert base["Recording"]["channels"] == 1
    assert base["Recording"]["mode"] == "record"


def test_config_processing():
    cfgdir = Path(__file__).resolve().parent.parent / Path("config")

    cfg = process_configs(cfgdir / "custom_example.yml")
    assert cfg["Output"]["runtime"] == 20
    assert cfg["Output"]["output_folder"] == "~/iSparrow_data"
    assert cfg["Recording"]["sample_rate"] == 32000
    assert cfg["Recording"]["length_s"] == 10
    assert cfg["Recording"]["channels"] == 1
    assert cfg["Recording"]["mode"] == "record"


def test_condition_creation():
    pass


def test_main_func():
    pass
