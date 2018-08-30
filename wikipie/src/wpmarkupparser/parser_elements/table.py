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
.. _`Help:Basic table markup`: \
https://en.wikipedia.org/wiki/Help:Basic_table_markup

:synopsis: Table wiki markup parser elements.

See `Help:Basic table markup`_ for further information.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.table


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def get_basic_table(parse_actions=False):
    """Get basic table parser element.

    basic_table = "{|", { any Unicode character }, "|}";

    :returns: basic table parser element
    :rtype: ParserElement
    """
    basic_table = pyparsing.QuotedString(
        "{|", multiline=True, unquoteResults=False, endQuoteChar="|}"
    )
    basic_table.setName("basic_table")
    basic_table.parseWithTabs()
    if parse_actions:
        basic_table.setParseAction(
            src.wpmarkupparser.parse_actions.table.sub_basic_table
        )
    return basic_table
