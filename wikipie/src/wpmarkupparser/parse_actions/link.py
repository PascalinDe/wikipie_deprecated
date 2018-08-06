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
:synopsis: Link and external link parse actions.
"""


# standard library imports
# third party imports
# library specific imports


def sub_link(toks):
    """Substitute link.

    :param ParseResults toks: parse results

    :returns: label
    :rtype: str
    """
    if "label" in toks:
        label = toks["label"].strip()
    else:
        label = toks["pagename"].strip()
    if "label_extension" in toks:
        label += toks["label_extension"]
    return label


def sub_external_link(toks):
    """Substitute external link.

    :param ParseResults toks: parse results

    :returns: anchor
    :rtype: str
    """
    if "anchor" in toks["external_link"]:
        anchor = toks["external_link"]["anchor"].strip()
    else:
        anchor = toks["external_link"]["url"].strip()
    return anchor
