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
:synopsis: Tests template parser elements.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.wpmarkupparser.parser_elements import fundamental, template
from tests.markupparser.parser_elements import strategies
import tests.wpdata


class TestTemplate(unittest.TestCase):
    """Test template parser elements.

    :cvar ParserElement WIKI_MARKUP: wiki markup parser element
    :cvar list MODIFIERS: modifiers
    :cvar list NAMESPACES: namespaces
    """

    WIKI_MARKUP = (fundamental.get_plaintext() | fundamental.get_special())
    WIKI_MARKUP.setName("wiki_markup")
    WIKI_MARKUP.parseWithTabs()
    MODIFIERS = tests.wpdata.MODIFIERS
    NAMESPACES = [
        namespace
        for value in tests.wpdata.NAMESPACES.values()
        for namespace in value
    ]

    @hypothesis.given(
        strategies.template.modifier()
    )
    def test_modifier_00(self, modifier):
        """Test modifier parser element.

        :param str modifier: modifier

        modifier = any modifier;
        """
        parser_element = template._get_modifier(self.MODIFIERS)
        parse_results = parser_element.parseString(modifier)
        self.assertEqual(modifier, parse_results["modifier"])
        return

    @hypothesis.given(
        strategies.template.modifier()
    )
    def test_modifier_prefix_00(self, modifier):
        """Test modifier_prefix parser element.

        :param str modifier: modifier

        modifier_prefix = modifier, ":";
        """
        modifier_prefix = strategies.template.modifier_prefix(modifier)
        parser_element = template._get_modifier_prefix(self.MODIFIERS)
        parse_results = parser_element.parseString(modifier_prefix)
        self.assertEqual(modifier, parse_results["modifier"])
        return

    @hypothesis.given(
        strategies.template.namespace()
    )
    def test_namespace_00(self, namespace):
        """Test namespace parser element.

        :param str namespace: namespace

        namespace = any namespace;
        """
        parser_element = template._get_namespace(self.NAMESPACES)
        parse_results = parser_element.parseString(namespace)
        self.assertEqual(namespace, parse_results["namespace"])
        return

    @hypothesis.given(
        strategies.template.namespace()
    )
    def test_namespace_prefix_00(self, namespace):
        """Test namespace_prefix parser element.

        :param str namespace: namespace

        namespace_prefix = namespace, ":";
        """
        namespace_prefix = strategies.template.namespace_prefix(namespace)
        parser_element = template._get_namespace_prefix(self.NAMESPACES)
        parse_results = parser_element.parseString(namespace_prefix)
        self.assertEqual(namespace, parse_results["namespace"])
        return

    @hypothesis.given(
        strategies.template.template(1, 8, 16)
    )
    def test_template_00(self, template_):
        """Test template parser element.

        :param str template_: template

        template = { any Unicode character without "|[]#<>{}" }-;
        """
        parser_element = fundamental.get_pagename()
        parse_results = parser_element.parseString(template_)
        self.assertEqual(template_, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.template.template(1, 8, 16)
    )
    def test_full_template_00(self, template_):
        """Test full_template parser element.

        :param str template_: template

        full_template = template;
        """
        full_template = strategies.template.full_template(template_)
        parser_element = template._get_full_template(
            self.MODIFIERS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(full_template)
        self.assertEqual(template_, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.template.namespace(),
        strategies.template.template(1, 8, 16)
    )
    def test_full_template_01(self, namespace, template_):
        """Test full_template parser element.

        :param str namespace: namespace
        :param str template_: template

        full_template = namespace_prefix, template;
        """
        namespace_prefix = strategies.template.namespace_prefix(namespace)
        full_template = strategies.template.full_template(
            template_, namespace_prefix_=namespace_prefix
        )
        parser_element = template._get_full_template(
            self.MODIFIERS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(full_template)
        self.assertEqual(namespace, parse_results["namespace"])
        self.assertEqual(template_, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.template.modifier(),
        strategies.template.template(1, 8, 16)
    )
    def test_full_template_02(self, modifier, template_):
        """Test full_template parser element.

        :param str modifier: modifier
        :param str template_: template

        full_template = modifier_prefix, template;
        """
        modifier_prefix = strategies.template.modifier_prefix(modifier)
        full_template = strategies.template.full_template(
            template_, modifier_prefix_=modifier_prefix
        )
        parser_element = template._get_full_template(
            self.MODIFIERS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(full_template)
        self.assertEqual(modifier, parse_results["modifier"])
        self.assertEqual(template_, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.template.modifier(),
        strategies.template.namespace(),
        strategies.template.template(1, 8, 16)
    )
    def test_full_template_03(self, modifier, namespace, template_):
        """Test full_template parser element.

        :param str modifier: modifier
        :param str namespace: namespace
        :param str template_: template

        full_template = modifier_prefix, namespace_prefix, template;
        """
        modifier_prefix = strategies.template.modifier_prefix(modifier)
        namespace_prefix = strategies.template.namespace_prefix(namespace)
        full_template = strategies.template.full_template(
            template_,
            modifier_prefix_=modifier_prefix,
            namespace_prefix_=namespace_prefix
        )
        parser_element = template._get_full_template(
            self.MODIFIERS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(full_template)
        self.assertEqual(modifier, parse_results["modifier"])
        self.assertEqual(namespace, parse_results["namespace"])
        self.assertEqual(template_, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.template.value(1, 8, 16)
    )
    def test_value_00(self, value):
        """Test value parser element.

        :param str value: value

        value = plaintext;
        """
        parser_element = template._get_value(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(value)
        self.assertEqual(value, parse_results["value"])
        return

    @hypothesis.given(
        strategies.template.name(1, 4, 8),
        strategies.template.value(1, 8, 16)
    )
    def test_named_arg_00(self, name, value):
        """Test named_arg parser element.

        :param str name: name
        :param str value: value

        named_arg = { any Unicode character without "|=" }-, "=", value;
        """
        named_arg = strategies.template.named_arg(name, value)
        parser_element = template._get_named_arg(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(named_arg)
        self.assertEqual(name, parse_results["name"])
        self.assertEqual(value, parse_results["value"])
        return

    @hypothesis.given(
        strategies.template.value(1, 8, 16)
    )
    def test_named_arg_01(self, value):
        """Test named_arg parser element.

        :param str name: name
        :param str value: value

        named_arg = "=", value;
        """
        named_arg = strategies.template.named_arg("", value)
        parser_element = template._get_named_arg(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(named_arg)
        self.assertNotIn("name", parse_results)
        self.assertEqual(value, parse_results["value"])
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_arg_00(self, data):
        """Test arg parser element.

        arg = "|", named_arg;
        """
        name = data.draw(strategies.template.name(0, 4, 8))
        value = data.draw(strategies.template.value(1, 8, 16))
        named_arg = strategies.template.named_arg(name, value)
        arg = strategies.template.arg(named_arg)
        parser_element = template._get_arg(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(arg)
        if len(name):
            self.assertEqual(name, parse_results["arg"][0]["name"])
        else:
            self.assertNotIn("name", parse_results["arg"][0])
        self.assertEqual(value, parse_results["arg"][0]["value"])
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_arg_01(self, data):
        """Test arg parser element.

        arg = "|", unnamed_arg;
        """
        value = data.draw(strategies.template.value(1, 8, 16))
        arg = strategies.template.arg(value)
        parser_element = template._get_arg(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(arg)
        self.assertEqual(value, parse_results["arg"][0]["value"])
        return

    # inclusion = "{{", full_template, { arg }, "}}";
    # inclusion = "{{", ( modifier_prefix | namespace_prefix | template ) ...;
    # inclusion = ..., template, ( "}}" | named_arg | unnamed_arg ) ...;
    # inclusion = ..., ( template | value ), "}}";

    # inclusion = "{{", template, "}}";
    # inclusion = "{{", modifier_prefix, template,
    # named_arg, unnamed_arg, "}}";
    # inclusion = "{{", namespace_prefix, template, unnamed_arg,
    # named_arg, "}}";

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_inclusion_00(self, data):
        """Test inclusion parser element.

        inclusion = "{{", template, "}}";
        """
        template_ = data.draw(strategies.template.template(1, 8, 16))
        full_template = strategies.template.full_template(template_)
        inclusion = strategies.template.inclusion(full_template)
        parser_element = template.get_inclusion(
            self.MODIFIERS, self.NAMESPACES, self.WIKI_MARKUP
        )
        parse_results = parser_element.parseString(inclusion)
        self.assertEqual(template_, parse_results[0]["pagename"])
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_inclusion_01(self, data):
        """Test inclusion parser element.

        inclusion = "{{", modifier_prefix, template, named_arg,
        unnamed_arg, "}}";
        """
        modifier = data.draw(strategies.template.modifier())
        modifier_prefix = strategies.template.modifier_prefix(modifier)
        template_ = data.draw(strategies.template.template(1, 8, 16))
        full_template = strategies.template.full_template(
            template_, modifier_prefix_=modifier_prefix
        )
        name = data.draw(strategies.template.name(1, 4, 8))
        value0 = data.draw(strategies.template.value(1, 8, 16))
        named_arg = strategies.template.named_arg(name, value0)
        value1 = data.draw(strategies.template.value(1, 8, 16))
        arg = (
            strategies.template.arg(named_arg)
            + strategies.template.arg(value1)
        )
        inclusion = strategies.template.inclusion(full_template, arg_=arg)
        parser_element = template.get_inclusion(
            self.MODIFIERS, self.NAMESPACES, self.WIKI_MARKUP
        )
        parse_results = parser_element.parseString(inclusion)
        self.assertEqual(modifier, parse_results[0]["modifier"])
        self.assertEqual(template_, parse_results[0]["pagename"])
        self.assertEqual(name, parse_results[0]["arg"][0]["name"])
        self.assertEqual(value0, parse_results[0]["arg"][0]["value"])
        self.assertEqual(value1, parse_results[0]["arg"][1]["value"])
        return

    @hypothesis.given(
        hypothesis.strategies.data()
    )
    def test_inclusion_02(self, data):
        """Test inclusion parser element.

        inclusion = "{{", namespace_prefix, template, unnamed_arg,
        named_arg, "}}";
        """
        namespace = data.draw(strategies.template.namespace())
        namespace_prefix = strategies.template.namespace_prefix(namespace)
        template_ = data.draw(strategies.template.template(1, 8, 16))
        full_template = strategies.template.full_template(
            template_, namespace_prefix_=namespace_prefix
        )
        value0 = data.draw(strategies.template.value(1, 8, 16))
        name = data.draw(strategies.template.name(1, 4, 8))
        value1 = data.draw(strategies.template.value(1, 8, 16))
        named_arg = strategies.template.named_arg(name, value1)
        arg = (
            strategies.template.arg(value0)
            + strategies.template.arg(named_arg)
        )
        inclusion = strategies.template.inclusion(full_template, arg_=arg)
        parser_element = template.get_inclusion(
            self.MODIFIERS, self.NAMESPACES, self.WIKI_MARKUP
        )
        parse_results = parser_element.parseString(inclusion)
        self.assertEqual(namespace, parse_results[0]["namespace"])
        self.assertEqual(template_, parse_results[0]["pagename"])
        self.assertEqual(value0, parse_results[0]["arg"][0]["value"])
        self.assertEqual(name, parse_results[0]["arg"][1]["name"])
        self.assertEqual(value1, parse_results[0]["arg"][1]["value"])
        return

    @hypothesis.given(
        strategies.template.param_name(1, 4, 8)
    )
    def test_param_00(self, param_name):
        """Test param parser element.

        param = "{{{", { any Unicode character without "|={}" }-, "}}}";
        """
        param = strategies.template.param(param_name)
        parser_element = template.get_param(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(param)
        self.assertEqual(param_name, parse_results[0]["name"])
        return

    @hypothesis.given(
        strategies.template.param_name(1, 4, 8),
        strategies.template.default(0, 8, 16)
    )
    def test_param_01(self, param_name, default):
        """Test param parser_element.

        param = "{{{", { any Unicode character without "|={}" }-,
        default, "}}}";
        """
        param = strategies.template.param(param_name, default_=default)
        parser_element = template.get_param(self.WIKI_MARKUP)
        parse_results = parser_element.parseString(param)
        self.assertEqual(param_name, parse_results[0]["name"])
        if len(default) > 1:
            self.assertEqual(default[1:], parse_results[0]["value"])
        else:
            self.assertNotIn("value", parse_results[0])
        return
