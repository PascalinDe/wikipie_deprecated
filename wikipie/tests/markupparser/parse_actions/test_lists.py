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
:synopsis: Test lists wiki markup parse actions.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
import src.wpmarkupparser.parser_elements.lists
from tests.markupparser.parser_elements import strategies


class TestLists(unittest.TestCase):
    """Test lists parse actions."""

    @hypothesis.given(
        strategies.lists.list_item(1, 4, 8)
    )
    def test_sub_list_item_00(self, list_item):
        """Test list_item parse action (transformString).

        :param str list_item: list_item
        """
        parser_element = (
            src.wpmarkupparser.parser_elements.lists.get_list_item(
                parse_actions=True
            )
        )
        transformed = parser_element.transformString(list_item)
        list_item = "\n{} ".format(len(list_item.strip())*"-")
        self.assertEqual(list_item, transformed)
        return

    @hypothesis.given(
        strategies.lists.indent(1, 4, 8)
    )
    def test_sub_indent_00(self, indent):
        """Test indent parse action (transformString).

        :param str indent: indent
        """
        parser_element = (
            src.wpmarkupparser.parser_elements.lists.get_indent(
                parse_actions=True
            )
        )
        transformed = parser_element.transformString(indent)
        self.assertEqual("", transformed)
        return
