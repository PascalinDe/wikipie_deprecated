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
:synopsis: Generate HTML-style wiki markup and HTML tags.
"""


# standard library imports

# third party imports

# library specific imports


def noinclude(text):
    """Return noinclude tag.

    :param str text: noinclude tag content

    :returns: noinclude tag
    :rtype: str

    noinclude = "<noinclude>", { any Unicode character }, "</noinclude>";
    """
    noinclude_ = "<noinclude>{}</noinclude>".format(text)
    return noinclude_


def includeonly(text):
    """Return includeonly tag.

    :param str text: includeonly tag content

    :returns: includeonly tag
    :rtype: str

    includeonly = "<includeonly>", { any Unicode character }, "</includeonly>";
    """
    includeonly_ = "<includeonly>{}</includeonly>".format(text)
    return includeonly_


def onlyinclude(text):
    """Return onlyinclude tag.

    :param str text: onlyinclude tag content

    :returns: onlyinclude tag
    :rtype: str

    onlyinclude = "<onlyinclude>", { any Unicode character }, "</onlyinclude>";
    """
    onlyinclude_ = "<onlyinclude>{}</onlyinclude>".format(text)
    return onlyinclude_


def comment(text):
    """Returns comment.

    :param str text: text

    comment = "<!--", { any Unicode character }, "-->";
    """
    comment_ = "<!--{}-->".format(text)
    return comment_
