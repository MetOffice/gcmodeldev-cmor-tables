###############################################################################
# (c) Crown copyright 2022 Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
###############################################################################
import unittest
import warnings
from pathlib import Path

from parameterized import parameterized

from utils.entities import VariableTable, Dimensions

root = Path(__file__).parent.parent.joinpath("definitions", "variable_tables")


def list_tables():
    files = root.glob("*.json")
    return [str(file.name) for file in files]


def load_table(file):
    return VariableTable.parse_file(root.joinpath(file))


class TestTables(unittest.TestCase):

    def setUp(self) -> None:
        dimensions = Dimensions.parse_file(Path(__file__).parent.parent.joinpath("definitions", "dimensions.json"))
        self.dimensions = {dim.id: dim for dim in dimensions.axis_entry}
        self.generic_dimensions = {dim.generic_level_name for dim in dimensions.axis_entry}

    @parameterized.expand(list_tables())
    def test_table_file(self, file):

        self.assertTrue(isinstance(load_table(file), VariableTable))

    @parameterized.expand(list_tables())
    def test_valid_dimensions(self, file):
        table = load_table(file)
        for variable in table.variable_entry:
            for dimension in variable.dimensions:
                msg = f"Test dimension {dimension} from variable {variable.id}" \
                      f" ({table.header.table_id}) is a valid dimension"
                # need to test not only if the dimension is valid but also
                # some are using generic level names as a dimension which are not
                # defined as dimensions. This second assertion of validity needs
                # confirming so outputting a warning for now
                if dimension not in self.dimensions:
                    if dimension in self.generic_dimensions:
                        warnings.warn(f"Using generic level rather than real dimensions - {msg}")
                    else:
                        self.fail(msg)


if __name__ == '__main__':
    unittest.main()
