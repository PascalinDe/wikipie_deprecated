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
:synopsis: Run time parsers.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpdata
import src.wpmarkupparser.parse_actions.link
from src.wpmarkupparser.parser_elements import (
    fundamental, link, lists,
    magic_words, sections, table,
    tags, template, text_formatting
)


class Parser(object):
    """Run time parser.

    :param ConfigParser localization: localization
    """

    def __init__(self, localization=None):
        """Initialize run time parser.

        :param ConfigParser localization: localization
        """
        self.wiki_markup = None
        self.localization = localization
        self._restore()
        self._set_parser_elements()
        return

    def _restore(self):
        """Restore state."""
        pass

    def _set_parser_elements(self):
        """Set parser elements."""
        self.wiki_markup = None
        return

    def _get_behavior_switches(self):
        """Get behavior switches.

        :returns: behavior switches
        :rtype: list
        """
        behavior_switches = list(src.wpdata.BEHAVIOR_SWITCHES)
        if self.localization is not None:
            behavior_switches += list(
                behavior_switch
                for value in self.localization["BEHAVIOR_SWITCHES"].values()
                for behavior_switch in value.split(",")
            )
        return behavior_switches

    def _get_parser_extensions(self):
        """Get parser extensions.

        :returns: parser extensions
        :rtype: list
        """
        parser_extensions = list(src.wpdata.PARSER_EXTENSIONS)
        return parser_extensions

    def _get_language_codes(self):
        """Get language codes.

        :returns: language codes
        :rtype: list
        """
        language_codes = list(src.wpdata.LANGUAGE_CODES)
        return language_codes

    def _get_projects(self):
        """Get projects.

        :returns: projects
        :rtype: list
        """
        projects = list(src.wpdata.PROJECTS)
        return projects

    def _get_namespaces(self):
        """Get namespaces.

        :returns: namespaces
        :rtype: list
        """
        namespaces = list(src.wpdata.NAMESPACES)
        if self.localization is not None:
            namespaces += list(
                namespace
                for value in self.localization["NAMESPACES"].values()
                for namespace in value.split(",")
            )
        return namespaces

    def _get_variables(self):
        """Get variables.

        :returns: variables
        :rtype: list
        """
        variables = list(src.wpdata.VARIABLES)
        if self.localization is not None:
            variables += list(
                variable
                for value in self.localization["VARIABLES"].values()
                for variable in value.split(",")
            )
        return variables

    def _get_parser_functions(self):
        """Get parser functions.

        :returns: parser functions
        :rtype: list
        """
        parser_functions = list(src.wpdata.PARSER_FUNCTIONS)
        if self.localization is not None:
            parser_functions += list(
                parser_function
                for value in self.localization["PARSER_FUNCTIONS"].values()
                for parser_function in value.split(",")
            )
        return parser_functions

    def _get_modifiers(self):
        """Get modifiers.

        :returns: modifiers
        :rtype: list
        """
        modifiers = list(src.wpdata.MODIFIERS)
        if self.localization is not None:
            modifiers += list(
                modifier
                for value in self.localization["MODIFIERS"].values()
                for modifier in value.split(",")
            )
        return modifiers

    def _transform_text(self, text):
        """Transform text.

        :param str text: text

        :returns: text
        :rtype: str
        """
        text = self._strip_text(text)
        text = self._parse(text)
        return text

    def _strip_text(self, text):
        """Strip non-included wiki markup.

        :param str text: text

        :returns: text
        :rtype: str
        """
        onlyinclude = tags.get_onlyinclude()
        matches = onlyinclude.searchString(text)
        if matches:
            text = "".join(match[0] for match in matches)
        return text

    def _parse(self, text):
        """Parse wiki markup.

        :param str text: text

        :returns: text
        :rtype: str
        """
        matches = list(self.wiki_markup.scanString(text))
        text = ""
        delta = 0
        for toks, start, end in matches:
            substring_len = end - start
            sub = toks[0]
            text += sub
            delta += (substring_len - len(sub))
        return text


