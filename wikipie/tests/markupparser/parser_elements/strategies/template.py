#    This file is part of WikiPie.
#    Copyright (C) 2017  Carine Dengler
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
:synopsis: Generate template wiki markup.
"""


# standard library imports

# third party imports
import pyparsing
import hypothesis
import hypothesis.strategies

# library specific imports
import tests.wpdata
from tests.markupparser.parser_elements import strategies


# modifier = any modifier;
_MODIFIERS = list(tests.wpdata.MODIFIERS)
_MODIFIERS.sort(key=len, reverse=True)
MODIFIER = pyparsing.MatchFirst(
    pyparsing.CaselessKeyword(modifier) for modifier in _MODIFIERS
)

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
def modifier(draw):
    """Returns modifier.

    :returns: modifier
    :rtype: str

    modifier = any modifier;
    """
    modifier_ = draw(
        hypothesis.strategies.sampled_from(tests.wpdata.MODIFIERS)
    )
    return modifier_


def modifier_prefix(modifier_):
    """Returns modifier_prefix.

    :param str modifier_: modifier

    :returns: modifier_prefix
    :rtype: str

    modifier_prefix = modifier, ":";
    """
    return modifier_ + ":"


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

    :param str namespace_: namespace

    :returns: namespace_prefix
    :rtype: str

    namespace_prefix = namespace, ":";
    """
    return namespace_ + ":"


@hypothesis.strategies.composite
def template(draw, min_size, average_size, max_size):
    """Return template.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: template
    :rtype: str

    template = pagename;
    """
    template_ = draw(
        strategies.fundamental.pagename(min_size, average_size, max_size)
    )
    return template_


def full_template(template_, modifier_prefix_="", namespace_prefix_=""):
    """Return full_template.

    :param str template: template
    :param str modifier_prefix: modifier prefix
    :param str namespace_prefix: namespace prefix

    :returns: full_template
    :rtype: str

    full_template = [ modifier_prefix ], [ namespace_prefix ], template;
    """
    full_template_ = modifier_prefix_ + namespace_prefix_ + template_
    return full_template_


@hypothesis.strategies.composite
def value(draw, min_size, average_size, max_size):
    """Return value.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: value
    :rtype: str

    value = plaintext;
    """
    value_ = draw(
        strategies.fundamental.plaintext(min_size, average_size, max_size)
    )
    return value_


@hypothesis.strategies.composite
def name(draw, min_size, average_size, max_size):
    """Return name.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: name
    :rtype: str

    name = { any Unicode character w/o "|=" };
    """
    name_ = draw(
        hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(
                blacklist_characters="|="
            ),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return name_


def named_arg(name_, value_):
    """Return named.

    :param str name_: name
    :param str value_: value

    :returns: named
    :rtype: str

    named = name, "=", value;
    """
    named_ = name_ + "=" + value_
    return named_


def arg(arg_):
    """Return inclusion_param.

    :param str arg_: named or unnamed argument


    :returns: arg
    :rtype: str

    arg = "|", ( named_arg | unnamed_arg );
    """
    return "|" + arg_


def inclusion(full_template_, arg_=""):
    """Returns inclusion.

    :param str full_template_: full_template
    :param str arg_: arg

    :returns: inclusion
    :rtype: str

    inclusion = "{{", full_template, { arg }, "}}";
    """
    inclusion_ = ("{{" + full_template_ + arg_ + "}}")
    return inclusion_


@hypothesis.strategies.composite
def param_name(draw, min_size, average_size, max_size):
    """Return parameter name.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: param_name
    :rtype: str

    param_name = { any Unicode character without "|={}"};
    """
    param_name_ = draw(
        hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(
                blacklist_characters="|={}"
            ),
            min_size=min_size,
            average_size=average_size,
            max_size=max_size
        )
    )
    return param_name_


@hypothesis.strategies.composite
def default(draw, min_size, average_size, max_size):
    """Returns default.

    :param int min_size: minimum size
    :param int average_size: average size
    :param int max_size: maximum size

    :returns: default
    :rtype: str

    default = "|", { any Unicode character };
    """
    default_ = (
        "|"
        + draw(
            hypothesis.strategies.text(
                alphabet=hypothesis.strategies.characters(),
                min_size=min_size,
                average_size=average_size,
                max_size=max_size
            )
        )
    )
    return default_


def param(param_name_, default_=""):
    """Returns parameter.

    :param str name_: name
    :param str default_: default

    :returns: param
    :rtype: str

    param = "{{{", param_name, [ default ], "}}}";
    """
    param_ = "{{{" + param_name_ + default_ + "}}}"
    return param_
