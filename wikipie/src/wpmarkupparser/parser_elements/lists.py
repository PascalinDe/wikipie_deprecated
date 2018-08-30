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
.. _`Help:List`: https://en.wikipedia.org/wiki/Help:List
.. _`Help:Wikitext`: https://en.wikipedia.org/wiki/Help:Nowiki

:synopsis: Lists wiki markup parser elements.

See `Help:List`_ and `Help:Wikitext`_  for further information.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.lists
import src.wpmarkupparser.parser_elements.fundamental


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def _get_unordered(parse_actions=False):
    """Get unordered parser element.

    unordered = "*";

    :returns: unordered parser element
    :rtype: ParserElement
    """
    unordered = pyparsing.Literal("*")
    unordered.setName("unordered")
    unordered.parseWithTabs()
    if parse_actions:
        pass
    return unordered


def _get_ordered(parse_actions=False):
    """Get ordered parser element.

    ordered = "#";

    :returns: ordered parser element
    :rtype: ParserElement
    """
    ordered = pyparsing.Literal("#")
    ordered.setName("ordered")
    ordered.parseWithTabs()
    if parse_actions:
        pass
    return ordered


def _get_term(parse_actions=False):
    """Get term parser element.

    term = ";";

    :returns: term parser element
    :rtype: ParserElement
    """
    term = pyparsing.Literal(";")
    term.setName("term")
    term.parseWithTabs()
    if parse_actions:
        pass
    return term


def _get_description(parse_actions=False):
    """Get description parser element.

    description = ":";

    :returns: description parser element
    :rtype: ParserElement
    """
    description = pyparsing.Literal(":")
    description.setName("description")
    description.parseWithTabs()
    if parse_actions:
        pass
    return description


def get_list_item(parse_actions=False):
    """Get list item parser element.

    list_item = line_start, { ordered | unordered }- |
    ( term | description ), [ { space | tabs }- ];

    :returns: list item parser element
    :rtype: ParserElement
    """
    ordered = _get_ordered(parse_actions=parse_actions)
    unordered = _get_unordered(parse_actions=parse_actions)
    term = _get_term(parse_actions=parse_actions)
    description = _get_description(parse_actions=parse_actions)
    space = src.wpmarkupparser.parser_elements.fundamental.get_space(
        parse_actions=parse_actions
    )
    tab = src.wpmarkupparser.parser_elements.fundamental.get_tab(
        parse_actions=parse_actions
    )
    list_item = pyparsing.Combine(
        pyparsing.lineStart
        + (pyparsing.OneOrMore(ordered ^ unordered) ^ (term ^ description))
        + pyparsing.Optional(pyparsing.OneOrMore(space ^ tab))
    )
    list_item.setName("list_name")
    list_item.parseWithTabs()
    if parse_actions:
        list_item.setParseAction(
            src.wpmarkupparser.parse_actions.lists.sub_list_item
        )
    return list_item


def get_indent(parse_actions=False):
    """Get indent parser element.

    indent = line_start, { ":" }-;

    :returns: indent parser element
    :rtype: ParserElement
    """
    indent = pyparsing.Combine(
        pyparsing.lineStart + pyparsing.OneOrMore(pyparsing.Literal(":"))
    )
    indent.setName("indent")
    indent.parseWithTabs()
    if parse_actions:
        indent.setParseAction(
            src.wpmarkupparser.parse_actions.lists.sub_indent
        )
    return indent
