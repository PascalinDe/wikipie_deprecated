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
:synopsis: Generate text formatting wiki markup.
"""


# standard library imports

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from tests.markupparser.parser_elements import strategies


@hypothesis.strategies.composite
def text(draw, min_size, average_size, max_size):
    """Return text.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    text = plaintext;
    """
    text_ = draw(
        strategies.fundamental.plaintext(min_size, average_size, max_size)
    )
    return text_


@hypothesis.strategies.composite
def italics(draw, text_):
    """Text formatting (italics).

    :param str text_: text

    italics = ( "''", text, "''" ) | ( "<i>", text, "</i>" );
    """
    italics_ = draw(
        hypothesis.strategies.sampled_from(
            ("''" + text_ + "''", "<i>" + text_ + "</i>")
        )
    )
    return italics_


@hypothesis.strategies.composite
def bold(draw, text_):
    """Text formatting (bold).

    :param str text_: text

    bold = ( "'''", text, "'''" ) | ( "<b>", text, "</b>" );
    """
    bold_ = draw(
        hypothesis.strategies.sampled_from(
            ("'''" + text_ + "'''", "<b>" + text_ + "</b>")
        )
    )
    return bold_


def bold_italics(text_):
    """Text formatting (bold/italics).

    :param str text_: text

    bold_italics = "'''''", text, "'''''";
    """
    return "'''''" + text_ + "'''''"
