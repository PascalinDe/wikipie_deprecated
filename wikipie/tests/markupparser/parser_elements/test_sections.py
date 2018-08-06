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
:synopsis: Tests page formatting wiki markup parser elements.
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
    """Test section parser elements.

    :cvar ParserElement WIKI_MARKUP: wiki_markup
    """

    WIKI_MARKUP = (fundamental.get_plaintext() | fundamental.get_special())
    WIKI_MARKUP.setName("wiki_markup")
    WIKI_MARKUP.parseWithTabs()

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.sections.heading(1, 16, 32)
    )
    def test_header6_00(self, data, heading):
        """Test header6 parser element.

        :param str heading: heading

        header6 = ( "<h6>", heading, "</h6>" ) | ( 6*"=", heading, 6*"=" );
        """
        header6 = data.draw(strategies.sections.header6(heading))
        parser_element = sections.get_header6(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(header6)
        self.assertEqual(heading, "".join(parse_results[0]))
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.sections.heading(1, 16, 32)
    )
    def test_header5_00(self, data, heading):
        """Test header5 parser element.

        :param str heading: heading

        header5 = ( "<h5>", heading, "</h5>" ) | ( 5*"=", heading, 5*"=" );
        """
        header5 = data.draw(strategies.sections.header5(heading))
        parser_element = sections.get_header5(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(header5)
        self.assertEqual(heading, "".join(parse_results[0]))
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.sections.heading(1, 16, 32)
    )
    def test_header4_00(self, data, heading):
        """Test heading4 parser element.

        :param str heading: heading

        header4 = ( "<h4>", heading, "</h4>" ) | ( 4*"=", heading, 4*"=" );
        """
        header4 = data.draw(strategies.sections.header4(heading))
        parser_element = sections.get_header4(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(header4)
        self.assertEqual(heading, "".join(parse_results[0]))
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.sections.heading(1, 16, 32)
    )
    def test_header3_00(self, data, heading):
        """Test header3 parser element.

        :param str heading: heading

        header3 = ( "<h3>", heading, "</h3>" ) | ( 3*"=", heading, 3*"=" );
        """
        header3 = data.draw(strategies.sections.header3(heading))
        parser_element = sections.get_header3(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(header3)
        self.assertEqual(heading, "".join(parse_results[0]))
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.sections.heading(1, 16, 32)
    )
    def test_heading2_00(self, data, heading):
        """Test heading2 parser element.

        :param str heading: heading

        header2 = ( "<h2>", heading, "</h2>" ) | ( 2*"=", heading, 2*"=" );
        """
        header2 = data.draw(strategies.sections.header2(heading))
        parser_element = sections.get_header2(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(header2)
        self.assertEqual(heading, "".join(parse_results[0]))
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.sections.heading(1, 16, 32)
    )
    def test_heading1_00(self, data, heading):
        """Test heading1 parser element.

        :param str heading: heading

        header1 = ( "<h1>", heading, "</h1>" ) | ( 1*"=", heading, 1*"=" );
        """
        header1 = data.draw(strategies.sections.header1(heading))
        parser_element = sections.get_header1(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(header1)
        self.assertEqual(heading, "".join(parse_results[0]))
        return

    @hypothesis.given(
        strategies.fundamental.plaintext(1, 16, 32)
    )
    def test_p_tag_00(self, content):
        """Test p_tag parser element.

        :param str content: content

        p_tag = "<p>", content, "</p>";
        """
        p_tag = strategies.sections.p_tag(content)
        parser_element = sections.get_p_tag(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(p_tag)
        self.assertEqual(content, "".join(parse_results[0]))
        return

    @hypothesis.given(
        strategies.sections.br_tag()
    )
    def test_br_tag_00(self, br_tag):
        """Test br_tag parser element.

        :param str br_tag: br_tag

        br_tag = "<br>" | "<br />";
        """
        parser_element = sections.get_br_tag()
        parse_results = parser_element.parseString(br_tag)
        self.assertEqual(br_tag, parse_results[0])
        return

    @hypothesis.given(
        strategies.sections.horizontal()
    )
    def test_horizontal_00(self, horizontal):
        """Test horizontal parser element.

        :param str horizontal: horizontal

        horizontal = "<hr>" | "----";
        """
        parser_element = sections.get_horizontal()
        parse_results = parser_element.parseString(horizontal)
        self.assertEqual(horizontal, parse_results[0])
        return
