import yaml
from pathlib import Path
import ast


def update_dict_recursive(base, update):
    """
    _update_dict_recursive Merge recursively two arbitrarily nested dictionaries such that only those leaves of 'base' are upated with the content of 'update'
    for which the given path in 'update' fully exists in 'base'.

    This function assumes that nodes in 'base' are only replaced, and 'update' does not add new nodes.

    Args:
        base (dict): Base dictionary to update.
        update (dict): dictionary to update 'base' with.
    """
    # basic assumption: update is a sub-tree of base with unknown entry point.
    if isinstance(base, dict) and isinstance(update, dict):

        for kb, vb in base.items():
            if kb in update:
                # overlapping element branch found
                if isinstance(vb, dict) and isinstance(update[kb], dict):
                    # follow branch if possible
                    update_dict_recursive(vb, update[kb])
                else:
                    # assign if not
                    base[kb] = update[kb]
            else:
                update_dict_recursive(vb, update)  # find entrypoint
    else:
        pass  # not found and no dictionaries - pass


def read_yaml(path: str):
    """
    read_yaml Read the yaml basic config file for iSparrow from path.
            It contains the install directory, data directory and other things used
            by iSparrow internally.

    Args:
        path (str): Path to the yaml base config.

    Returns:
        dict: read base config file.
    """

    if Path(path).exists() is False:
        raise FileNotFoundError(f"The folder {path} does not exist")

    with open(Path(path)) as file:
        cfg = yaml.safe_load(file)

    return cfg


def dict_from_string(dict_repr: str):
    dictionary = None
    try:
        # Convert the string representation of dictionary to a dictionary object
        dictionary = ast.literal_eval(dict_repr)
        if not isinstance(dictionary, dict):
            raise ValueError("Invalid dictionary format")
    except ValueError as e:
        print("Error when converting dictionary string")
        raise e

    return dictionary
