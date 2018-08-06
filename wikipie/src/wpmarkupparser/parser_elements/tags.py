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
.. _`Help:Template`: https://en.wikipedia.org/wiki/Help:Templates
.. _`Help:HTML in wikitext`: \
https://en.wikipedia.org/wiki/Help:HTML_in_wikitext
.. _`Version`: https://en.wikipedia.org/wiki/Special:Version

:synopsis: HTML-style and HTML tags wiki markup parser elements.

See `Help:HTML in wikitext`_, `Help:Template`_ and
`Version`_ for further information.
"""


# standard library imports
import re

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.tags


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def get_noinclude(parse_actions=False):
    """Get noinclude parser element.

    noinclude = "<noinclude>", { any Unicode character }-, "</noinclude>";

    :returns: noinclude parser element
    :rtype: ParserElement
    """
    noinclude = pyparsing.Regex(
        r"<noinclude>(?P<text>.+?)</noinclude>", re.DOTALL
    )
    noinclude.setName("noinclude")
    noinclude.parseWithTabs()
    if parse_actions:
        noinclude.setParseAction(
            src.wpmarkupparser.parse_actions.tags.sub_noinclude
        )
    return noinclude


def get_includeonly(parse_actions=False):
    """Get includeonly parser element.

    includeonly = "<includeonly>", { any Unicode character }-,
    "</includeonly>";

    :returns: includeonly parser element
    :rtype: ParserElement
    """
    includeonly = pyparsing.Regex(
        r"<includeonly>(?P<text>.+?)</includeonly>", re.DOTALL
    )
    includeonly.setName("includeonly")
    includeonly.parseWithTabs()
    if parse_actions:
        includeonly.setParseAction(
            src.wpmarkupparser.parse_actions.tags.sub_includeonly
        )
    return includeonly


def get_onlyinclude(parse_actions=False):
    """Get onlyinclude parser element.

    onlyinclude = "<onlyinclude>", { any Unicode character }-,
    "</onlyinclude>";

    :returns: onlyinclude parser element
    :rtype: ParserElement
    """
    onlyinclude = pyparsing.QuotedString(
        "<onlyinclude>", multiline=True, endQuoteChar="</onlyinclude>"
    )
    onlyinclude.setName("onlyinclude")
    onlyinclude.parseWithTabs()
    if parse_actions:
        pass
    return onlyinclude


def get_comment(parse_actions=False):
    """Get comment parser element.

    comment = "<!--", { any Unicode character }-, "-->";

    :returns: comment parser element
    :rtype: ParserElement
    """
    comment = pyparsing.Regex("<!--(?P<text>.+?)-->", re.DOTALL)
    comment.setName("comment")
    comment.parseWithTabs()
    if parse_actions:
        comment.setParseAction(
            src.wpmarkupparser.parse_actions.tags.sub_comment
        )
    return comment


def get_parser_extension(parser_extensions, parse_actions=False):
    """Get parser extension parser element.

    :param list parser_extensions: parser extensions

    parser_extension = opening tag, { any Unicode character }, closing tag;

    :returns: parser extension parser element
    :rtype: ParserElement
    """
    parser_extensions.sort(key=len, reverse=True)
    parser_extension = (
        pyparsing.MatchFirst(
            pyparsing.Regex("<{0}(.*?)>(.*?)</{0}>".format(tag), re.DOTALL)
            for tag in parser_extensions
        )
        | pyparsing.MatchFirst(
            pyparsing.Regex("<{}(.*?)/>".format(tag))
            for tag in parser_extensions
        )
    )
    parser_extension.setName("parser_extension")
    parser_extension.parseWithTabs()
    if parse_actions:
        parser_extension.setParseAction(
            src.wpmarkupparser.parse_actions.tags.sub_parser_extension
        )
    return parser_extension
