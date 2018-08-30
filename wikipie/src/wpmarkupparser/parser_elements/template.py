#    This file is part of WikiPie 0.x.
#    Copyright (C) 2017  Carine Dengler, Heidelberg University (DBS)
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
.. _`Help:Template`: https://en.wikipedia.org/wiki/Help:Templates
.. _`Help:Templates`: https://www.mediawiki.org/wiki/Help:Templates
.. _`Help:Template (Meta-Wiki)`: https://meta.wikimedia.org/wiki/Help:Templates
.. _`Help:Advanced templates`: \
https://meta.wikimedia.org/wiki/Help:Advanced_templates

:synopsis: Template wiki markup parser elements.

See `Help:Template`_, `Help:Templates`_, `Help:Template (Meta-Wiki)`_
and `Help:Advanced templates`_ for further information.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.template
import src.wpmarkupparser.parser_elements.fundamental


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def _get_modifier(modifiers, parse_actions=False):
    """Get modifier parser element.

    :param list modifiers: modifiers

    modifier = any modifier;

    :returns: modifier parser element
    :rtype: ParserElement
    """
    modifiers.sort(key=len, reverse=True)
    modifiers = [
        pyparsing.CaselessKeyword(modifier) for modifier in modifiers
    ]
    modifier = pyparsing.MatchFirst(modifiers).setResultsName("modifier")
    modifier.parseWithTabs()
    if parse_actions:
        pass
    return modifier


def _get_modifier_prefix(modifiers, parse_actions=False):
    """Get modifier prefix parser element.

    :param list modifiers: modifiers

    modifier_prefix = modifier, ":";

    :returns: modifier prefix parser element
    :rtype: ParserElement
    """
    modifier = _get_modifier(modifiers, parse_actions=parse_actions)
    modifier_prefix = modifier + pyparsing.Literal(":")
    modifier_prefix.setName("modifier_prefix")
    modifier_prefix.parseWithTabs()
    if parse_actions:
        pass
    return modifier_prefix


def _get_namespace(namespaces, parse_actions=False):
    """Get namespace parser element.

    :param list namespaces: namespaces

    namespace = any namespace;

    :returns: namespace parser element
    :rtype: ParserElement
    """
    namespaces.sort(key=len, reverse=True)
    namespaces = [
        pyparsing.CaselessKeyword(namespace) for namespace in namespaces
    ]
    namespace = pyparsing.MatchFirst(namespaces).setResultsName("namespace")
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


def _get_pagename(parse_actions=False):
    """Get pagename parser element.

    :returns: pagename parser element
    :rtype: ParserElement
    """
    pagename = src.wpmarkupparser.parser_elements.fundamental.get_pagename()
    if parse_actions:
        pagename.setParseAction(
            src.wpmarkupparser.parse_actions.template.normalize_template
        )
    return pagename


def _get_full_template(
        modifiers, namespaces, localization=None, parse_actions=False
):
    """Get full template parser element.

    :param list modifiers: modifiers
    :param list namespaces: namespaces

    full_template = [ modifier_prefix ], [ namespace_prefix ], pagename;

    :returns: full template parser element
    :rtype: ParserElement
    """
    pagename = _get_pagename(parse_actions=parse_actions)
    modifier_prefix = _get_modifier_prefix(
        modifiers, parse_actions=parse_actions
    )
    namespace_prefix = _get_namespace_prefix(
        namespaces, parse_actions=parse_actions
    )
    full_template = (
        pyparsing.Optional(modifier_prefix)
        + pyparsing.Optional(namespace_prefix)
        + pagename
    )
    full_template.setName("full_template")
    full_template.parseWithTabs()
    if parse_actions:
        full_template.setParseAction(
            lambda toks:
            src.wpmarkupparser.parse_actions.template.mod_full_template(
                toks, localization=localization
            )
        )
    return full_template


def _get_value(wiki_markup, parse_actions=False):
    """Get value parser element.

    :param ParserElement wiki_markup: wiki markup

    value = wiki_markup;

    :returns: value parser element
    :rtype: ParserElement
    """
    value = pyparsing.Combine(
        pyparsing.OneOrMore(
            pyparsing.originalTextFor(wiki_markup)
        )
    ).setResultsName("value")
    value.setName("value")
    value.parseWithTabs()
    if parse_actions:
        pass
    return value


def _get_named_arg(wiki_markup, parse_actions=False):
    """Get named argument parser element.

    :param ParserElement wiki_markup: wiki markup

    named_arg = { any Unicode character without "|=" }, "=", value;

    :returns: named argument parser element
    :rtype: ParserElement
    """
    name = pyparsing.CharsNotIn("|=").setResultsName("name")
    name.setName("name")
    name.parseWithTabs()
    value = _get_value(wiki_markup)
    named_arg = (pyparsing.Optional(name) + pyparsing.Literal("=") + value)
    named_arg.setName("named_arg")
    named_arg.parseWithTabs()
    if parse_actions:
        pass
    return named_arg


def _get_arg(wiki_markup, parse_actions=False):
    """Get argument parser element.

    :param ParserElement wiki_markup: wiki markup

    arg = "|", ( named_arg | value );

    :returns: argument parser element
    :rtype: ParserElement
    """
    named_arg = _get_named_arg(wiki_markup)
    value = _get_value(wiki_markup)
    arg = (
        pyparsing.Literal("|") + (named_arg | value)
    ).setResultsName("arg", listAllMatches=True)
    arg.setName("arg")
    arg.parseWithTabs()
    if parse_actions:
        pass
    return arg


def get_inclusion(
        modifiers, namespaces, wiki_markup,
        localization=None, parse_actions=False
):
    """Get inclusion parser element.

    :param list modifiers: modifiers
    :param list namespaces: namespaces
    :param ParserElement wiki_markup: wiki markup

    inclusion = "{{", full_template, { arg }, "}}";
    """
    full_template = _get_full_template(
        modifiers, namespaces,
        localization=localization, parse_actions=parse_actions
    )
    arg = _get_arg(wiki_markup)
    inclusion = pyparsing.nestedExpr(
        opener="{{",
        closer="}}",
        content=(full_template + pyparsing.ZeroOrMore(arg)),
        ignoreExpr=None
    ).setResultsName("inclusion")
    inclusion.setName("inclusion")
    inclusion.parseWithTabs()
    if parse_actions:
        pass
    return inclusion


def get_param(wiki_markup, parse_actions=False):
    """Get parameter parser element.

    param = "{{{", { any Unicode character without "|={}" }-, [ default ],
    "}}}";
    default = "|", { any Unicode character };

    :returns: parameter parser element
    :rtype: ParserElement
    """
    name = pyparsing.CharsNotIn("|={}").setResultsName("name")
    name.setName("name")
    name.parseWithTabs()
    value = _get_value(wiki_markup, parse_actions=parse_actions)
    param = pyparsing.nestedExpr(
        opener="{{{",
        closer="}}}",
        content=(
            name
            + pyparsing.Optional(
                pyparsing.Literal("|") + pyparsing.Optional(value)
            )
        ),
        ignoreExpr=None
    )
    param.setName("param")
    param.parseWithTabs()
    if parse_actions:
        pass
    return param
