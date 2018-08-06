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
.. _`Help:Interwiki linking`: \
https://en.wikipedia.org/wiki/Help:Interwiki_linking
.. _`Help:URL`: \
https://en.wikipedia.org/wiki/Help:URL
.. _`Uniform Resource Identifier`: \
https://en.wikipedia.org/wiki/URI_scheme

:synopsis: Link wiki markup parser elements.

See `Help:Interwiki linking`_, `Help:URL`_ and `Uniform Resource Identifier`_
for further information.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.link
import src.wpmarkupparser.parser_elements.fundamental


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def _get_label(parse_actions=False):
    """Get label parser element.

    label = { any Unicode character without "|[]" }-;

    :returns: label parser element
    :rtype: ParserElement
    """
    label = pyparsing.CharsNotIn("|[]").setResultsName("label")
    label.setName("label")
    label.parseWithTabs()
    if parse_actions:
        pass
    return label


def _get_label_extension(parse_actions=False):
    """Get label extension parser element.

    label_extension = { letter }-;

    :returns: label extension parser element
    :rtype: ParserElement
    """
    alphas = pyparsing.alphas
    label_extension = pyparsing.Word(alphas).setResultsName("label_extension")
    label_extension.setName("label_extension")
    label_extension.parseWithTabs()
    if parse_actions:
        pass
    return label_extension


def _get_language_code(language_codes, parse_actions=False):
    """Get language code parser element.

    :param list language_codes: language codes

    language_code = any language code;

    :returns: language code parser element
    :rtype: ParserElement
    """
    language_codes.sort(key=len, reverse=True)
    caseless_keywords = [
        pyparsing.CaselessKeyword(language_code)
        for language_code in language_codes
    ]
    language_code = (
        pyparsing.MatchFirst(caseless_keywords).setResultsName("language_code")
    )
    language_code.setName("language_code")
    language_code.parseWithTabs()
    if parse_actions:
        pass
    return language_code


def _get_language_prefix(language_codes, parse_actions=False):
    """Get language prefix parser element.

    :param list language_codes: language codes

    language_prefix = ":", language_code, ":";

    :returns: language prefix parser element
    :rtype: ParserElement
    """
    language_prefix = (
        pyparsing.Literal(":")
        + _get_language_code(language_codes, parse_actions=parse_actions)
        + pyparsing.Literal(":")
    )
    language_prefix.setName("language_prefix")
    language_prefix.parseWithTabs()
    if parse_actions:
        pass
    return language_prefix


def _get_project(projects, parse_actions=False):
    """Get project parser element.

    :param list projects: projects

    project = any project;

    :returns: project parser element
    :rtype: ParserElement
    """
    keywords = (
        [
            pyparsing.CaselessKeyword(project)
            for project in projects if project != "wikipedia"
        ]
        + [pyparsing.Keyword("wikipedia")]
    )
    project = pyparsing.MatchFirst(keywords).setResultsName("project")
    project.setName("project")
    project.parseWithTabs()
    if parse_actions:
        pass
    return project


def _get_project_prefix(projects, parse_actions=False):
    """Get project prefix parser element.

    :param list projects: projects

    project_prefix = project, ":";

    :returns: project prefix parser element
    :rtype: ParserElement
    """
    project = _get_project(projects, parse_actions)
    project_prefix = project + pyparsing.Literal(":")
    project_prefix.setName("project_prefix")
    project_prefix.parseWithTabs()
    if parse_actions:
        pass
    return project_prefix


def _get_interwiki_prefix(language_codes, projects, parse_actions=False):
    """Get interwiki prefix parser element.

    :param list language_codes: language codes
    :param list projects: projects

    interwiki_prefix = ( [ language_prefix ], project_prefix )
    | ( [ project ], language_prefix );

    :returns: interwiki prefix parser element
    :rtype: ParserElement
    """
    language_prefix = _get_language_prefix(
        language_codes, parse_actions=parse_actions
    )
    project_prefix = _get_project_prefix(projects, parse_actions=parse_actions)
    project = _get_project(projects, parse_actions=parse_actions)
    interwiki_prefix = (
        (pyparsing.Optional(language_prefix) + project_prefix)
        ^ (pyparsing.Optional(project) + language_prefix)
    )
    interwiki_prefix.setName("interwiki_prefix")
    interwiki_prefix.parseWithTabs()
    if parse_actions:
        pass
    return interwiki_prefix


