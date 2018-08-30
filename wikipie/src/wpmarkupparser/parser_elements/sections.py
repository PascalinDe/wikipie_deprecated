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
.. _`Help:Wikitext`: https://en.wikipedia.org/wiki/Help:Nowiki
.. _`Help:Section`: https://en.wikipedia.org/wiki/Help:Section

:synopsis: Page formatting wiki markup parser elements.

See `Help:Wikitext`_ and `Help:Section`_ for further information.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.sections


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def get_header6(wiki_markup, parse_actions=False):
    """Get header6 parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    header6 = line_start,
    ( 6*"=", content, 6*"=" ) | ( "<h6>", content, "</h6>" ),
    line_end;

    :returns: header6 parser element
    :rtype: ParserElement
    """
    header6 = (
        (
            (pyparsing.lineStart + pyparsing.Literal(6*"=")).suppress()
            + wiki_markup
            + (pyparsing.Literal(6*"=") + pyparsing.lineEnd).suppress()
        )
        | (
            (pyparsing.lineStart + pyparsing.Literal("<h6>")).suppress()
            + wiki_markup
            + (pyparsing.Literal("</h6>") + pyparsing.lineEnd).suppress()
        )
    )
    header6.setName("header6")
    header6.parseWithTabs()
    if parse_actions:
        header6.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_header6
        )
    return header6


def get_header5(wiki_markup, parse_actions=False):
    """Get header5 parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    header5 = line_start,
    ( 5*"=", content, 5*"=" ) | ( "<h5>", content, "</h5>" ),
    line_end;

    :returns: header5 parser element
    :rtype: ParserElement
    """
    header5 = (
        (
            (pyparsing.lineStart + pyparsing.Literal(5*"=")).suppress()
            + wiki_markup
            + (pyparsing.Literal(5*"=") + pyparsing.lineEnd).suppress()
        )
        | (
            (pyparsing.lineStart + pyparsing.Literal("<h5>")).suppress()
            + wiki_markup
            + (pyparsing.Literal("</h5>") + pyparsing.lineEnd).suppress()
        )
    )
    header5.setName("header5")
    header5.parseWithTabs()
    if parse_actions:
        header5.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_header5
        )
    return header5


def get_header4(wiki_markup, parse_actions=False):
    """Get header4 parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    header4 = line_start,
    ( 4*"=", content, 4*"=" ) | ( "<h4>", content, "</h4>" ),
    line_end;

    :returns: header4 parser element
    :rtype: ParserElement
    """
    header4 = (
        (
            (pyparsing.lineStart + pyparsing.Literal(4*"=")).suppress()
            + wiki_markup
            + (pyparsing.Literal(4*"=") + pyparsing.lineEnd).suppress()
        )
        | (
            (pyparsing.lineStart + pyparsing.Literal("<h4>")).suppress()
            + wiki_markup
            + (pyparsing.Literal("</h4>") + pyparsing.lineEnd).suppress()
        )
    )
    header4.setName("header4")
    header4.parseWithTabs()
    if parse_actions:
        header4.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_header4
        )
    return header4


def get_header3(wiki_markup, parse_actions=False):
    """Get header3 parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    header3 = line_start,
    ( 3*"=", content, 3*"=" ) | ( "<h3>", content, "</h3>" ),
    line_end;

    :returns: header3 parser element
    :rtype: ParserElement
    """
    header3 = (
        (
            (pyparsing.lineStart + pyparsing.Literal(3*"=")).suppress()
            + wiki_markup
            + (pyparsing.Literal(3*"=") + pyparsing.lineEnd).suppress()
        )
        | (
            (pyparsing.lineStart + pyparsing.Literal("<h3>")).suppress()
            + wiki_markup
            + (pyparsing.Literal("</h3>") + pyparsing.lineEnd).suppress()
        )
    )
    header3.setName("header3")
    header3.parseWithTabs()
    if parse_actions:
        header3.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_header3
        )
    return header3


def get_header2(wiki_markup, parse_actions=False):
    """Get header2 parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    header2 = line_start,
    ( 2*"=", content, 2*"=" ) | ( "<h2>", content, "</h2>" ),
    line_end;

    :returns: header2 parser element
    :rtype: ParserElement
    """
    header2 = (
        (
            (pyparsing.lineStart + pyparsing.Literal(2*"=")).suppress()
            + wiki_markup
            + (pyparsing.Literal(2*"=") + pyparsing.lineEnd).suppress()
        )
        | (
            (pyparsing.lineStart + pyparsing.Literal("<h2>")).suppress()
            + wiki_markup
            + (pyparsing.Literal("</h2>") + pyparsing.lineEnd).suppress()
        )
    )
    header2.setName("header2")
    header2.parseWithTabs()
    if parse_actions:
        header2.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_header2
        )
    return header2


def get_header1(wiki_markup, parse_actions=False):
    """Get header1 parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    header1 = line_start,
    ( 1*"=", content, 1*"=" ) | ( "<h1>", content, "</h1>" ),
    line_end;

    :returns: header1 parser element
    :rtype: ParserElement
    """
    header1 = (
        (
            (pyparsing.lineStart + pyparsing.Literal(1*"=")).suppress()
            + wiki_markup
            + (pyparsing.Literal(1*"=") + pyparsing.lineEnd).suppress()
        )
        | (
            (pyparsing.lineStart + pyparsing.Literal("<h1>")).suppress()
            + wiki_markup
            + (pyparsing.Literal("</h1>") + pyparsing.lineEnd).suppress()
        )
    )
    header1.setName("header1")
    header1.parseWithTabs()
    if parse_actions:
        header1.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_header1
        )
    return header1


def get_p_tag(wiki_markup, parse_actions=False):
    """Get paragraph tag parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    p_tag = "<p>", wiki_markup, "</p>";

    :returns: paragraph tag parser element
    :rtype: ParserElement
    """
    p_tag = (
        pyparsing.Literal("<p>").suppress()
        + wiki_markup
        + pyparsing.Literal("</p>").suppress()
    )
    p_tag.setName("p_tag")
    p_tag.parseWithTabs()
    if parse_actions:
        p_tag.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_p_tag
        )
    return p_tag


def get_br_tag(parse_actions=False):
    """Get br tag parser element.

    br_tag = "<br>" | "<br />" | "<br/>";

    :returns: br tag parser element
    :rtype: ParserElement
    """
    br_tag = (
        pyparsing.Literal("<br>") | pyparsing.Regex("<br[ ]?/>")
    )
    br_tag.setName("br_tag")
    br_tag.parseWithTabs()
    if parse_actions:
        br_tag.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_br_tag
        )
    return br_tag


def get_horizontal(parse_actions=False):
    """Get horizontal parser element.

    horizontal = "----" | "<hr>";

    :returns: horizontal parser element
    :rtype: ParserElement
    """
    horizontal = (
        pyparsing.Literal("----") | pyparsing.Literal("<hr>")
    )
    horizontal.setName("horizontal")
    horizontal.parseWithTabs()
    if parse_actions:
        horizontal.setParseAction(
            src.wpmarkupparser.parse_actions.sections.sub_horizontal
        )
    return horizontal
