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
:synopsis: Generate fundamental and recurring wiki markup.
"""


# standard library imports
import string

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports


SPACE = "\u0020"
TAB = "\u0009"
NEWLINE = ("\u000A", "\u000D", "\u000A\u000D", "\u000D\u000A")


@hypothesis.strategies.composite
def space_tabs(draw, min_size, average_size, max_size):
    """Return space_tabs.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: space_tabs
    :rtype: str

    space_tabs = { space | tab }-;
    """
    space_tabs_ = draw(
        hypothesis.strategies.text(
            alphabet=SPACE+TAB,
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return space_tabs_


@hypothesis.strategies.composite
def newline(draw):
    """Return newline.

    :returns: newline
    :rtype: str

    newline = U+000A | U+000D | U+000AU+000D | U+000DU+000A;
    """
    newline_ = draw(hypothesis.strategies.sampled_from(NEWLINE))
    return newline_


@hypothesis.strategies.composite
def newlines(draw, min_size, average_size, max_size):
    """Return newlines.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: newlines
    :rtype: str

    newlines = { newline }-;
    """
    newlines_ = draw(
        hypothesis.strategies.text(
            alphabet=newline(),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return newlines_


@hypothesis.strategies.composite
def whitespace(draw):
    """Return whitespace.

    :returns: whitespace
    :rtype: str

    whitespace = space | tab | newline;
    """
    whitespace_ = draw(
        hypothesis.strategies.sampled_from((SPACE, TAB, draw(newline())))
    )
    return whitespace_


@hypothesis.strategies.composite
def whitespaces(draw, min_size, average_size, max_size):
    """Return whitespaces.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: whitespaces
    :rtype: str

    whitespaces = { whitespace }-;
    """
    whitespaces_ = draw(
        hypothesis.strategies.text(
            alphabet=whitespace(),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return whitespaces_


@hypothesis.strategies.composite
def plaintext(draw, min_size, average_size, max_size):
    """Return plaintext.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: plaintext
    :rtype: str

    plaintext = { any of a-z, A-Z, 0-9 or "!"$%&()+,-./?@\^_`~",
    any of "[]*#:;='",
    any Unicode character without "|[]*#:;<>='{}"
    | any Unicode character without "|[]*#:;<>='{}" }-;
    """
    char0 = hypothesis.strategies.characters(
        blacklist_characters="|[]*#:;<>='{}"
    )
    char1 = hypothesis.strategies.sampled_from(
        string.ascii_letters+string.digits+'!"$%&()+,-./?@\^_`~'
    )
    char2 = hypothesis.strategies.sampled_from("[]*#:;'")
    plaintext_ = draw(
        hypothesis.strategies.text(
            alphabet=hypothesis.strategies.sampled_from(
                (draw(char1) + draw(char2) + draw(char0), draw(char0))
            ),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return plaintext_


@hypothesis.strategies.composite
def special(draw):
    """Return special characters.

    :returns: special character
    :rtype: str

    special = any of "[]*#:;<>='";
    """
    special_ = draw(hypothesis.strategies.sampled_from("[]*#:;<>='"))
    return special_


@hypothesis.strategies.composite
def pagename(draw, min_size, average_size, max_size):
    """Return pagename.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: pagename
    :rtype: str

    pagename = { any Unicode character without "|[]#<>{}" }-;
    """
    pagename_ = draw(
        hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(
                blacklist_characters="|[]#<>{}"
            ),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return pagename_