def _get_namespace(namespaces, parse_actions=False):
    """Get namespace parser element.

    :param list namespaces: namespaces

    namespace = any namespace;

    :returns: namespace parser element
    :rtype: ParserElement
    """
    namespaces.sort(key=len, reverse=True)
    keywords = (
        [
            pyparsing.CaselessKeyword(namespace)
            for namespace in namespaces if namespace != "Wikipedia"
        ]
        + [pyparsing.Keyword("Wikipedia")]
    )
    namespace = pyparsing.MatchFirst(keywords).setResultsName("namespace")
    namespace.setName("namespace")
    namespace.parseWithTabs()
    if parse_actions:
        pass
    return namespace


def _get_namespace_prefix(namespaces, parse_actions=False):
    """Get namespace prefix parser element.

    :param list namespaces: namespaces

    namespace_prefix = namespace, ":";

    :returns: namespace prefix parser element
    :rtype: ParserElement
    """
    namespace = _get_namespace(namespaces, parse_actions=parse_actions)
    namespace_prefix = namespace + pyparsing.Literal(":")
    namespace_prefix.setName("namespace_prefix")
    namespace_prefix.parseWithTabs()
    if parse_actions:
        pass
    return namespace_prefix


def _get_full_pagename(namespaces, parse_actions=False):
    """Get full pagename parser element.

    :param list namespaces: namespaces

    full_pagename = [ namespace_prefix ], pagename;

    :returns: full pagename parser element
    :rtype: ParserElement
    """
    namespace_prefix = _get_namespace_prefix(
        namespaces, parse_actions=parse_actions
    )
    pagename = src.wpmarkupparser.parser_elements.fundamental.get_pagename(
        parse_actions=parse_actions
    )
    full_pagename = pyparsing.Optional(namespace_prefix) + pagename
    full_pagename.setName("full_pagename")
    full_pagename.parseWithTabs()
    if parse_actions:
        pass
    return full_pagename


def _get_page_link(language_codes, projects, namespaces, parse_actions=False):
    """Get page link parser element.

    :param list language_codes: language codes
    :param list projects: projects
    :param list namespaces: namespaces

    page_link = [ interwiki_prefix ], full_pagename;

    :returns: page link parser element
    :rtype: ParserElement
    """
    interwiki_prefix = _get_interwiki_prefix(
        language_codes, projects, parse_actions=parse_actions
    )
    full_pagename = _get_full_pagename(namespaces, parse_actions=parse_actions)
    page_link = pyparsing.Optional(interwiki_prefix) + full_pagename
    page_link.setName("page_link")
    page_link.parseWithTabs()
    if parse_actions:
        pass
    return page_link


def _get_heading(parse_actions=False):
    """Get heading parser element.

    heading = { any Unicode character without "|[]" }-;

    :returns: heading parser element
    :rtype: ParserElement
    """
    heading = pyparsing.CharsNotIn("|[]")
    heading.setName("heading")
    heading.parseWithTabs()
    if parse_actions:
        pass
    return heading


def _get_section_id(parse_actions=False):
    """Get section ID parser element.

    section_id = "#", heading;

    :returns: section ID parser element
    :rtype: ParserElement
    """
    section_id = pyparsing.Combine(pyparsing.Literal("#") + _get_heading())
    section_id.setName("section_id")
    section_id.parseWithTabs()
    if parse_actions:
        pass
    return section_id


def get_link(language_codes, projects, namespaces, parse_actions=False):
    """Get link parser element.

    :param list language_codes: language codes
    :param list projects: projects
    :param list namespaces: namespaces

    link = "[[", page_link, [ section_id ], [ "|", [ label ] ], "]]",
    [ label_extension ];

    :returns: link parser element
    :rtype: ParserElement
    """
    page_link = _get_page_link(
        language_codes, projects, namespaces, parse_actions=parse_actions
    )
    section_id = _get_section_id(parse_actions=parse_actions)
    label = _get_label(parse_actions=parse_actions)
    label_extension = _get_label_extension(parse_actions=parse_actions)
    link = (
        pyparsing.Literal("[[")
        + page_link
        + pyparsing.Optional(section_id)
        + pyparsing.Optional(
            pyparsing.Literal("|") + pyparsing.Optional(label)
        )
        + pyparsing.Literal("]]")
        + pyparsing.Optional(label_extension)
    ).setResultsName("link")
    link.setName("link")
    link.parseWithTabs()
    if parse_actions:
        link.setParseAction(src.wpmarkupparser.parse_actions.link.sub_link)
    return link


