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
:synopsis: Generate page formatting wiki markup.
"""


# standard library imports

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from tests.markupparser.parser_elements import strategies


@hypothesis.strategies.composite
def heading(draw, min_size, average_size, max_size):
    """Return section heading.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: heading
    :rtype: str

    heading = plaintext;
    """
    heading_ = draw(
        strategies.fundamental.plaintext(min_size, average_size, max_size)
    )
    return heading_


@hypothesis.strategies.composite
def header6(draw, text):
    """Return header6.

    :param str text: text

    :returns: header6
    :rtype: str

    header6 = ( "<h6>", heading, "</h6>" ) | ( 6*"=", heading,  6*"=" );
    """
    opener = draw(hypothesis.strategies.sampled_from(("<h6>", 6*"=")))
    closer = "</h6>" if opener == "<h6>" else 6*"="
    header6_ = (opener + text + closer)
    return header6_


@hypothesis.strategies.composite
def header5(draw, text):
    """Return header5.

    :param str text: text

    :returns: header5
    :rtype: str

    header5 = ( "<h5>", heading, "</h5>" ) | ( 5*"=", heading,  5*"=" );
    """
    opener = draw(hypothesis.strategies.sampled_from(("<h5>", 5*"=")))
    closer = "</h5>" if opener == "<h5>" else 5*"="
    header5_ = (opener + text + closer)
    return header5_


@hypothesis.strategies.composite
def header4(draw, text):
    """Return header4.

    :param str text: text

    :returns: header4
    :rtype: str

    header4 = ( "<h4>", heading, "</h4>" ) | ( 4*"=", heading,  4*"=" );
    """
    opener = draw(hypothesis.strategies.sampled_from(("<h4>", 4*"=")))
    closer = "</h4>" if opener == "<h4>" else 4*"="
    header4_ = (opener + text + closer)
    return header4_


@hypothesis.strategies.composite
def header3(draw, text):
    """Return header3.

    :param str text: text

    :returns: header3
    :rtype: str

    header3 = ( "<h3>", heading, "</h3>" ) | ( 3*"=", heading,  3*"=" );
    """
    opener = draw(hypothesis.strategies.sampled_from(("<h3>", 3*"=")))
    closer = "</h3>" if opener == "<h3>" else 3*"="
    header3_ = (opener + text + closer)
    return header3_


@hypothesis.strategies.composite
def header2(draw, text):
    """Return header2.

    :param str text: text

    :returns: header2
    :rtype: str

    header2 = ( "<h2>", heading, "</h2>" ) | ( 2*"=", heading,  2*"=" );
    """
    opener = draw(hypothesis.strategies.sampled_from(("<h2>", 2*"=")))
    closer = "</h2>" if opener == "<h2>" else 2*"="
    header2_ = (opener + text + closer)
    return header2_


@hypothesis.strategies.composite
def header1(draw, text):
    """Return header1.

    :param str text: text

    :returns: header1
    :rtype: str

    header1 = ( "<h1>", heading, "</h1>" ) | ( 1*"=", heading,  1*"=" );
    """
    opener = draw(hypothesis.strategies.sampled_from(("<h1>", 1*"=")))
    closer = "</h1>" if opener == "<h1>" else 1*"="
    header1_ = (opener + text + closer)
    return header1_


def p_tag(content):
    """Return p_tag.

    :param str content: content

    :returns: p_tag
    :rtype: str

    p_tag = "<p>", content, "</p>"
    """
    p_tag_ = "<p>" + content + "</p>"
    return p_tag_


@hypothesis.strategies.composite
def br_tag(draw):
    """Return br.

    :returns: br
    :rtype: str

    br = "<br>" | "<br />"
    """
    br_tag_ = draw(hypothesis.strategies.sampled_from(("<br>", "<br />")))
    return br_tag_


@hypothesis.strategies.composite
def horizontal(draw):
    """Return horizontal.

    :returns: horizontal
    :rtype: str

    horizontal = "<hr>" | "----";
    """
    horizontal_ = draw(hypothesis.strategies.sampled_from(("<hr>", "----")))
    return horizontal_
