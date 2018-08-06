#    This file is part of WikiPie 0.x.
#    Copyright (C) 2017  Carine Dengler
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
:synopsis: Tests HTML-style wiki markup and HTML tags parser elements.
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
    """Test tags parser element."""

    @hypothesis.given(
        hypothesis.strategies.text(min_size=1, average_size=8, max_size=16)
    )
    def test_noinclude_00(self, text):
        """Test noinclude tag parser element.

        :param str text: noinclude tag content

        noinclude = "<noinclude>", { any Unicode character }-, "</noinclude>";
        """
        noinclude = strategies.tags.noinclude(text)
        parser_element = tags.get_noinclude()
        parse_results = parser_element.parseString(noinclude)
        self.assertEqual(text, parse_results["text"])
        return

    @hypothesis.given(
        hypothesis.strategies.text(min_size=1, average_size=8, max_size=16)
    )
    def test_includeonly_00(self, text):
        """Test includeonly tag parser element.

        :param str text: includeonly tag content

        includeonly =
        "<includeonly>", { any Unicode character }-, "</includeonly>";
        """
        includeonly = strategies.tags.includeonly(text)
        parser_element = tags.get_includeonly()
        parse_results = parser_element.parseString(includeonly)
        self.assertEqual(text, parse_results["text"])
        return

    @hypothesis.given(
        hypothesis.strategies.text(min_size=1, average_size=8, max_size=16)
    )
    def test_onlyinclude_00(self, text):
        """Test onlyinclude tag parser element.

        :param str text: onlyinclude tag content

        onlyinclude =
        "<onlyinclude>", { any Unicode character }-, "</onlyinclude>";
        """
        onlyinclude = strategies.tags.onlyinclude(text)
        parser_element = tags.get_onlyinclude()
        parse_results = parser_element.parseString(onlyinclude)
        self.assertEqual(text, parse_results[0])
        return

    @hypothesis.given(
        hypothesis.strategies.text(min_size=1, average_size=8, max_size=16)
    )
    def test_comment_00(self, text):
        """Test comment parser element.

        :param str text: text

        comment = "<!--", { any Unicode character }-, "-->";
        """
        comment = strategies.tags.comment(text)
        parser_element = tags.get_comment()
        parse_results = parser_element.parseString(comment)
        self.assertEqual(text, parse_results["text"])
        return
