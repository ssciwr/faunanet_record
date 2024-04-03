from iSparrowRecord import utils


def test_dict_merging(install, folders):
    _, _, cfgdir = folders

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

    utils.update_dict_recursive(base, update)

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

    utils.update_dict_recursive(base, base)
    assert base["a"]["x"] == 3
    assert base["a"]["y"]["l"] == 2
    assert base["a"]["y"]["k"] == "hello"
    assert base["b"]["p"] == "c"
    assert base["b"]["d"]["v"] == 5
    assert base["b"]["d"]["w"] == 6

    utils.update_dict_recursive(base, {})
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

    utils.update_dict_recursive(base, update)
    assert base["a"]["x"] == 3
    assert base["a"]["y"]["l"] == 8
    assert base["a"]["y"]["k"] == "hello"
    assert base["b"]["p"] == "c"
    assert base["b"]["d"]["v"] == 5
    assert "s" not in base["b"]
