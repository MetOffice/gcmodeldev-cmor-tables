# (C) British Crown Copyright 2021-2022, Met Office.
# Please see LICENSE.rst for license details.
import json

from typing import Any, Dict, Tuple


def read_json(json_file: str) -> Dict[str, Any]:
    """
    Read the JSON file ``json_file``.

    Parameters
    ----------
    json_file: str
        The name of file to read.

    Returns
    -------
    : dict
        Data read from ``json_file``.
    """
    with open(json_file, 'r') as file_handle:
        data = json.load(file_handle)
    return data


def write_json(json_file: str, data: Dict[str, Any], indent: int = 2, sort_keys: bool = True,
               separators: Tuple[str, str] = (',', ':'), **kwargs: Any):
    """
    Write ``data`` to a JSON file with the name ``json_file``.

    Parameters
    ----------
    json_file: str
        The name of file to write to.
    data: dict
        Data to write to ``json_file``.
    indent: int, optional
        number of characters to indent
    sort_keys: bool, optional
        Sort keys in output file
    separators: tuple
        Specifies the separators in the json file between items and key-values. The default is ``(', ', ': ')``.
    **kwargs
        Other keyword arguments to pass to json.dump
    """
    with open(json_file, 'w') as file_handle:
        json.dump(data, file_handle, indent=indent, sort_keys=sort_keys, separators=separators, **kwargs)
