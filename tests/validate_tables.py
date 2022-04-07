###############################################################################
# (c) Crown copyright 2022 Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
###############################################################################
import unittest
from pathlib import Path

from parameterized import parameterized

from utils.entities import VariableTable

root = Path(__file__).parent.parent.joinpath("definitions", "variable_tables")

def list_tables():

    files = root.glob("*.json")
    return [str(file.name) for file in files]


class TestTables(unittest.TestCase):

    @parameterized.expand(list_tables())
    def test_table_file(self, file):
        VariableTable.parse_file(root.joinpath(file))


if __name__ == '__main__':
    unittest.main()
