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
:synopsis: Generate table wiki markup.
"""


# standard library imports

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports


def table_start():
    """Return table_start.

    :returns: table_start
    :rtype: str

    table_start = "{|";
    """
    return "{|"


def table_end():
    """Return table_end.

    :returns: table_end
    :rtype: str

    table_end = "|}";
    """
    return "|}"


@hypothesis.strategies.composite
def basic_table(draw, min_size, average_size, max_size):
    """Return basic table.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: basic table
    :rtype: str

    basic_table = "{|", { any Unicode character }, "|}";
    """
    basic_table_ = (
        table_start()
        + draw(
            hypothesis.strategies.text(
                alphabet=hypothesis.strategies.characters(),
                min_size=min_size,
                average_size=average_size,
                max_size=max_size
            )
        )
        + table_end()
    )
    return basic_table_
