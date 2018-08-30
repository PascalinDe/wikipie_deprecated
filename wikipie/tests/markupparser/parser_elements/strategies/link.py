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
:synopsis: Generate link wiki markup.
"""


# standard library imports
import string

# third party imports
import pyparsing
import hypothesis
import hypothesis.strategies

# library specific imports
import tests.wpdata
from tests.markupparser.parser_elements import strategies


# namespace = any namespace;
_NAMESPACES = [
    namespace
    for values in tests.wpdata.NAMESPACES.values()
    for namespace in values
    if namespace != "Wikipedia"

]
_NAMESPACES.sort(key=len, reverse=True)
NAMESPACE = pyparsing.MatchFirst(
    [pyparsing.CaselessKeyword(namespace) for namespace in _NAMESPACES]
    + [pyparsing.Keyword("Wikipedia")]
)


@hypothesis.strategies.composite
def label(draw, min_size, average_size, max_size):
    """Returns label.

    :param int min_size: minimum size
    :param int average_size: average_size
    :param int max_size: maximum size

    :returns: label
    :rtype: str

    label = { any Unicode character without "|[]" }-;
    """
    label_ = draw(
        hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(
                blacklist_characters="|[]"
            ),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return label_


@hypothesis.strategies.composite
def label_extension(draw, min_size, average_size, max_size):
    """Returns label_extension.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: label_extension
    :rtype: str

    label_extension = { letter }-;
    """
    label_extension_ = draw(
        hypothesis.strategies.text(
            alphabet=string.ascii_letters,
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return label_extension_


@hypothesis.strategies.composite
def language_code(draw):
    """Returns language_code.

    :returns: language_code
    :rtype: str

    language_code = any language code;
    """
    language_code_ = draw(
        hypothesis.strategies.sampled_from(tests.wpdata.LANGUAGE_CODES)
    )
    return language_code_


def language_prefix(language_code_):
    """Returns language_prefix.

    :param str language_code: language_code

    :returns: language_prefix
    :rtype: str

    language_prefix = ":", language_code, ":";
    """
    language_prefix_ = ":" + language_code_ + ":"
    return language_prefix_


@hypothesis.strategies.composite
def project(draw):
    """Returns project.

    :param str project: project

    :returns: project
    :rtype: str

    project = any project;
    """
    project_ = draw(hypothesis.strategies.sampled_from(tests.wpdata.PROJECTS))
    return project_


def project_prefix(project_):
    """Returns project_prefix.

    :param str project: project

    :returns: project_prefix
    :rtype: str

    project_prefix = project, ":";
    """
    project_prefix_ = project_ + ":"
    return project_prefix_


def interwiki_prefix(language_prefix_="", project_prefix_="", project_=""):
    """Returns interwiki_prefix.

    :param str language_prefix: language_prefix
    :param str project_prefix: project_prefix
    :param str project: project

    :returns: interwiki_prefix
    :rtype: str

    interwiki_prefix = ( [ language_prefix ], project_prefix ) |
    ( [ project ], language_prefix );
    """
    if language_prefix_:
        if project_prefix_:
            interwiki_prefix_ = language_prefix_ + project_prefix_
        elif project_:
            interwiki_prefix_ = project_ + language_prefix_
        else:
            interwiki_prefix_ = language_prefix_
    elif project_prefix_:
        interwiki_prefix_ = project_prefix_
    elif project_:
        interwiki_prefix_ = project_
    else:
        interwiki_prefix_ = ""
    return interwiki_prefix_


@hypothesis.strategies.composite
def namespace(draw):
    """Returns namespace.

    :returns: namespace
    :rtype: str

    namespace = any non-localized namespace;
    """
    namespace_ = draw(
        hypothesis.strategies.sampled_from(
            [
                namespace
                for values in tests.wpdata.NAMESPACES.values()
                for namespace in values
            ]
        )
    )
    return namespace_


def namespace_prefix(namespace_):
    """Returns namespace_prefix.

    :param str namespace: namespace

    :returns: namespace_prefix
    :rtype: str

    namespace_prefix = namespace, ":";
    """
    namespace_prefix_ = namespace_ + ":"
    return namespace_prefix_


@hypothesis.strategies.composite
def pagename(draw, min_size, average_size, max_size):
    """Returns pagename.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: pagename
    :rtype: str

    pagename = { any Unicode character without "|[]#<>{}" }-;
    """
    pagename_ = draw(
        strategies.fundamental.pagename(min_size, average_size, max_size)
    )
    return pagename_


def full_pagename(pagename_, namespace_prefix_=""):
    """Returns full_pagename.

    :param str pagename: pagename
    :param str namespace_prefix: namespace_prefix

    :returns: full_pagename
    :rtype: str

    full_pagename = [ namespace_prefix ], pagename;
    """
    full_pagename_ = namespace_prefix_ + pagename_
    return full_pagename_


def page_link(full_pagename_, interwiki_prefix_=""):
    """Returns page_link.

    :param str full_pagename: full_pagename
    :param str interwiki_prefix: interwiki_prefix

    :returns: page_link
    :rtype: str

    page_link = [ interwiki_prefix ], full_pagename;
    """
    page_link_ = interwiki_prefix_ + full_pagename_
    return page_link_


@hypothesis.strategies.composite
def heading(draw, min_size, average_size, max_size):
    """Returns heading.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: heading
    :rtype: str

    heading = { any Unicode character w/o "|[]" }-;
    """
    heading_ = draw(
        hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(
                blacklist_characters="|[]"
            ),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return heading_


def section_id(heading_):
    """Returns section_id.

    :param str heading: heading

    :returns: section_id
    :rtype: str

    section_id = "#", heading;
    """
    section_id_ = "#" + heading_
    return section_id_


def link(page_link_, section_id_="", pipe="", label_="", label_extension_=""):
    """Returns page_link.

    :param str page_link: page_link
    :param str section_id: section_id
    :param str label: label
    :param str label_extension: label_extension

    link = "[[", page_link, [ section_id ], [ "|", [ label ] ],
    "]]", [ label_extension ];
    """
    link_ = (
        "[["
        + page_link_
        + section_id_
        + pipe
        + label_
        + "]]"
        + label_extension_
    )
    return link_


@hypothesis.strategies.composite
def uri_reserved_character(draw):
    """Returns URI reserved character.

    :returns: URI reserved character
    :rtype: str

    uri_reserved_character = any of "!*'():@&=+$/#";
    """
    uri_reserved_character_ = draw(
        hypothesis.strategies.sampled_from("!*'():@&=+$/#")
    )
    return uri_reserved_character_


@hypothesis.strategies.composite
def uri_unreserved_character(draw):
    """Returns URI unreserved character.

    :returns: URI unreserved character
    :rtype: str

    uri_unreserved_character = letter | digit any of "-_.~";
    """
    uri_unreserved_character_ = draw(
        hypothesis.strategies.sampled_from(
            string.ascii_letters+string.digits+"-_.~"
        )
    )
    return uri_unreserved_character_


@hypothesis.strategies.composite
def html_encoded(draw):
    """Returns HTML encoded character.

    :returns: HTML encoded character
    :rtype: str

    html_encoded = "%", 2*hex_digit;
    """
    html_encoded_ = (
        "%"
        + draw(
            hypothesis.strategies.text(
                alphabet=string.hexdigits,
                min_size=2,
                average_size=2,
                max_size=2
            )
        )
    )
    return html_encoded_


@hypothesis.strategies.composite
def uri_character(draw):
    """Returns URI character.

    :returns: URI character
    :rtype: str

    uri_character = uri_reserved character | uri_unreserved_character |
    html_encoded;
    """
    uri_reserved_character_ = draw(uri_reserved_character())
    uri_unreserved_character_ = draw(uri_unreserved_character())
    html_encoded_ = draw(html_encoded())
    uri_character_ = draw(
        hypothesis.strategies.sampled_from(
            (uri_reserved_character_, uri_unreserved_character_, html_encoded_)
        )
    )
    return uri_character_


@hypothesis.strategies.composite
def url_scheme(draw, min_size, average_size, max_size):
    """Returns URL scheme.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: URL scheme
    :rtype: str

    url_scheme = letter, { letter | digit | any of "+-." };
    """
    url_scheme_ = draw(
        hypothesis.strategies.sampled_from(string.ascii_letters)
    )
    if max_size > 1:
        url_scheme_ += draw(
            hypothesis.strategies.text(
                alphabet=(string.ascii_letters+string.digits+"+-."),
                min_size=min_size,
                average_size=average_size,
                max_size=max_size
            )
        )
    return url_scheme_


@hypothesis.strategies.composite
def url(draw, url_scheme_size, uri_character_size):
    """Returns URL.

    :param tuple url_scheme_size: size (url_scheme)
    :param tuple uri_character_size: size (uri_character)

    :returns: URL
    :rtype: str

    url = url_scheme, ":", [ "//" ], { uri_character };
    """
    url_scheme_ = draw(
        url_scheme(url_scheme_size[0], url_scheme_size[1], url_scheme_size[2])
    )
    uri_character_ = draw(
        hypothesis.strategies.text(
            alphabet=uri_character(),
            min_size=uri_character_size[0],
            average_size=uri_character_size[1],
            max_size=uri_character_size[2]
        )
    )
    url_ = (
        url_scheme_
        + ":"
        + draw(hypothesis.strategies.sampled_from(("", "//")))
        + uri_character_
    )
    return url_


@hypothesis.strategies.composite
def anchor(draw, min_size, average_size, max_size):
    """Returns anchor.

    :returns: anchor
    :rtype: str

    anchor = { any Unicode character w/o "[]" }-;
    """
    anchor_ = draw(
        hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(
                blacklist_characters="[]"
            ),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return anchor_


@hypothesis.strategies.composite
def external_link(draw, url_, anchor_=""):
    """Returns external link.

    :param str url: URL
    :param str anchor: anchor

    :returns: external link
    :rtype: str

    external_link = "[", url, [ whitespace, anchor ], "]";
    """
    if anchor_:
        whitespace_ = draw(strategies.fundamental.whitespace())
        external_link_ = (
            "["
            + url_
            + whitespace_
            + anchor_
            + "]"
        )
    else:
        external_link_ = "[" + url_ + "]"
    return external_link_
