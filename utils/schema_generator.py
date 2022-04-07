###############################################################################
# (c) Crown copyright 2022 Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
###############################################################################

from pathlib import Path

from utils.entities import VariableTable, Dimensions

with open(Path(__file__).parent.parent.joinpath("schema", "variable-tables.schema.json"), "w") as schema_file:
    schema_file.write(VariableTable.schema_json(indent=2))

with open(Path(__file__).parent.parent.joinpath("schema", "dimensions.schema.json"), "w") as schema_file:
    schema_file.write(Dimensions.schema_json(indent=2))
