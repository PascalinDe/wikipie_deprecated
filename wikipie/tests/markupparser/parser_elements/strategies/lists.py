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
:synopsis: Generate lists wiki markup.
"""


# standard library imports

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from tests.markupparser.parser_elements import strategies


def unordered():
    """Return unordered.

    :returns: unordered
    :rtype: str

    unordered = "*";
    """
    return "*"


def ordered():
    """Return ordered.


    :returns: ordered
    :rtype: str

    ordered = "#";
    """
    return "#"


def term():
    """Return term.

    :returns: term
    :rtype: str

    term = ";"
    """
    return ";"


def description():
    """Return description.

    :returns: description
    :rtype: str

    description = ":"
    """
    return ":"


@hypothesis.strategies.composite
def list_item(draw, min_size, average_size, max_size):
    """Return list_item.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: list_item
    :rtype: str

    list_item = { unordered | ordered }- | ( term | description ),
    [ space_tabs ];
    """
    if max_size == 1:
        list_item_ = draw(
            hypothesis.strategies.sampled_from((term(), description()))
        )
    else:
        list_item_ = draw(
            hypothesis.strategies.text(
                alphabet=unordered()+ordered(),
                min_size=min_size,
                average_size=average_size,
                max_size=max_size
            )
        )
    list_item_ += draw(strategies.fundamental.space_tabs(0, 2, 4))
    return list_item_


@hypothesis.strategies.composite
def indent(draw, min_size, average_size, max_size):
    """Return indent.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: indent
    :rtype: str

    indent = { ":" }-;
    """
    indent_ = draw(
        hypothesis.strategies.text(
            alphabet=":",
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return indent_
