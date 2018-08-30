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
.. _`Markup spec/BNF/Article`: \
https://www.mediawiki.org/wiki/Special:MyLanguage/Markup_spec/BNF/Article

:synopsis: Fundamental and recurring wiki markup elements.

See `Markup spec/BNF/Article`_ for further information.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def get_space(parse_actions=False):
    """Get space parser element.

    space = U+0020;

    :returns: space parser element
    :rtype: ParserElement
    """
    space = pyparsing.Literal("\u0020")
    space.setName("space")
    space.parseWithTabs()
    if parse_actions:
        pass
    return space


def get_tab(parse_actions=False):
    """Get tab parser element.

    tab = U+0009;

    :returns: tab parser element
    :rtype: ParserElement
    """
    tab = pyparsing.Literal("\u0009")
    tab.setName("tab")
    tab.parseWithTabs()
    if parse_actions:
        pass
    return tab


def get_newline(parse_actions=False):
    """Get newline parser element.

    newline = U+000AU+000D | U+000DU+000A | U+000A | U+000D;

    :returns: newline parser element
    :rtype: ParserElement
    """
    newline = (
        pyparsing.Literal("\u000A\u000D")
        ^ pyparsing.Literal("\u000D\u000A")
        ^ pyparsing.Literal("\u000A")
        ^ pyparsing.Literal("\u000D")
    )
    newline.setName("newline")
    newline.parseWithTabs()
    if parse_actions:
        pass
    return newline


def get_whitespace(parse_actions=False):
    """Get whitespace parser element.

    whitespace = space | tab | newline;

    :returns: whitespace parser element
    :rtype: ParserElement
    """
    space = get_space()
    tab = get_tab()
    newline = get_newline()
    whitespace = (space ^ tab ^ newline).setResultsName("whitespace")
    whitespace.setName("whitespace")
    whitespace.parseWithTabs()
    if parse_actions:
        pass
    return whitespace


def get_plaintext(parse_actions=False):
    """Get plaintext parser element.

    plaintext = { ( any of a-zA-Z0-9 or '!"$%&()+,-./?@\^_`~',
    any of "[]*#:;='", any Unicode character without "|[]*#:;<>='{}" ) |
    any Unicode character without "|[]*#:;<>='{}" }-;

    :returns: plaintext parser element
    :rtype: ParserElement
    """
    str0 = '!"$%&()+,-./?@\^_`~'
    str1 = "[]*#:;='"
    str2 = "|[]*#:;<>='{}"
    plaintext = pyparsing.Combine(
        pyparsing.OneOrMore(
            (
                pyparsing.oneOf(" ".join(pyparsing.alphanums+str0))
                + pyparsing.oneOf(" ".join(str1))
                + pyparsing.CharsNotIn(str2, max=1)
            )
            ^ pyparsing.CharsNotIn(str2, max=1)
        )
    )
    plaintext.setName("plaintext")
    plaintext.parseWithTabs()
    if parse_actions:
        pass
    return plaintext


def get_special(parse_actions=False):
    """Get special character parser element.

    special = any of "[]*#:;<>='";

    :returns: special parser element
    :rtype: ParserElement
    """
    special = pyparsing.oneOf(" ".join("[]*#:;<>='"))
    special.setName("special")
    special.parseWithTabs()
    special.setDebug
    if parse_actions:
        pass
    return special


def get_pagename(parse_actions=False):
    """Get pagename parser element.

    pagename = { any Unicode character without "|[]#<>{}" }-;

    :returns: pagename parser element
    :rtype: ParserElement
    """
    pagename = pyparsing.CharsNotIn("|[]#<>{}").setResultsName("pagename")
    pagename.setName("pagename")
    pagename.parseWithTabs()
    if parse_actions:
        pass
    return pagename
