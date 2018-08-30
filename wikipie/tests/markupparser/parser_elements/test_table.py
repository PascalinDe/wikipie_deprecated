#    This file is part of WikiPie 0.x.
#    Copyright (C) 2017  Carine Dengler, Heidelberg University (DBS)
#
#    WikiPie 0.x is free software: you can redistribute it and/or modify
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
:synopsis: Test table wiki markup parser elements.
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
    """Test table parser elements."""

    @hypothesis.given(
        strategies.table.basic_table(0, 16, 32)
    )
    def test_basic_table_00(self, basic_table):
        """Test basic table parser element.

        :param str basic_table: basic table

        basic_table = "{|", { any Unicode character }, "|}";
        """
        parser_element = table.get_basic_table()
        parse_results = parser_element.parseString(basic_table)
        self.assertEqual(basic_table, parse_results[0])
        return
