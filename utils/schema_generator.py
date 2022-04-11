###############################################################################
# (c) Crown copyright 2022 Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
###############################################################################
"""
Generate the dimensions and variable-tables schema files based on the entity
definition
"""
from pathlib import Path

from utils.entities import VariableTable, Dimensions

DIMENSIONS_SCHEMA = Path(__file__).parent.parent.joinpath("schema", "dimensions.schema.json")

VARIABLE_TABLE_SCHEMA = Path(__file__).parent.parent.joinpath("schema", "variable-tables.schema.json")

with open(VARIABLE_TABLE_SCHEMA, "w") as schema_file:
    schema_file.write(VariableTable.schema_json(indent=2))

with open(DIMENSIONS_SCHEMA, "w") as schema_file:
    schema_file.write(Dimensions.schema_json(indent=2))