class TemplateParser(Parser):
    """Run time template parser.

    :ivar list params: parameters
    """

    def _restore(self):
        """Restore state."""
        self.params = []
        return

    def _set_parser_elements(self):
        """Set parser elements."""
        # wiki markup parser element
        self.wiki_markup = pyparsing.Forward()
        self.wiki_markup.setName("wiki_markup")
        self.wiki_markup.parseWithTabs()
        # behavior switch parser element
        behavior_switches = self._get_behavior_switches()
        behavior_switch = pyparsing.originalTextFor(
            magic_words.get_behaviour_switch(behavior_switches)
        )
        # param parser element
        param = pyparsing.originalTextFor(template.get_param(self.wiki_markup))
        # noinclude parser element
        noinclude = tags.get_noinclude(parse_actions=True)
        # comment parser element
        comment = pyparsing.originalTextFor(tags.get_comment())
        # parser extension parser element
        parser_extensions = self._get_parser_extensions()
        parser_extension = pyparsing.originalTextFor(
            tags.get_parser_extension(parser_extensions)
        )
        # basic table parser element
        basic_table = pyparsing.originalTextFor(table.get_basic_table())
        # br tag parser element
        br_tag = pyparsing.originalTextFor(sections.get_br_tag())
        # horizontal parser element
        horizontal = pyparsing.originalTextFor(sections.get_horizontal())
        # internal link parser element
        language_codes = self._get_language_codes()
        projects = self._get_projects()
        namespaces = self._get_namespaces()
        internal_link = pyparsing.originalTextFor(
            link.get_link(language_codes, projects, namespaces)
        )
        # abbr tag parser element
        abbr_tag = pyparsing.originalTextFor(text_formatting.get_abbr_tag())
        # URL parser element
        url = pyparsing.originalTextFor(link.get_url())
        # external link parser element
        external_link = pyparsing.originalTextFor(link.get_external_link())
        # list item parser element
        list_item = lists.get_list_item()
        # indent parser element
        indent = lists.get_indent()
        # plaintext parser element
        plaintext = pyparsing.originalTextFor(fundamental.get_plaintext())
        # special parser element
        special = pyparsing.originalTextFor(fundamental.get_special())
        # magic words variable parser element
        variables = self._get_variables()
        mw_variable = pyparsing.originalTextFor(
            magic_words.get_mw_variable(variables, self.wiki_markup)
        )
        # magic words parser function parser element
        parser_functions = self._get_parser_functions()
        mw_parser_function = pyparsing.originalTextFor(
            magic_words.get_mw_parser_function(
                parser_functions, self.wiki_markup
            )
        )
        # inclusion parser element
        modifiers = self._get_modifiers()
        inclusion = pyparsing.originalTextFor(
            template.get_inclusion(modifiers, namespaces, self.wiki_markup)
        )
        # header6 parser element
        header6 = pyparsing.originalTextFor(
            sections.get_header6(self.wiki_markup)
        )
        # header5 parser element
        header5 = pyparsing.originalTextFor(
            sections.get_header5(self.wiki_markup)
        )
        # header4 parser element
        header4 = pyparsing.originalTextFor(
            sections.get_header4(self.wiki_markup)
        )
        # header3 parser element
        header3 = pyparsing.originalTextFor(
            sections.get_header3(self.wiki_markup)
        )
        # header2 parser element
        header2 = pyparsing.originalTextFor(
            sections.get_header2(self.wiki_markup)
        )
        # header1 parser element
        header1 = pyparsing.originalTextFor(
            sections.get_header1(self.wiki_markup)
        )
        # paragraph tag parser element
        p_tag = pyparsing.originalTextFor(sections.get_p_tag(self.wiki_markup))
        # italics parser element
        italics = pyparsing.originalTextFor(
            text_formatting.get_italics(self.wiki_markup)
        )
        # bold parser element
        bold = pyparsing.originalTextFor(
            text_formatting.get_bold(self.wiki_markup)
        )
        # bold italics parser element
        bold_italics = pyparsing.originalTextFor(
            text_formatting.get_bold_italics(self.wiki_markup)
        )
        # cite parser element
        cite = pyparsing.originalTextFor(
            text_formatting.get_cite_tag(self.wiki_markup)
        )
        # assign parser element(s)
        self.wiki_markup << (
            # terminal magic words parser element(s)
            behavior_switch
            # terminal inclusion parser element(s)
            | param
            # terminal tag parser element(s)
            | noinclude
            | comment
            | parser_extension
            # terminal table parser element(s)
            | basic_table
            # terminal section parser element(s)
            | br_tag
            | horizontal
            # terminal link parser element(s)
            | internal_link
            # terminal text formatting parser element(s)
            | abbr_tag
            # terminal external link parser element(s)
            | url
            | external_link
            # terminal lists parser element(s)
            | list_item
            | indent
            # non-terminal magic words parser element(s)
            | mw_variable
            | mw_parser_function
            # non-terminal inclusion parser element(s)
            | inclusion
            # non-terminal section parser element(s)
            | header6
            | header5
            | header4
            | header3
            | header2
            | header1
            | p_tag
            # non-terminal text formatting parser element(s)
            | italics
            | bold
            | bold_italics
            | cite
            # terminal fundamental parser element(s)
            | plaintext
            | special
        )
        return

    def parse(self, page):
        """Parse Wikipedia page.

        :param Page page: page

        :returns: page
        :rtype: Page
        """
        page.text = self._transform_text(page.text)
        page.params = self.params
        self._restore()
        return page

    def _parse(self, text):
        """Parse wiki markup.

        :param str text: text

        :returns: text
        :rtype: str
        """
        matches = list(self.wiki_markup.scanString(text))
        text = ""
        delta = 0
        for toks, start, end in matches:
            substring_len = end - start
            if "param" in toks:
                sub = self._collect_param(start - delta, toks)
            else:
                sub = toks[0]
            text += sub
            delta += (substring_len - len(sub))
        return text

    def _collect_param(self, loc, toks):
        """Collect param.

        :param int loc: location of the matching substring
        :param ParseResults toks: parse results

        :returns: empty string
        :rtype: str
        """
        covered_text = toks[0] + toks["name"] + toks[-1]
        param = {
            "name": toks["name"],
            "covered_text": covered_text,
            "start_doc": loc,
            "end_doc": loc + len(covered_text)
        }
        if "value" in toks:
            if toks["value"] is not None:
                param["value"] = toks["value"]
            else:
                param["value"] = ""
        else:
            param["value"] = ""
        self.params.append(param)
        return covered_text


