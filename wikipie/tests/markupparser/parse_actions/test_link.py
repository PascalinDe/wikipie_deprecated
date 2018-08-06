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
:synopsis: Tests link wiki markup parse actions.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
import src.wpmarkupparser.parser_elements.link
import tests.wpdata
from tests.markupparser.parser_elements import strategies


class TestLink(unittest.TestCase):
    """Test link parse actions."""

    LANGUAGE_CODES = tests.wpdata.LANGUAGE_CODES
    PROJECTS = tests.wpdata.PROJECTS
    NAMESPACES = [
        namespace
        for value in tests.wpdata.NAMESPACES.values() for namespace in value
    ]

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_sub_link_00(self, data):
        """Test link parse action (transformString).

        link = "[[", pagename, "]]";
        """
        pagename = data.draw(strategies.link.pagename(1, 8, 16))
        link_ = strategies.link.link(pagename)
        parser_element = src.wpmarkupparser.parser_elements.link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES,
            parse_actions=True
        )
        transformed = parser_element.transformString(link_)
        self.assertEqual(pagename.strip(), transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_sub_link_01(self, data):
        """Test link parse action (transformString).

        link = "[[", pagename, "]]", label_extension;
        """
        pagename = data.draw(strategies.link.pagename(1, 8, 16))
        label_extension = data.draw(strategies.link.label_extension(1, 8, 16))
        link_ = strategies.link.link(
            pagename, label_extension_=label_extension
        )
        parser_element = src.wpmarkupparser.parser_elements.link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES,
            parse_actions=True
        )
        transformed = parser_element.transformString(link_)
        self.assertEqual(pagename.strip()+label_extension, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_sub_link_02(self, data):
        """Test link parse action (transformString).

        link = "[[", pagename, "|", label, "]]";
        """
        pagename = data.draw(strategies.link.pagename(1, 8, 16))
        label = data.draw(strategies.link.label(1, 8, 16))
        link_ = strategies.link.link(pagename, pipe="|", label_=label)
        parser_element = src.wpmarkupparser.parser_elements.link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES,
            parse_actions=True
        )
        transformed = parser_element.transformString(link_)
        self.assertEqual(label.strip(), transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_sub_link_03(self, data):
        """Test link parse action (transformString).

        link = "[[", pagename, "|", label, "]]", label_extension;
        """
        pagename = data.draw(strategies.link.pagename(1, 8, 16))
        label = data.draw(strategies.link.label(1, 8, 16))
        label_extension = data.draw(strategies.link.label_extension(1, 8, 16))
        link_ = strategies.link.link(
            pagename, label_=label, pipe="|", label_extension_=label_extension
        )
        parser_element = src.wpmarkupparser.parser_elements.link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES,
            parse_actions=True
        )
        transformed = parser_element.transformString(link_)
        self.assertEqual(label.strip()+label_extension, transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_sub_external_link_00(self, data):
        """Test external link parse action (transformString).

        external_link = "[", url, "]";
        """
        url = data.draw(strategies.link.url((1, 4, 8), (0, 4, 8)))
        external_link = data.draw(strategies.link.external_link(url))
        parser_element = (
            src.wpmarkupparser.parser_elements.link.get_external_link(
                parse_actions=True
            )
        )
        transformed = parser_element.transformString(external_link)
        self.assertEqual(url.strip(), transformed)
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_sub_external_link_01(self, data):
        """Test external link parse action (transformString).

        external_link = "[", url, whitespace, anchor, "]";
        """
        url = data.draw(strategies.link.url((1, 4, 8), (0, 4, 8)))
        anchor = data.draw(strategies.link.anchor(1, 8, 16))
        external_link = data.draw(
            strategies.link.external_link(url, anchor_=anchor)
        )
        parser_element = (
            src.wpmarkupparser.parser_elements.link.get_external_link(
                parse_actions=True
            )
        )
        transformed = parser_element.transformString(external_link)
        self.assertEqual(anchor.strip(), transformed)
        return
