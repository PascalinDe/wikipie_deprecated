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
:synopsis: Test page formatting wiki markup parse actions.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.wpmarkupparser.parser_elements import fundamental, sections
from tests.markupparser.parser_elements import strategies


class TestSections(unittest.TestCase):
    """Test sections parse actions."""
    WIKI_MARKUP = (fundamental.get_plaintext() | fundamental.get_special())
    WIKI_MARKUP.setName("wiki_markup")
    WIKI_MARKUP.parseWithTabs()

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_header6_00(self, data):
        """Test header parse action (transform string)."""
        heading = data.draw(strategies.sections.heading(1, 8, 16))
        header6 = data.draw(strategies.sections.header6(heading))
        parser_element = sections.get_header6(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(header6)
        heading = "\n{}\n".format(heading.strip())
        self.assertEqual(heading, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_header5_00(self, data):
        """Test header parse action (transform string)."""
        heading = data.draw(strategies.sections.heading(1, 8, 16))
        header5 = data.draw(strategies.sections.header5(heading))
        parser_element = sections.get_header5(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(header5)
        heading = "\n{}\n".format(heading.strip())
        self.assertEqual(heading, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_header4_00(self, data):
        """Test header parse action (transform string)."""
        heading = data.draw(strategies.sections.heading(1, 8, 16))
        header4 = data.draw(strategies.sections.header4(heading))
        parser_element = sections.get_header4(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(header4)
        heading = "\n{}\n".format(heading.strip())
        self.assertEqual(heading, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_header3_00(self, data):
        """Test header parse action (transform string)."""
        heading = data.draw(strategies.sections.heading(1, 8, 16))
        header3 = data.draw(strategies.sections.header3(heading))
        parser_element = sections.get_header3(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(header3)
        heading = "\n{}\n".format(heading.strip())
        self.assertEqual(heading, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_header2_00(self, data):
        """Test header parse action (transform string)."""
        heading = data.draw(strategies.sections.heading(1, 8, 16))
        header2 = data.draw(strategies.sections.header2(heading))
        parser_element = sections.get_header2(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(header2)
        heading = "\n{}\n".format(heading.strip())
        self.assertEqual(heading, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_header1_00(self, data):
        """Test header parse action (transform string)."""
        heading = data.draw(strategies.sections.heading(1, 8, 16))
        header1 = data.draw(strategies.sections.header1(heading))
        parser_element = sections.get_header1(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(header1)
        heading = "\n{}\n".format(heading.strip())
        self.assertEqual(heading, transformed)
        return

    @hypothesis.given(
        strategies.fundamental.plaintext(1, 8, 16)
    )
    def test_p_tag_00(self, content):
        """Test p_tag parse action (transformString).

        :param str content: content
        """
        p_tag = strategies.sections.p_tag(content)
        parser_element = sections.get_p_tag(
            self.WIKI_MARKUP, parse_actions=True
        )
        transformed = parser_element.transformString(p_tag)
        p_tag = "\n{}".format(content.strip())
        self.assertEqual(p_tag, transformed)
        return

    @hypothesis.given(
        strategies.sections.br_tag()
    )
    def test_br_tag_00(self, br_tag):
        """Test br_tag parse action (transformString).

        :param str br_tag: br_tag
        """
        parser_element = sections.get_br_tag(parse_actions=True)
        transformed = parser_element.transformString(br_tag)
        br_tag = "\n"
        self.assertEqual(br_tag, transformed)
        return

    @hypothesis.given(
        strategies.sections.horizontal()
    )
    def test_horizontal_00(self, horizontal):
        """Test horizontal parse action (transformString).

        :param str horizontal: horizontal
        """
        parser_element = sections.get_horizontal(parse_actions=True)
        transformed = parser_element.transformString(horizontal)
        horizontal = ""
        self.assertEqual(horizontal, transformed)
        return
