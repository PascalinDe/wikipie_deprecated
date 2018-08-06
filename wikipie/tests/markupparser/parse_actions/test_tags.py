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
:synopsis: Test HTML-style wiki markup and HTML tags parse actions.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.wpmarkupparser.parser_elements import tags
from tests.markupparser.parser_elements import strategies


class TestTags(unittest.TestCase):
    """Test tags parse actions."""

    @hypothesis.given(
        hypothesis.strategies.text(min_size=1, average_size=8, max_size=16)
    )
    def test_noinclude_00(self, text):
        """Test noinclude tag parse action (transformString).

        :param str text: text
        """
        noinclude = strategies.tags.noinclude(text)
        parser_element = tags.get_noinclude(parse_actions=True)
        transformed = parser_element.transformString(noinclude)
        self.assertEqual("", transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.text(min_size=1, average_size=8, max_size=16)
    )
    def test_includeonly_00(self, text):
        """Test includeonly tag parse action (transformString).

        :param str text: text
        """
        includeonly = strategies.tags.includeonly(text)
        parser_element = tags.get_includeonly(parse_actions=True)
        transformed = parser_element.transformString(includeonly)
        self.assertEqual("", transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.text(min_size=1, average_size=8, max_size=16)
    )
    def test_comment_00(self, text):
        """Test comment parse action (transformString).

        :param str text: text
        """
        comment = strategies.tags.comment(text)
        parser_element = tags.get_comment(parse_actions=True)
        transformed = parser_element.transformString(comment)
        self.assertEqual("", transformed)
        return
