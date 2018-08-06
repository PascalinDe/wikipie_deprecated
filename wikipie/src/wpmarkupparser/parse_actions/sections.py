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
:synopsis: Page formatting parse actions.
"""


# standard library imports
# third party imports
# library specific imports


def sub_header6(toks):
    """Substitute header6.

    :param ParseResults toks: parse results

    :returns: heading
    :rtype: str
    """
    heading = "\n{}\n".format("".join(toks[0]).strip())
    return heading


def sub_header5(toks):
    """Substitute header5.

    :param ParseResults toks: parse results

    :returns: heading
    :rtype: str
    """
    heading = "\n{}\n".format("".join(toks[0]).strip())
    return heading


def sub_header4(toks):
    """Substitute header4.

    :param ParseResults toks: parse results

    :returns: heading
    :rtype: str
    """
    heading = "\n{}\n".format("".join(toks[0]).strip())
    return heading


def sub_header3(toks):
    """Substitute header3.

    :param ParseResults toks: parse results

    :returns: heading
    :rtype: str
    """
    heading = "\n{}\n".format("".join(toks[0]).strip())
    return heading


def sub_header2(toks):
    """Substitute header2.

    :param ParseResults toks: parse results

    :returns: heading
    :rtype: str
    """
    heading = "\n{}\n".format("".join(toks[0]).strip())
    return heading


def sub_header1(toks):
    """Substitute header1.

    :param ParseResults toks: parse results

    :returns: heading
    :rtype: str
    """
    heading = "\n{}\n".format("".join(toks[0]).strip())
    return heading


def sub_p_tag(toks):
    """Substitute p_tag.

    :returns: paragraph
    :rtype: str
    """
    paragraph = "\n{}".format("".join(toks[0]).strip())
    return paragraph


def sub_br_tag():
    """Substitute br_tag.

    :returns: linebreak
    :rtype: str
    """
    return "\n"


def sub_horizontal():
    """Substitute horizontal.

    :returns: empty string
    :rtype: str
    """
    return ""
