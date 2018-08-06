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
:synopsis: Page module, provides containers for Wikipedia pages.
"""


# standard library imports
# third party imports
# library specific imports


class Page(object):
    """Wikipedia page.

    :ivar str title: title
    :ivar str pageid: page ID
    :ivar str redirect: title
    :ivar str revid: revision ID
    :ivar str text: text
    """

    def __init__(self, title, pageid, redirect, revid, text):
        """Initialize Wikipedia page.

        :param str title: title
        :param str pageid: page ID
        :param str redirect: title
        :param str revid: revision ID
        :param str text: text
        """
        self.title = title
        self.pageid = pageid
        self.redirect = redirect
        self.revid = revid
        self.text = text
        return


class Article(Page):
    """Article.

    :ivar list inclusions: inclusions
    :ivar list links: links
    :ivar list categories: categories
    """

    def __init__(self, title, pageid, redirect, revid, text):
        """Initialize article.

        :param str title: title
        :param str pageid: page ID
        :param str redirect: title
        :param str revid: revision ID
        :param str text: text
        """
        super().__init__(title, pageid, redirect, revid, text)
        self.inclusions = []
        self.links = []
        self.categories = []
        return


class Template(Page):
    """Template.

    :ivar list params: parameters
    """

    def __init__(self, title, pageid, redirect, revid, text):
        """Initialize template.

        :param str title: title
        :param str pageid: page ID
        :param str redirect: title
        :param str revid: revision ID
        :param str text: text
        """
        super().__init__(title, pageid, redirect, revid, text)
        self.params = []
        return
