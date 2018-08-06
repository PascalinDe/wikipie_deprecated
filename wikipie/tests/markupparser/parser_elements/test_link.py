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
:synopsis: Test link wiki markup parser elements.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
import tests.wpdata
from src.wpmarkupparser.parser_elements import link
from tests.markupparser.parser_elements import strategies


class TestLink(unittest.TestCase):
    """Test link parser elements.

    :cvar list LANGUAGE_CODES: language codes
    :cvar list PROJECTS: projects
    :cvar list NAMESPACES: namespaces
    """
    LANGUAGE_CODES = tests.wpdata.LANGUAGE_CODES
    PROJECTS = tests.wpdata.PROJECTS
    NAMESPACES = [
        namespace
        for value in tests.wpdata.NAMESPACES.values() for namespace in value
    ]

    @hypothesis.given(
        strategies.link.label(1, 8, 16)
    )
    def test_label_00(self, label):
        """Test label parser element.

        :param str label: label

        label = { any Unicode character without "|[]" }-;
        """
        parser_element = link._get_label()
        parse_results = parser_element.parseString(label)
        self.assertEqual(label, parse_results["label"])
        return

    @hypothesis.given(
        strategies.link.label_extension(1, 8, 16)
    )
    def test_label_extension_00(self, label_extension):
        """Test label_extension parser element.

        :param str label_extension: label_extension

        label_extension = { letter }-;
        """
        parser_element = link._get_label_extension()
        parse_results = parser_element.parseString(label_extension)
        self.assertEqual(label_extension, parse_results["label_extension"])
        return

    @hypothesis.given(
        strategies.link.language_code()
    )
    def test_language_code_00(self, language_code):
        """Test language_code parser_element.

        :param str language_code: language_code

        language_code = any language_code;
        """
        parser_element = link._get_language_code(self.LANGUAGE_CODES)
        parse_results = parser_element.parseString(language_code)
        self.assertEqual(language_code, parse_results["language_code"])
        return

    @hypothesis.given(
        strategies.link.language_code()
    )
    def test_language_prefix_00(self, language_code):
        """Test language_prefix parser_element.

        :param str language_code: language_code

        language_prefix = ":", language_code, ":";
        """
        language_prefix = strategies.link.language_prefix(language_code)
        parser_element = link._get_language_prefix(self.LANGUAGE_CODES)
        parse_results = parser_element.parseString(language_prefix)
        self.assertEqual(language_code, parse_results["language_code"])
        return

    @hypothesis.given(
        strategies.link.project()
    )
    def test_project_00(self, project):
        """Test project parser_element.

        :param str project: project

        project = any project;
        """
        parser_element = link._get_project(self.PROJECTS)
        parse_results = parser_element.parseString(project)
        self.assertEqual(project, parse_results["project"])
        return

    @hypothesis.given(
        strategies.link.project()
    )
    def test_project_prefix_00(self, project):
        """Test project_prefix parser_element.

        :param str project: project

        project_prefix = project, ":";
        """
        project_prefix = strategies.link.project_prefix(project)
        parser_element = link._get_project_prefix(self.PROJECTS)
        parse_results = parser_element.parseString(project_prefix)
        self.assertEqual(project, parse_results["project"])
        return

    @hypothesis.given(
        strategies.link.language_code(),
        strategies.link.project()
    )
    def test_interwiki_prefix_00(self, language_code, project):
        """Test interwiki_prefix parser_element.

        :param str language_code: language_code
        :param str project: project

        interwiki_prefix = language_prefix, project_prefix;
        """
        language_prefix = strategies.link.language_prefix(language_code)
        project_prefix = strategies.link.project_prefix(project)
        interwiki_prefix = strategies.link.interwiki_prefix(
            language_prefix_=language_prefix,
            project_prefix_=project_prefix
        )
        parser_element = link._get_interwiki_prefix(
            self.LANGUAGE_CODES, self.PROJECTS
        )
        parse_results = parser_element.parseString(interwiki_prefix)
        self.assertEqual(language_code, parse_results["language_code"])
        self.assertEqual(project, parse_results["project"])
        return

    @hypothesis.given(
        strategies.link.project()
    )
    def test_interwiki_prefix_01(self, project):
        """Test interwiki_prefix parser_element.

        :param str project: project

        interwiki_prefix = project_prefix;
        """
        project_prefix = strategies.link.project_prefix(project)
        interwiki_prefix = strategies.link.interwiki_prefix(
            project_prefix_=project_prefix
        )
        parser_element = link._get_interwiki_prefix(
            self.LANGUAGE_CODES, self.PROJECTS
        )
        parse_results = parser_element.parseString(interwiki_prefix)
        self.assertEqual(project, parse_results["project"])
        return

    @hypothesis.given(
        strategies.link.project(),
        strategies.link.language_code()
    )
    def test_interwiki_prefix_02(self, project, language_code):
        """Test interwiki_prefix parser_element.

        :param str project: project
        :param str language_code: language_code

        interwiki_prefix = project, language_prefix;
        """
        language_prefix = strategies.link.language_prefix(language_code)
        interwiki_prefix = strategies.link.interwiki_prefix(
            project_=project,
            language_prefix_=language_prefix
        )
        parser_element = link._get_interwiki_prefix(
            self.LANGUAGE_CODES, self.PROJECTS
        )
        parse_results = parser_element.parseString(interwiki_prefix)
        self.assertEqual(project, parse_results["project"])
        self.assertEqual(language_code, parse_results["language_code"])
        return

    @hypothesis.given(
        strategies.link.language_code()
    )
    def test_interwiki_prefix_03(self, language_code):
        """Test interwiki_prefix parser element.

        :param str language_prefix: language_code

        interwiki_prefix = language_prefix;
        """
        language_prefix = strategies.link.language_prefix(language_code)
        interwiki_prefix = strategies.link.interwiki_prefix(
            language_prefix_=language_prefix
        )
        parser_element = link._get_interwiki_prefix(
            self.LANGUAGE_CODES, self.PROJECTS
        )
        parse_results = parser_element.parseString(interwiki_prefix)
        self.assertEqual(language_code, parse_results["language_code"])
        return

    @hypothesis.given(
        strategies.link.namespace()
    )
    def test_namespace_00(self, namespace):
        """Test namespace parser element.

        :param str namespace: namespace

        namespace = any namespace;
        """
        parser_element = link._get_namespace(self.NAMESPACES)
        parse_results = parser_element.parseString(namespace)
        self.assertEqual(namespace, parse_results["namespace"])
        return

    @hypothesis.given(
        strategies.link.namespace()
    )
    def test_namespace_prefix_00(self, namespace):
        """Test namespace_prefix parser element.

        :param str namespace: namespace

        namespace_prefix = namespace, ":";
        """
        namespace_prefix = strategies.link.namespace_prefix(namespace)
        parser_element = link._get_namespace_prefix(self.NAMESPACES)
        parse_results = parser_element.parseString(namespace_prefix)
        self.assertEqual(namespace, parse_results["namespace"])
        return

    @hypothesis.given(
        strategies.link.namespace(),
        strategies.link.pagename(1, 8, 16)
    )
    def test_full_pagename_00(self, namespace, pagename):
        """Test full_pagename parser element.

        :param str namespace: namespace
        :param str pagename: pagename

        full_pagename = namespace_prefix, pagename;
        """
        namespace_prefix = strategies.link.namespace_prefix(namespace)
        full_pagename = strategies.link.full_pagename(
            namespace_prefix_=namespace_prefix,
            pagename_=pagename
        )
        parser_element = link._get_full_pagename(self.NAMESPACES)
        parse_results = parser_element.parseString(full_pagename)
        self.assertEqual(namespace, parse_results["namespace"])
        self.assertEqual(pagename, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.link.pagename(1, 8, 16)
    )
    def test_full_pagename_01(self, pagename):
        """Test full_pagename parser element.

        :param str pagename: pagename

        full_pagename = pagename;
        """
        full_pagename = strategies.link.full_pagename(pagename_=pagename)
        parser_element = link._get_full_pagename(self.NAMESPACES)
        parse_results = parser_element.parseString(full_pagename)
        self.assertEqual(pagename, parse_results["pagename"])
        return

    # interwiki_prefix = ..., project;
    # interwiwik_prefix = ..., language_code;
    # full_pagename = namespace, ...;
    # full_pagename = pagename, ...;
    # page_link = [ interwiki_prefix ], full_pagename;
    # page_link = project_prefix, namespace_prefix, pagename;
    # page_link = project_prefix, pagename;
    # page_link = language_prefix, namespace_prefix, pagename;
    # page_link = language_prefix, pagename;

    @hypothesis.given(
        strategies.link.project(),
        strategies.link.namespace(),
        strategies.link.pagename(1, 8, 16)
    )
    def test_page_link_00(self, project, namespace, pagename):
        """Test page_link parser element.

        :param str project: project
        :param str namespace: namespace
        :param str pagename: pagename

        page_link = project_prefix, namespace_prefix, pagename;
        """
        project_prefix = strategies.link.project_prefix(project)
        namespace_prefix = strategies.link.namespace_prefix(namespace)
        interwiki_prefix = strategies.link.interwiki_prefix(
            project_prefix_=project_prefix
        )
        full_pagename = strategies.link.full_pagename(
            pagename,
            namespace_prefix_=namespace_prefix
        )
        page_link = strategies.link.page_link(
            interwiki_prefix_=interwiki_prefix,
            full_pagename_=full_pagename
        )
        parser_element = link._get_page_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(page_link)
        self.assertEqual(project, parse_results["project"])
        self.assertEqual(namespace, parse_results["namespace"])
        self.assertEqual(pagename, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.link.project(),
        strategies.link.pagename(1, 8, 16)
    )
    def test_page_link_01(self, project, pagename):
        """Test page_link parser element.

        :param str project: project
        :param str pagename: pagename

        page_link = project_prefix, pagename;
        """
        project_prefix = strategies.link.project_prefix(project)
        interwiki_prefix = strategies.link.interwiki_prefix(
            project_prefix_=project_prefix
        )
        full_pagename = strategies.link.full_pagename(pagename)
        page_link = strategies.link.page_link(
            interwiki_prefix_=interwiki_prefix,
            full_pagename_=full_pagename
        )
        parser_element = link._get_page_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(page_link)
        self.assertEqual(project, parse_results["project"])
        self.assertEqual(pagename, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.link.language_code(),
        strategies.link.namespace(),
        strategies.link.pagename(1, 8, 16)
    )
    def test_page_link_02(self, language_code, namespace, pagename):
        """Test page_link parser element.

        :param str language_code: language_code
        :param str namespace: namespace
        :param str pagename: pagename

        page_link = language_prefix, namespace_prefix, pagename;
        """
        language_prefix = strategies.link.language_prefix(language_code)
        interwiki_prefix = strategies.link.interwiki_prefix(
            language_prefix_=language_prefix
        )
        namespace_prefix = strategies.link.namespace_prefix(namespace)
        full_pagename = strategies.link.full_pagename(
            pagename,
            namespace_prefix_=namespace_prefix
        )
        page_link = strategies.link.page_link(
            interwiki_prefix_=interwiki_prefix,
            full_pagename_=full_pagename
        )
        parser_element = link._get_page_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(page_link)
        self.assertEqual(language_code, parse_results["language_code"])
        self.assertEqual(namespace, parse_results["namespace"])
        self.assertEqual(pagename, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.link.language_code(),
        strategies.link.pagename(1, 8, 16)
    )
    def test_page_link_03(self, language_code, pagename):
        """Test page_link parser_element.

        :param str language_code: language_code
        :param str pagename: pagename

        page_link = language_prefix, pagename;
        """
        language_prefix = strategies.link.language_prefix(language_code)
        interwiki_prefix = strategies.link.interwiki_prefix(
            language_prefix_=language_prefix
        )
        full_pagename = strategies.link.full_pagename(pagename)
        page_link = strategies.link.page_link(
            interwiki_prefix_=interwiki_prefix,
            full_pagename_=full_pagename
        )
        parser_element = link._get_page_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(page_link)
        self.assertEqual(language_code, parse_results["language_code"])
        self.assertEqual(pagename, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.link.heading(1, 8, 16)
    )
    def test_heading_00(self, heading):
        """Test heading parser element.

        :param str heading: heading

        heading = { any Unicode without "|[]" }-;
        """
        parser_element = link._get_heading()
        parse_results = parser_element.parseString(heading)
        self.assertEqual(heading, parse_results[0])
        return

    @hypothesis.given(
        strategies.link.heading(1, 8, 16)
    )
    def test_section_id_00(self, heading):
        """Test section_id parser element.

        :param str heading: heading

        section_id = "#", heading;
        """
        section_id = strategies.link.section_id(heading)
        parser_element = link._get_section_id()
        parse_results = parser_element.parseString(section_id)
        self.assertEqual(section_id, parse_results[0])
        return

    # page_link = ..., pagename;
    # link = "[[", pagename, "]]";
    # link = "[[", pagename, "]]", label_extension;
    # link = "[[", pagename, section_id, "]]";
    # link = "[[", pagename, "|", "]]";
    # link = "[[", pagename, "|", label, "]]";

    @hypothesis.given(
        strategies.link.pagename(1, 8, 16)
    )
    def test_link_00(self, pagename):
        """Test link parser element.

        :param str pagename: pagename

        link = "[[", page_link, "]]";
        """
        page_link = strategies.link.page_link(full_pagename_=pagename)
        link_ = strategies.link.link(page_link_=page_link)
        parser_element = link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(link_)
        self.assertEqual(pagename, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.link.pagename(1, 8, 16),
        strategies.link.label_extension(1, 8, 16)
    )
    def test_link_01(self, pagename, label_extension):
        """Test link parser element.

        :param str pagename: pagename
        :param str label_extension: label_extension

        link = "[[", pagename, "]]", label_extension;
        """
        page_link = strategies.link.page_link(full_pagename_=pagename)
        link_ = strategies.link.link(
            page_link_=page_link, label_extension_=label_extension
        )
        parser_element = link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(link_)
        self.assertEqual(pagename, parse_results["pagename"])
        self.assertEqual(label_extension, parse_results["label_extension"])
        return

    @hypothesis.given(
        strategies.link.pagename(1, 8, 16),
        strategies.link.heading(1, 8, 16)
    )
    def test_link_02(self, pagename, heading):
        """Test link parser element.

        :param str pagename: pagename
        :param str heading: heading

        link = "[[", pagename, section_id, "]]";
        """
        page_link = strategies.link.page_link(full_pagename_=pagename)
        section_id = strategies.link.section_id(heading)
        link_ = strategies.link.link(
            page_link_=page_link, section_id_=section_id
        )
        parser_element = link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(link_)
        self.assertEqual(pagename, parse_results["pagename"])
        self.assertEqual(section_id, parse_results[2])
        return

    @hypothesis.given(
        strategies.link.pagename(1, 8, 16),
    )
    def test_link_03(self, pagename):
        """Test link parser element.

        :param str pagename: pagename

        link = "[[", pagename, "|", "]]";
        """
        page_link = strategies.link.page_link(full_pagename_=pagename)
        link_ = strategies.link.link(page_link_=page_link, pipe="|")
        parser_element = link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(link_)
        self.assertEqual(pagename, parse_results["pagename"])
        return

    @hypothesis.given(
        strategies.link.pagename(1, 8, 16),
        strategies.link.label(1, 8, 16)
    )
    def test_link_04(self, pagename, label):
        """Test link parser element.

        :param str pagename: pagename
        :param str label: label

        link = "[[", pagename, "|", label, "]]";
        """
        page_link = strategies.link.page_link(full_pagename_=pagename)
        link_ = strategies.link.link(
            page_link_=page_link, pipe="|", label_=label
        )
        parser_element = link.get_link(
            self.LANGUAGE_CODES, self.PROJECTS, self.NAMESPACES
        )
        parse_results = parser_element.parseString(link_)
        self.assertEqual(pagename, parse_results["pagename"])
        self.assertEqual(label, parse_results["label"])
        return

    @hypothesis.given(
        strategies.link.uri_reserved_character()
    )
    def test_uri_character_00(self, uri_reserved_character):
        """Test URI character regular expression.

        :param str uri_reserved_character: URI reserved character

        uri_character = uri_reserved_character;
        """
        parser_element = link._get_uri_character()
        parse_results = parser_element.parseString(uri_reserved_character)
        self.assertEqual(uri_reserved_character, parse_results[0])
        return

    @hypothesis.given(
        strategies.link.uri_unreserved_character()
    )
    def test_uri_character_01(self, uri_unreserved_character):
        """Test URI character regular expression.

        :param str uri_unreserved_character: URI unreserved character

        uri_character = uri_unreserved_character;
        """
        parser_element = link._get_uri_character()
        parse_results = parser_element.parseString(uri_unreserved_character)
        self.assertEqual(uri_unreserved_character, parse_results[0])
        return

    @hypothesis.given(
        strategies.link.html_encoded()
    )
    def test_uri_character_02(self, html_encoded):
        """Test HTML encoded character regular expression.

        :param str html_encoded: HTML encoded character

        uri_character = html_encoded;
        """
        parser_element = link._get_uri_character()
        parse_results = parser_element.parseString(html_encoded)
        self.assertEqual(html_encoded, parse_results[0])
        return

    @hypothesis.given(
        strategies.link.url_scheme(1, 4, 8)
    )
    def test_url_scheme_00(self, url_scheme):
        """Test URL scheme regular expression.

        :param str url_scheme: URL scheme

        url_scheme = letter, { letter | digit | any of "+-." };
        """
        parser_element = link._get_url_scheme()
        parse_results = parser_element.parseString(url_scheme)
        self.assertEqual(url_scheme, parse_results[0])
        return

    @hypothesis.given(
        strategies.link.url((1, 4, 8), (0, 4, 8))
    )
    def test_url_00(self, url):
        """Test URL parser element.

        url = url_scheme, ":", [ "//" ], { uri_character };
        """
        parser_element = link.get_url()
        parse_results = parser_element.parseString(url)
        self.assertEqual(url, parse_results["url"])
        return

    @hypothesis.given(
        strategies.link.anchor(1, 8, 16)
    )
    def test_anchor_00(self, anchor):
        """Test anchor parser element.

        anchor = { any Unicode character without "[]" }-;
        """
        parser_element = link._get_anchor()
        parse_results = parser_element.parseString(anchor)
        self.assertEqual(anchor, parse_results["anchor"])
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.link.url((1, 4, 8), (1, 4, 8))
    )
    def test_external_link_00(self, data, url):
        """Test external link parser element.

        :param str url: URL

        external_link = "[", url, "]";
        """
        external_link = data.draw(strategies.link.external_link(url))
        parser_element = link.get_external_link()
        parse_results = parser_element.parseString(external_link)
        self.assertEqual(url, parse_results["url"])
        return

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.link.url((1, 4, 8), (1, 4, 8)),
        strategies.link.anchor(1, 8, 16)
    )
    def test_external_link_01(self, data, url, anchor):
        """Test external link parser element.

        :param str url: URL
        :param str anchor: anchor

        external_link = "[", url, anchor, "]";
        """
        external_link = data.draw(
            strategies.link.external_link(url, anchor_=anchor)
        )
        parser_element = link.get_external_link()
        parse_results = parser_element.parseString(external_link)
        self.assertEqual(url, parse_results["url"])
        self.assertEqual(anchor, parse_results["anchor"])
        return
