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
:synopsis: Test template wiki markup parse actions.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from tests.markupparser.parser_elements import strategies
from src.wpmarkupparser.parser_elements import template


class TestTemplate(unittest.TestCase):
    """Test template parser template parse actions."""

    @hypothesis.given(
        strategies.template.template(1, 8, 16)
    )
    def test_normalize_template_00(self, template_):
        """Test normalize_template (parseString).

        :param str template: template
        """
        # template contains at least one non-whitespace character
        hypothesis.assume(template_.strip())
        parser_element = template._get_pagename(parse_actions=True)
        parse_results = parser_element.parseString(template_)
        if len(template_) > 1:
            template_ = template_[0].upper() + template_[1:]
        else:
            template_ = template_[0].upper()
        template_ = template_.strip()
        self.assertEqual(template_, parse_results["pagename"])
        return
