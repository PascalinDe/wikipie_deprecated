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
:synopsis: Test fundamental and recurring wiki markup parser elements.
"""


# standard library imports
import unittest

# third party imports
import hypothesis

# library specific imports
from src.wpmarkupparser.parser_elements import fundamental
from tests.markupparser.parser_elements import strategies


class TestFundamental(unittest.TestCase):
    """Test fundamental parser elements."""

    def test_space_00(self, space="\u0020"):
        """Test space parser element.

        space = U+0020;
        """
        parser_element = fundamental.get_space()
        parse_results = parser_element.parseString(space)
        self.assertEqual(space, parse_results[0])
        return

    def test_tab_00(self, tab="\u0009"):
        """Test tab parser element.

        tab = U+0009;
        """
        parser_element = fundamental.get_tab()
        parse_results = parser_element.parseString(tab)
        self.assertEqual(tab, parse_results[0])
        return

    @hypothesis.given(
        strategies.fundamental.newline()
    )
    def test_newline_00(self, newline):
        """Test newline parser element.

        :param str newline: newline

        newline = U+000AU+000D | U+000DU+000A | U+000A | U+000D;
        """
        parser_element = fundamental.get_newline()
        parse_results = parser_element.parseString(newline)
        self.assertEqual(newline, parse_results[0])
        return

    @hypothesis.given(
        strategies.fundamental.whitespace()
    )
    def test_whitespace_00(self, whitespace):
        """Test whitespace parser element.

        :param str whitespace: whitespace

        whitespace = space | tab | newline;
        """
        parser_element = fundamental.get_whitespace()
        parse_results = parser_element.parseString(whitespace)
        self.assertEqual(whitespace, parse_results[0])
        return

    @hypothesis.given(
        strategies.fundamental.plaintext(1, 8, 16)
    )
    def test_plaintext_00(self, plaintext):
        """Test plaintext parser element.

        :param str plaintext: plaintext

        plaintext = { ( any of a-zA-Z0-9 or '!"$%&()+,-./?@\^_`~',
        any of "[]*#:;='", any Unicode character without "|[]*#:;<>='{}" ) |
        any Unicode character without "|[]*#:;<>='{}" }-;
        """
        parser_element = fundamental.get_plaintext()
        parse_results = parser_element.parseString(plaintext)
        self.assertEqual(plaintext, parse_results[0])
        return

    @hypothesis.given(
        strategies.fundamental.special()
    )
    def test_special_00(self, special):
        """Test special character parser element.

        :param str special: special character

        special = any of "[]*#:;<>='";
        """
        parser_element = fundamental.get_special()
        parse_results = parser_element.parseString(special)
        self.assertEqual(special, parse_results[0])
        return

    @hypothesis.given(
        strategies.fundamental.pagename(1, 8, 16)
    )
    def test_pagename_00(self, pagename):
        """Test pagename parser element.

        :param str pagename: pagename

        pagename = { any Unicode character without "|[]#<>{}" }-;
        """
        parser_element = fundamental.get_pagename()
        parse_results = parser_element.parseString(pagename)
        self.assertEqual(pagename, parse_results[0])
        return
