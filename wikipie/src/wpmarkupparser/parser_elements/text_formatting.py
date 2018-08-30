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
.. _`Help:HTML in wikitext`: \
https://en.wikipedia.org/wiki/Help:HTML_in_wikitext

:synopsis: Text formatting wiki markup parser elements.

See `Help:Wikitext`_ and `Help:HTML in wikitext`_ for further information.
"""


# standard library imports
import re

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.text_formatting


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def get_italics(wiki_markup, parse_actions=False):
    """Get italics parser element.

    :param ParserElement wiki_markup: wiki markup

    italics = ( "''", text, "''" ) | ( "<i>", text, "</i>" );

    :returns: italics parser element
    :rtype: ParserElement
    """
    italics = (
        (
            pyparsing.Literal("''").suppress()
            + wiki_markup
            + pyparsing.Literal("''").suppress()
        )
        | (
            pyparsing.Literal("<i>").suppress()
            + wiki_markup
            + pyparsing.Literal("</i>").suppress()
        )
    )
    italics.setName("italics")
    italics.parseWithTabs()
    if parse_actions:
        italics.setParseAction(
            src.wpmarkupparser.parse_actions.text_formatting.sub_italics
        )
    return italics


def get_bold(wiki_markup, parse_actions=False):
    """Get bold parser element.

    :param ParserElement wiki_markup: wiki markup

    bold = ( "'''", wiki_markup, "'''" ) | ( "<b>", wiki_markup, "</b>" );

    :returns: bold parser element
    :rtype: ParserElement
    """
    bold = (
        (
            pyparsing.Literal("'''").suppress()
            + wiki_markup
            + pyparsing.Literal("'''").suppress()
        )
        | (
            pyparsing.Literal("<b>").suppress()
            + wiki_markup
            + pyparsing.Literal("</b>").suppress()
        )
    )
    bold.setName("bold")
    bold.parseWithTabs()
    if parse_actions:
        bold.setParseAction(
            src.wpmarkupparser.parse_actions.text_formatting.sub_bold
        )
    return bold


def get_bold_italics(wiki_markup, parse_actions=False):
    """Get bold italics parser element.

    :param ParserElement wiki_markup: wiki markup

    bold_itcalics = "'''''", wiki_markup, "'''''";

    :returns: bold italics parser element
    :rtype: ParserElement
    """
    bold_italics = (
        pyparsing.Literal("'''''").suppress()
        + wiki_markup
        + pyparsing.Literal("'''''").suppress()
    )
    bold_italics.setName("bold_italics")
    bold_italics.parseWithTabs()
    if parse_actions:
        bold_italics.setParseAction(
            src.wpmarkupparser.parse_actions.text_formatting.sub_bold_italics
        )
    return bold_italics


def get_abbr_tag(parse_actions=False):
    """Get abbr tag parser element.

    abbr_tag = opening_tag, wiki_markup, closing_tag;

    :returns: abbr tag parser element
    :rtype: ParserElement
    """
    abbr = pyparsing.Regex("<abbr(.*?)>(.*?)</abbr>", re.DOTALL)
    abbr.setName("abbr")
    abbr.parseWithTabs()
    if parse_actions:
        pass
    return abbr


def get_cite_tag(wiki_markup, parse_actions=False):
    """Get cite tag parser element.

    :param ParserElement wiki_markup: wiki markup

    cite_tag = opening_tag, wiki_markup, closing_tag;

    :returns: cite tag
    :rtype: ParserElement
    """
    cite_tag = (
        pyparsing.Literal("<cite>").suppress()
        + wiki_markup
        + pyparsing.Literal("</cite>").suppress()
    )
    cite_tag.setName("cite_tag")
    cite_tag.parseWithTabs()
    if parse_actions:
        pass
    return cite_tag
