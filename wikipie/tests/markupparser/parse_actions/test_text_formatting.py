#    This file is part of WikiPie.
#    Copyright (C) 2017  Carine Dengler, Heidelberg University (DBS)
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
:synopsis: Test text formatting wiki markup parse actions.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.wpmarkupparser.parser_elements import fundamental, text_formatting
from tests.markupparser.parser_elements import strategies


class TestTextFormatting(unittest.TestCase):
    """Test text formatting parse actions."""
    WIKI_MARKUP = (fundamental.get_plaintext() | fundamental.get_special())
    WIKI_MARKUP.setName("wiki_markup")
    WIKI_MARKUP.parseWithTabs()

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.text_formatting.text(1, 16, 32)
    )
    def test_sub_italics_00(self, data, text):
        """Test italics parse action (transformString).

        :param str text: text
        """
        italics = data.draw(strategies.text_formatting.italics(text))
        parser_element = text_formatting.get_italics(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(italics)
        self.assertEqual(text, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.text_formatting.text(1, 16, 32)
    )
    def test_sub_bold_00(self, data, text):
        """Test bold parse action (transformString).

        :param str text: text
        """
        bold = data.draw(strategies.text_formatting.bold(text))
        parser_element = text_formatting.get_bold(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(bold)
        self.assertEqual(text, transformed)
        return

    @hypothesis.given(
        strategies.text_formatting.text(1, 16, 32)
    )
    def test_bold_italics_00(self, text):
        """Test bold/italics parse action (transformString).

        :param str text: text
        """
        bold_italics = strategies.text_formatting.bold_italics(text)
        parser_element = text_formatting.get_bold_italics(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(bold_italics)
        self.assertEqual(text, transformed)
        return