def _get_uri_character(parse_actions=False):
    """Get URI character parser element.

    uri_character = uri_reserved_character | uri_unreserved_character |
    html_encoded;
    uri_reserved_character = any of "!*'():@&=+$/#";
    uri_unreserved_character = letter | digit | any of "-_.~";
    html_encoded = "%", 2*hex_digit;

    :returns: URI character parser element
    :rtype: ParserElement
    """
    uri_reserved_character = pyparsing.oneOf(" ".join("!*'():@&=+$/#"))
    uri_reserved_character.setName("uri_reserved_character")
    uri_reserved_character.parseWithTabs()
    uri_unreserved_character = pyparsing.oneOf(
        " ".join(pyparsing.alphanums + "-_.~")
    )
    uri_unreserved_character.setName("uri_unreserved_character")
    uri_unreserved_character.parseWithTabs()
    html_encoded = pyparsing.Combine(
        pyparsing.Literal("%") + pyparsing.Word(pyparsing.hexnums, exact=2)
    )
    html_encoded.setName("html_encoded")
    html_encoded.parseWithTabs()
    uri_character = (
        uri_reserved_character ^ uri_unreserved_character ^ html_encoded
    )
    uri_character.setName("uri_character")
    uri_character.parseWithTabs()
    if parse_actions:
        pass
    return uri_character


def _get_url_scheme(parse_actions=False):
    """Get URL scheme parser element.

    url_scheme = letter, { letter | digit | any of "+-." }-;

    :returns: URL scheme parser element
    :rtype: ParserElement
    """
    url_scheme = pyparsing.Combine(
        pyparsing.oneOf(" ".join(pyparsing.alphas))
        + pyparsing.Word(pyparsing.alphanums + "+-.")
    )
    url_scheme.setName("url_scheme")
    url_scheme.parseWithTabs()
    if parse_actions:
        pass
    return url_scheme


def get_url(parse_actions=False):
    """Get URL parser element.

    url = url_scheme, ":", [ "//" ], { uri_character };

    :returns: URL parser element
    :rtype: ParserElement
    """
    url_scheme = _get_url_scheme(parse_actions=parse_actions)
    uri_character = _get_uri_character(parse_actions=parse_actions)
    url = pyparsing.Combine(
        url_scheme
        + pyparsing.Literal(":")
        + pyparsing.Optional(pyparsing.Literal("//"))
        + pyparsing.ZeroOrMore(uri_character)
    ).setResultsName("url")
    url.setName("url")
    url.parseWithTabs()
    if parse_actions:
        pass
    return url


def _get_anchor(parse_actions=False):
    """Get anchor parser element.

    anchor = { any Unicode character without "[]" }-;

    :returns: anchor parser element
    :rtype: ParserElement
    """
    anchor = pyparsing.CharsNotIn("[]").setResultsName("anchor")
    anchor.setName("anchor")
    anchor.parseWithTabs()
    if parse_actions:
        pass
    return anchor


def get_external_link(parse_actions=False):
    """Get external link parser element.

    external_link = "[", url, [ whitespace, anchor ], "]";

    :returns: external link parser element
    :rtype: ParserElement
    """
    url = get_url(parse_actions=parse_actions)
    whitespace = src.wpmarkupparser.parser_elements.fundamental.get_whitespace(
        parse_actions=parse_actions
    )
    anchor = _get_anchor(parse_actions=parse_actions)
    external_link = (
        pyparsing.Literal("[")
        + url
        + pyparsing.Optional(whitespace + anchor)
        + pyparsing.Literal("]")
    ).setResultsName("external_link")
    external_link.setName("external_link")
    external_link.parseWithTabs()
    if parse_actions:
        external_link.setParseAction(
            src.wpmarkupparser.parse_actions.link.sub_external_link
        )
    return external_link
