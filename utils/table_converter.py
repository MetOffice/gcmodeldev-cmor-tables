###############################################################################
# (c) Crown copyright 2022 Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
###############################################################################
"""
Factory style methods to help with loading / writing different flavours of variable
table files.
If called as a script will run the generator method to create a full set of legacy style tables from the latest /definitions/variable_tables/*.json
"""
import json
from datetime import datetime, date
from pathlib import Path
from typing import Union

from utils.entities import CmorVariable, VariableTable, VariableTableHeader

INDENT = 2


def load_legacy_variable_table(file_path: Union[Path, str]) -> VariableTable:
    """
    Load a legacy format JSON and translate into a Variable Table
    :param file_path: filepath to open as Path or string
    :return: VariableTable object loaded from file
    """
    with open(file_path, "r") as source_file:
        json_obj = json.load(source_file)
        # process the header
        json_header = json_obj['Header']
        # non iso date format
        json_header['table_date'] = datetime.strptime(json_header['table_date'], "%d %B %Y").date()
        # blank values
        for optional in ['missing_value', 'int_missing_value', 'approx_interval']:
            if json_header[optional] is "":
                del json_header[optional]
        # split list and re-case conventions to match rest
        json_header['conventions'] = json_header.pop('Conventions').split(" ")
        # blank values AND split array if present
        if "generic_levels" in json_header:
            if json_header['generic_levels'] == "":
                del json_header['generic_levels']
            else:
                json_header['generic_levels'] = json_header['generic_levels'].split(" ")
        # now have a clean array to convert to a header
        header = VariableTableHeader(**json_header)
        variable_table = VariableTable(header=header)

        # repeat above for each record...
        for variable_id, row in json_obj["variable_entry"].items():
            # move the ID into the record from the dictionary key
            row['id'] = variable_id
            # array splitting
            row['dimensions'] = row['dimensions'].split(" ")
            row['modeling_realm'] = row['modeling_realm'].split(" ")
            # optional floats - convert numeric strings into numbers!
            for key in ["valid_min", "valid_max", "ok_min_mean_abs", "ok_max_mean_abs"]:
                if row[key] == "":
                    del row[key]
                else:
                    row[key] = float(row[key])
            # generate variable object and add it to the table
            cmor_variable = CmorVariable(**row)
            variable_table.variable_entry.append(cmor_variable)
        return variable_table


def load_variable_table(file_path: Union[Path, str]) -> VariableTable:
    """
    This doesn't really need wrapping but it keeps a consistent interface!
    :param file_path: Path of file to load as Path or string
    :return: VariableTable object loaded from file
    """
    return VariableTable.parse_file(file_path)


def save_legacy_variable_table(table: VariableTable, output_location: str):
    """
    Save VariableTable in legacy format - will create / overwrite location
    :param table: VariableTable to save
    :param output_location: string - file to output
    :return: None
    """
    # start with a dictionary version of object - note nested are not yet converted
    table_dict = dict(table)
    # recase header
    table_dict['Header'] = dict(table_dict.pop('header'))
    # implode arrays, format dates and convert everything else to strings
    for key, value in table_dict['Header'].items():
        if isinstance(value, list):
            table_dict['Header'][key] = " ".join(table_dict['Header'][key])
        elif isinstance(value, date):
            table_dict['Header'][key] = table_dict['Header'][key].strftime("%d %B %Y")
        else:
            table_dict['Header'][key] = str(table_dict['Header'][key])
    # recase conventions
    table_dict['Header']['Conventions'] = table_dict['Header'].pop('conventions')
    # move variable entry to temporary location whilst building up new dictionary
    table_dict['variable_entry_list'] = table_dict.pop('variable_entry')
    table_dict['variable_entry'] = {}
    # reformat each variable record
    for variable in table_dict['variable_entry_list']:
        # create the record in the dictionary
        table_dict['variable_entry'].update({variable.id: dict(variable)})
        # format dates, squish lists, convert to string and handle Nones
        for key, value in table_dict['variable_entry'][variable.id].items():
            if isinstance(value, list):
                table_dict['variable_entry'][variable.id][key] = " ".join(
                    table_dict['variable_entry'][variable.id][key])
            elif isinstance(value, date):
                table_dict['variable_entry'][variable.id][key] = table_dict['variable_entry'][variable.id][key].format(
                    "%d %B %Y")
            elif value is None:
                table_dict['variable_entry'][variable.id][key] = ""
            else:
                table_dict['variable_entry'][variable.id][key] = str(table_dict['variable_entry'][variable.id][key])
        # remove the ID - it's now the key not a record
        del table_dict['variable_entry'][variable.id]['id']
    # remove temporary list
    del table_dict['variable_entry_list']
    # and finally save it!
    with open(output_location, "w") as file:
        json.dump(table_dict, file, indent=INDENT)


def save_variable_table(table: VariableTable, output_location: str):
    """
    create / overwrite table to location
    :param table: VariableTable to save
    :param output_location: string - file location to save to
    :return: None
    """
    with open(output_location, "w") as file:
        file.write(table.json(indent=INDENT, exclude_none=True))


def generate_new_from_legacy():
    """
    Iterates through all legacy definitions in "/tables/" and
    overwrites / creates new style definitions in /definitions/variable_tables/
    :return:
    """
    root = Path(__file__).parent.parent
    # find
    files = root.joinpath("tables").glob("*.json")
    # iterate
    for path in files:
        # process file name to get new table file name
        new_filename = path.stem.split("_")[-1]
        new_path = root.joinpath("definitions", "variable_tables", f"{new_filename}.json")
        # load from old format, save to new
        loaded = load_legacy_variable_table(path)
        save_variable_table(loaded, new_path)


def generate_legacy_from_new():
    """
    Generates legacy style tables based on latest variable_tables definitions
    Output to /legacy_tables
    Ensures new updates are cascaded into a legacy format
    :return:
    """
    root = Path(__file__).parent.parent
    files = root.joinpath("definitions", "variable_tables").glob("*.json")
    for path in files:
        new_filename = path.stem
        new_path = root.joinpath("legacy_tables", f"GCModelDev_{new_filename}.json")
        loaded = load_variable_table(path)
        save_legacy_variable_table(loaded, new_path)


# generate_new_from_legacy()

if __name__ == '__main__':
    generate_legacy_from_new()
