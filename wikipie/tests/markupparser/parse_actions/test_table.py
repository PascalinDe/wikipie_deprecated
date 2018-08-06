#    This file is part of WikiPie.
#    Copyright (C) 2017  Carine Dengler
#
#    WikiPie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
:synopsis: Test table wiki markup parse actions.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.wpmarkupparser.parser_elements import table
from tests.markupparser.parser_elements import strategies


class TestTable(unittest.TestCase):
    """Test table parse actions."""

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_sub_table_00(self, data):
        """Test basic_table parse action (transformString).

        basic_table = "{|", { any Unicode character }, "|}";
        """
        basic_table = data.draw(strategies.table.basic_table(0, 16, 32))
        parser_element = table.get_basic_table(parse_actions=True)
        transformed = parser_element.transformString(basic_table)
        self.assertEqual("", transformed)
        return
