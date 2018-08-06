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
.. _`Manual:Title.php`: \
https://www.mediawiki.org/wiki/Manual:Title.php#Canonical_forms

:synopsis: Template parse actions.

See `Manual:Title.php`_ for further information.
"""


# standard library imports

# third party imports

# library specific imports
import src.wpdata


def normalize_template(toks):
    """Normalize template.

    :param ParseResults toks: parse results

    :returns: normalized template
    :rtype: str
    """
    if len(toks["pagename"]) > 1:
        template = toks["pagename"][0].upper() + toks["pagename"][1:]
    else:
        template = toks["pagename"][0].upper()
    template = template.strip()
    return template


def mod_full_template(toks, localization=None):
    """Modify full_template.

    :param ParseResults toks: parse results
    :param ConfigParser localization: localization

    :returns: modified parse results
    :rtype: ParseResults
    """
    if "modifier" in toks:
        if localization is not None:
            modifier = localization["MODIFIERS"][toks["modifier"]]
    else:
        modifier = ""
    toks["modifier"] = modifier
    if "namespace" in toks:
        namespace = toks["namespace"]
        if namespace in src.wpdata.NAMESPACES["10"]:
            if localization is not None:
                namespace = localization["NAMESPACES"]["10"].split(",")[0]
    else:
        if localization is not None:
            namespace = localization["NAMESPACES"]["10"].split(",")[0]
        else:
            namespace = src.wpdata.NAMESPACES["10"][0]
    toks["namespace"] = namespace
    return toks