class ArticleParser(Parser):
    """Run time parser.

    :ivar Namespace args: command-line arguments
    :ivar ParserElement wiki_markup: wiki markup parser element
    :ivar list inclusions: inclusions
    :ivar int delta: delta
    :ivar list links: links
    :ivar list categories: categories
    """

    def __init__(self, args, localization=None):
        """Initialize run time article parser.

        :param Namespace args: command-line arguments
        :param ConfigParser localization: localization
        """
        super().__init__(localization=localization)
        self.args = args
        return

    def _restore(self):
        """Restore state."""
        self.inclusions = []
        self.delta = 0
        self.links = []
        self.categories = []
        return

    def _set_parser_elements(self):
        """Set parser elements."""
        # wiki markup parser element
        self.wiki_markup = pyparsing.Forward()
        self.wiki_markup.setName("wiki_markup")
        self.wiki_markup.parseWithTabs()
        # behavior switch parser element
        behavior_switches = self._get_behavior_switches()
        behavior_switch = magic_words.get_behaviour_switch(
            behavior_switches, parse_actions=True
        )
        # param parser element
        param = template.get_param(self.wiki_markup)
        # noinclude parser element
        noinclude = tags.get_noinclude(parse_actions=True)
        # comment parser element
        comment = tags.get_comment(parse_actions=True)
        # parser extension parser element
        parser_extensions = self._get_parser_extensions()
        parser_extension = tags.get_parser_extension(
            parser_extensions, parse_actions=True
        )
        # basic table parser element
        basic_table = table.get_basic_table(parse_actions=True)
        # br tag parser element
        br_tag = sections.get_br_tag(parse_actions=True)
        # horizontal parser element
        horizontal = sections.get_horizontal(parse_actions=True)
        # internal link parser element
        language_codes = self._get_language_codes()
        projects = self._get_projects()
        namespaces = self._get_namespaces()
        internal_link = link.get_link(
            language_codes, projects, namespaces
        )
        # abbr tag parser element
        abbr_tag = text_formatting.get_abbr_tag()
        # URL parser element
        url = link.get_url()
        # external link parser element
        external_link = link.get_external_link(parse_actions=True)
        # list item parser element
        list_item = lists.get_list_item(parse_actions=True)
        # indent parser element
        indent = lists.get_indent(parse_actions=True)
        # plaintext parser element
        plaintext = fundamental.get_plaintext()
        # special parser element
        special = fundamental.get_special()
        # magic words variable parser element
        variables = self._get_variables()
        mw_variable = magic_words.get_mw_variable(
            variables, self.wiki_markup, parse_actions=True
        )
        # magic words parser function parser element
        parser_functions = self._get_parser_functions()
        mw_parser_function = magic_words.get_mw_parser_function(
            parser_functions, self.wiki_markup, parse_actions=True
        )
        # inclusion parser element
        modifiers = self._get_modifiers()
        inclusion = template.get_inclusion(
            modifiers, namespaces, self.wiki_markup, parse_actions=True
        )
        # header6 parser element
        header6 = sections.get_header6(self.wiki_markup, parse_actions=True)
        # header5 parser element
        header5 = sections.get_header5(self.wiki_markup, parse_actions=True)
        # header4 parser element
        header4 = sections.get_header4(self.wiki_markup, parse_actions=True)
        # header3 parser element
        header3 = sections.get_header3(self.wiki_markup, parse_actions=True)
        # header2 parser element
        header2 = sections.get_header2(self.wiki_markup, parse_actions=True)
        # header1 parser element
        header1 = sections.get_header1(self.wiki_markup, parse_actions=True)
        # paragraph tag parser element
        p_tag = sections.get_p_tag(self.wiki_markup, parse_actions=True)
        # italics parser element
        italics = text_formatting.get_italics(
            self.wiki_markup, parse_actions=True
        )
        # bold parser element
        bold = text_formatting.get_bold(self.wiki_markup, parse_actions=True)
        # bold italics parser element
        bold_italics = text_formatting.get_bold_italics(
            self.wiki_markup, parse_actions=True
        )
        # cite parser element
        cite = text_formatting.get_cite_tag(self.wiki_markup)
        # assign parser element(s)
        self.wiki_markup << (
            # terminal magic words parser element(s)
            behavior_switch
            # terminal inclusion parser element(s)
            | param
            # terminal tag parser element(s)
            | noinclude
            | comment
            | parser_extension
            # terminal table parser element(s)
            | basic_table
            # terminal section parser element(s)
            | br_tag
            | horizontal
            # terminal link parser element(s)
            | internal_link
            # terminal text formatting parser element(s)
            | abbr_tag
            # terminal external link parser element(s)
            | url
            | external_link
            # terminal lists parser element(s)
            | list_item
            | indent
            # non-terminal magic words parser element(s)
            | mw_variable
            | mw_parser_function
            # non-terminal inclusion parser element(s)
            | inclusion
            # non-terminal section parser element(s)
            | header6
            | header5
            | header4
            | header3
            | header2
            | header1
            | p_tag
            # non-terminal text formatting parser element(s)
            | italics
            | bold
            | bold_italics
            | cite
            # terminal fundamental parser element(s)
            | plaintext
            | special
        )
        return

    def parse(self, page):
        """Parse Wikipedia page.

        :param Page page: page

        :returns: page
        :rtype: Page
        """
        page.text = self._transform_text(page.text)
        page.inclusions = self.inclusions
        page.links = self.links
        page.categories = self.categories
        self._restore()
        return page

    def _transform_text(self, text):
        """Transform text.

        :param str text: text

        :returns: text
        :rtype: str
        """
        text = self._strip_text(text)
        text = self._parse(text)
        return text

    def _parse(self, text):
        """Parse wiki markup.

        :param str text: text

        :returns: text
        :rtype: str
        """
        matches = list(self.wiki_markup.scanString(text))
        text = ""
        delta = 0
        for toks, start, end in matches:
            substring_len = end - start
            if "inclusion" in toks:
                sub = self._collect_inclusion(start-delta, toks)
            elif "link" in toks:
                sub = self._collect_link(start-delta, toks)
            else:
                sub = toks[0]
            text += sub
            delta += (substring_len - len(sub))
        return text

    def _collect_inclusion(self, loc, toks):
        """Collect inclusion.

        :param int loc: location of the matching substring
        :param ParseResults toks: parse results

        :returns: template
        :rtype: str
        """
        i = 0
        args = {}
        if "arg" in toks[0]:
            for arg in toks[0]["arg"]:
                if "name" in arg:
                    name = arg["name"]
                else:
                    name = str(i)
                    i += 1
                if arg["value"] is not None:
                    args[name] = arg["value"]
                else:
                    args[name] = ""
        template_ = "{}:{}".format(toks[0]["namespace"], toks[0]["pagename"])
        inclusion = {
            "template": template_,
            "args": args,
            "start_doc": loc,
            "end_doc": loc + len(template_)
        }
        self.inclusions.append(inclusion)
        return template_

    def _collect_link(self, loc, toks):
        """Collect link.

        :param int loc: location of the matching substring
        :param ParseResults toks: parse results

        :returns: label
        :rtype: str
        """
        is_category = False
        label = src.wpmarkupparser.parse_actions.link.sub_link(toks)
        if "namespace" in toks:
            is_category = self._collect_category(toks)
        link_ = {
            "covered_text": label,
            "target": toks["pagename"].strip(),
            "start_doc": loc,
            "end_doc": loc + len(label)
        }
        if not is_category:
            self.links.append(link_)
        else:
            if not self.args.categories:
                label = ""
        return label

    def _collect_category(self, toks):
        """Collect category.

        :param ParseResults toks: parse results

        :returns: category toggle
        :rtype: bool
        """
        is_category = False
        namespace = toks["namespace"]
        if namespace in src.wpdata.NAMESPACES["14"]:
            self.categories.append(toks["pagename"])
            is_category = True
        elif self.localization is not None:
            if namespace in self.localization["NAMESPACES"].getlist("14"):
                self.categories.append(toks["pagename"])
                is_category = True
        return is_category
