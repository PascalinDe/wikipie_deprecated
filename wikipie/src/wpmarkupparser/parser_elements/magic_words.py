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
.. _`Help:Magic words`: \
https://en.wikipedia.org/wiki/Help:Magic_variables
.. _`Help:Magic words (MediaWiki.org)`: \
https://www.mediawiki.org/wiki/Help:Magic_words

:synopsis: Magic words wiki markup parser elements.

See `Help:Magic words`_ and `Help:Magic words (MediaWiki.org)`_
for further information.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpmarkupparser.parse_actions.magic_words


pyparsing.ParserElement.setDefaultWhitespaceChars("")


def get_behaviour_switch(behavior_switches, parse_actions=False):
    """Get behavior switch parser element.

    :param list behavior_switches: behavior switches

    behavior_switch = any behavior switch;

    :returns: behavior switch parser element
    :rtype: ParserElement
    """
    behavior_switches.sort(key=len, reverse=True)
    behavior_switch = pyparsing.MatchFirst(
        behavior_switches
    ).setResultsName("behavior_switch")
    behavior_switch.setName("behavior_switch")
    behavior_switch.parseWithTabs()
    if parse_actions:
        behavior_switch.setParseAction(
            src.wpmarkupparser.parse_actions.magic_words.sub_behavior_switch
        )
    return behavior_switch


def _get_variable(variables, parse_actions=False):
    """Get variable parser element.

    :param list variables: variables

    variable = any variable;

    :returns: variable parser element
    :rtype: ParserElement
    """
    variables.sort(key=len, reverse=True)
    variable = pyparsing.MatchFirst(variables).setResultsName("variable")
    variable.setName("variable")
    variable.parseWithTabs()
    if parse_actions:
        pass
    return variable


def _get_arg(wiki_markup, parse_actions=False):
    """Get argument parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    arg = wiki markup;

    :returns: argument parser element
    :rtype: ParserElement
    """
    arg = wiki_markup.setResultsName("arg", listAllMatches=True)
    arg.setName("arg")
    arg.parseWithTabs()
    if parse_actions:
        pass
    return arg


def _get_mw_arg(wiki_markup, parse_actions=False):
    """Get magic words argument parser element.

    :param ParserElement wiki_markup: wiki markup parser element

    mw_arg = ":", arg, { "|", arg };
    """
    arg = _get_arg(wiki_markup, parse_actions=parse_actions)
    mw_arg = (
        pyparsing.Literal(":")
        + arg
        + pyparsing.ZeroOrMore(pyparsing.Literal("|") + arg)
    )
    mw_arg.setName("mw_arg")
    mw_arg.parseWithTabs()
    if parse_actions:
        pass
    return mw_arg


def get_mw_variable(variables, wiki_markup, parse_actions=False):
    """Get magic words variable parser element.

    :param list variables: variables
    :param ParserElement wiki_markup: wiki markup parser element

    mw_variable = "{{", variable, [ mw_arg ], "}}";

    :returns: magic words variable parser element
    :rtype: ParserElement
    """
    variable = _get_variable(variables, parse_actions=parse_actions)
    mw_arg = _get_mw_arg(wiki_markup, parse_actions=parse_actions)
    mw_variable = (
        pyparsing.Literal("{{")
        + variable
        + pyparsing.Optional(mw_arg)
        + pyparsing.Literal("}}")
    ).setResultsName("mw_variable")
    mw_variable.setName("mw_variable")
    mw_variable.parseWithTabs()
    if parse_actions:
        mw_variable.setParseAction(
            src.wpmarkupparser.parse_actions.magic_words.sub_variable
        )
    return mw_variable


def _get_parser_function(parser_functions, parse_actions=False):
    """Get parser function parser element.

    :param list parser_functions: parser functions

    parser_function = any parser function;

    :returns: parser function parser element
    :rtype: ParserElement
    """
    parser_functions.sort(key=len, reverse=True)
    parser_function = pyparsing.MatchFirst(
        parser_functions
    ).setResultsName("parser_function")
    parser_function.setName("parser_function")
    parser_function.parseWithTabs()
    if parse_actions:
        pass
    return parser_function


def get_mw_parser_function(parser_functions, wiki_markup, parse_actions=False):
    """Get magic words parser functions.

    :param list parser_functions: parser functions
    :param ParserElement wiki_markup: wiki markup parser element

    mw_parser_function = "{{", parser_function, [ mw_arg ], "}}";

    :returns: magic words parser functions
    :rtype: ParserElement
    """
    parser_function = _get_parser_function(
        parser_functions, parse_actions=parse_actions
    )
    mw_arg = _get_mw_arg(wiki_markup, parse_actions=parse_actions)
    mw_parser_function = (
        pyparsing.Literal("{{")
        + parser_function
        + pyparsing.Optional(mw_arg)
        + pyparsing.Literal("}}")
    ).setResultsName("mw_parser_function")
    mw_parser_function.setName("mw_parser_function")
    mw_parser_function.parseWithTabs()
    if parse_actions:
        mw_parser_function.setParseAction(
            src.wpmarkupparser.parse_actions.magic_words.sub_parser_function
        )
    return mw_parser_function
