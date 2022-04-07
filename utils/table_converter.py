###############################################################################
# (c) Crown copyright 2022 Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
###############################################################################
import json
from datetime import datetime, date
from pathlib import Path

from utils.entities import CmorVariable, VariableTable, VariableTableHeader


def load_legacy_variable_table(file_path: str) -> VariableTable:
    with open(file_path, "r") as source_file:
        json_obj = json.load(source_file)
        json_header = json_obj['Header']
        json_header['table_date'] = datetime.strptime(json_header['table_date'], "%d %B %Y").date()
        for optional in ['missing_value', 'int_missing_value', 'approx_interval']:
            if json_header[optional] is "":
                del json_header[optional]
        json_header['conventions'] = json_header.pop('Conventions').split(" ")
        if "generic_levels" in json_header:
            if json_header['generic_levels'] == "":
                del json_header['generic_levels']
            else:
                json_header['generic_levels'] = json_header['generic_levels'].split(" ")
        header = VariableTableHeader(**json_header)
        variable_table = VariableTable(header=header)
        for variable_id, row in json_obj["variable_entry"].items():
            row['id'] = variable_id
            row['dimensions'] = row['dimensions'].split(" ")
            row['modeling_realm'] = row['modeling_realm'].split(" ")
            for key in ["valid_min", "valid_max", "ok_min_mean_abs", "ok_max_mean_abs"]:
                if row[key] == "":
                    del row[key]
                else:
                    row[key] = float(row[key])
            cmor_variable = CmorVariable(**row)
            variable_table.variable_entry.append(cmor_variable)
        return variable_table


def load_variable_table(file_path: str) -> VariableTable:
    return VariableTable.parse_file(file_path)


def save_legacy_variable_table(table: VariableTable, output_location: str):
    table_dict = dict(table)
    table_dict['Header'] = dict(table_dict.pop('header'))
    for key, value in table_dict['Header'].items():
        if isinstance(value, list):
            table_dict['Header'][key] = " ".join(table_dict['Header'][key])
        elif isinstance(value, date):
            table_dict['Header'][key] = table_dict['Header'][key].strftime("%d %B %Y")
        else:
            table_dict['Header'][key] = str(table_dict['Header'][key])
    table_dict['Header']['Conventions'] = table_dict['Header'].pop('conventions')
    table_dict['variable_entry_list'] = table_dict.pop('variable_entry')
    table_dict['variable_entry'] = {}
    for variable in table_dict['variable_entry_list']:
        table_dict['variable_entry'].update({variable.id: dict(variable)})
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
        del table_dict['variable_entry'][variable.id]['id']
    del table_dict['variable_entry_list']
    with open(output_location, "w") as file:
        json.dump(table_dict, file, indent=2)


def save_variable_table(table: VariableTable, output_location: str):
    with open(output_location, "w") as file:
        file.write(table.json(indent=2, exclude_none=True))


def generate_new_from_legacy():
    root = Path(__file__).parent.parent
    files = root.joinpath("tables").glob("*.json")
    for path in files:
        new_filename = path.stem.split("_")[-1]
        new_path = root.joinpath("definitions", "variable_tables", f"{new_filename}.json")
        loaded = load_legacy_variable_table(path)
        save_variable_table(loaded, new_path)


def generate_legacy_from_new():
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
