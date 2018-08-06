#    This file is part of WikiPie 0.x.
#    Copyright (C) 2017  WikiPie 0.x
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
:synopsis: Tests lists wiki markup parser elements.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.wpmarkupparser.parser_elements import lists
from tests.markupparser.parser_elements import strategies


class TestLists(unittest.TestCase):
    """Test lists parser elements."""

    @hypothesis.given(
        strategies.lists.list_item(1, 4, 8)
    )
    def test_list_item_00(self, list_item):
        """Test list_item parser element.

        :param str list_item: list_item

        list_item = line_start, { unordered | ordered }-,
        [ { space | tab }- ];
        """
        parser_element = lists.get_list_item()
        parse_results = parser_element.parseString(list_item)
        self.assertEqual(list_item, parse_results[0])
        return

    @hypothesis.given(
        strategies.lists.list_item(1, 1, 1)
    )
    def test_list_item_01(self, list_item):
        """Test list_item parser element.

        :param str list_item: list_item

        list_item = line_start, ( term | description ),
        [ { space | tab }- ];
        """
        parser_element = lists.get_list_item()
        parse_results = parser_element.parseString(list_item)
        self.assertEqual(list_item, parse_results[0])
        return

    @hypothesis.given(
        strategies.lists.indent(1, 4, 8)
    )
    def test_indent_00(self, indent):
        """Test indent parser element.

        :param str indent: indent

        indent = line_start, { ":" }-;
        """
        parser_element = lists.get_indent()
        parse_results = parser_element.parseString(indent)
        self.assertEqual(indent, parse_results[0])
        return
