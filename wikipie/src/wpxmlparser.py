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
:synopsis: Wikipedia export file parser.
"""


# standard library imports
import logging
import bz2

# third party imports
import lxml.etree

# library specific imports


class WPXMLParser(object):
    """Wikipedia export file parser.

    :cvar dict NSMAP: namespaces

    :ivar ElementTree tree: tree
    :ivar str xml: Wikipedia export file
    """
    # https://stackoverflow.com/questions/31250641/python-lxml-using-the-xmllang-attribute-to-retrieve-an-element
    NSMAP = {"xml": "http://www.w3.org/XML/1998/namespace"}

    def __init__(self, xml):
        """Parse Wikipedia export file.

        :param str xml: Wikipedia export file
        """
        try:
            logger = logging.getLogger().getChild(__name__)
            logger.info("parse Wikipedia export file %s", xml)
            if xml.endswith("bz2"):
                logger.info("unzip bz2 file")
                with bz2.open(xml) as file_:
                    self.tree = lxml.etree.parse(file_)
            else:
                with open(xml) as file_:
                    self.tree = lxml.etree.parse(file_)
        except:
            logger.exception("failed to parse Wikipedia export file %s", xml)
            raise
        return

    def find_language_attrib(self):
        """Find language attribute.

        :returns: language attribute
        :rtype: str
        """
        try:
            logger = logging.getLogger().getChild(__name__)
            logger.info("find language attribute")
            attrib = "{{{}}}lang".format(self.NSMAP["xml"])
            language_attrib = self.tree.getroot().attrib[attrib]
        except:
            logger.exception("failed to find language attribute")
            raise
        return language_attrib

    def find_page_elements(self, prop=("title", "ns", "id")):
        """Find page elements.

        :param list prop: properties

        :returns: page elements
        :rtype: generator
        """
        try:
            logger = logging.getLogger().getChild(__name__)
            logger.info("find pages")
            page_elements = self.tree.iterfind("{*}page")
            generator = self._find_page_elements(prop, page_elements)
        except:
            logger.exception("failed to find pages")
            raise
        return generator

    def _find_page_elements(self, prop, page_elements):
        """Find page elements.

        :param list prop: properties
        :param generator page_elements: page elements

        :returns: page elements
        :rtype: generator
        """
        for page_element in page_elements:
            yield self._find_page_element(prop, page_element)

    def _find_page_element(self, prop, page_element):
        """Find page element.

        :param list prop: properties
        :param Element page_element: page element

        :returns: page
        :rtype: dict
        """
        page = {}
        # total number: 1
        if "title" in prop:
            title_element = page_element.find("{*}title")
            if title_element.text is not None:
                page["title"] = title_element.text
            else:
                page["title"] = ""
        # total number: 1
        if "ns" in prop:
            ns_element = page_element.find("{*}ns")
            if ns_element.text is not None:
                page["ns"] = ns_element.text
            else:
                page["ns"] = ""
        # total number: 1
        if "id" in prop:
            pageid_element = page_element.find("{*}id")
            if pageid_element.text is not None:
                page["id"] = pageid_element.text
            else:
                page["id"] = ""
        if "redirect" in prop:
            redirect_element = page_element.find("{*}redirect")
            if redirect_element is not None:
                page["redirect"] = redirect_element.attrib["title"]
            else:
                page["redirect"] = ""
        # total number 0-
        if "revision" in prop:
            revision_elements = page_element.iterfind("{*}revision")
            page["revision"] = list(
                self._find_revision_elements(revision_elements)
            )
        return page

    def _find_revision_elements(self, revision_elements):
        """Find revision elements.

        :param generator revision_elements: revision elements

        :returns: revision elements
        :rtype: generator
        """
        for revision_element in revision_elements:
            yield self._find_revision_element(revision_element)

    def _find_revision_element(self, revision_element):
        """Find revision element.

        :param Element revision_element

        :returns: revision
        :rtype: dict
        """
        revision = {}
        # total number: 1
        id_element = revision_element.find("{*}id")
        if id_element.text is not None:
            revision["id"] = id_element.text
        else:
            revision["id"] = ""
        # total number: 0-1
        parentid_element = revision_element.find("{*}parentid")
        if parentid_element is not None:
            if parentid_element.text is not None:
                revision["parentid"] = parentid_element.text
            else:
                revision["parentid"] = ""
        else:
            revision["parentid"] = ""
        # total number: 1
        timestamp_element = revision_element.find("{*}timestamp")
        if timestamp_element.text is not None:
            revision["timestamp"] = timestamp_element.text
        else:
            revision["timestamp"] = ""
        # total number: 1
        contributor_element = revision_element.find("{*}contributor")
        revision["contributor"] = self._find_contributor_element(
            contributor_element
        )
        # total number: 0-1
        minor_element = revision_element.find("{*}minor")
        if minor_element is not None:
            if minor_element.text is not None:
                revision["minor"] = minor_element.text
            else:
                revision["minor"] = ""
        else:
            revision["minor"] = ""
        # total number: 0-1
        comment_element = revision_element.find("{*}comment")
        if comment_element is not None:
            if comment_element.text is not None:
                revision["comment"] = comment_element.text
            else:
                revision["comment"] = ""
        else:
            revision["comment"] = ""
        # total number: 1
        model_element = revision_element.find("{*}model")
        if model_element.text is not None:
            revision["model"] = model_element.text
        else:
            revision["model"] = ""
        # total number: 1
        format_element = revision_element.find("{*}format")
        if format_element.text is not None:
            revision["format"] = format_element.text
        else:
            revision["format"] = ""
        # total number: 1
        text_element = revision_element.find("{*}text")
        revision["text"] = self._find_text_element(text_element)
        # total number: 1
        sha1_element = revision_element.find("{*}sha1")
        if sha1_element.text is not None:
            revision["sha1"] = sha1_element.text
        else:
            revision["sha1"] = ""
        return revision

    def _find_contributor_element(self, contributor_element):
        """Find contributor.

        :param Element contributor_element: contributor element

        :returns: contributor
        :rtype: dict
        """
        contributor = {}
        # total number: 0-1
        username_element = contributor_element.find("{*}username")
        if username_element is not None:
            if username_element.text is not None:
                contributor["username"] = username_element.text
            else:
                contributor["username"] = ""
        else:
            contributor["username"] = ""
        # total number: 0-1
        id_element = contributor_element.find("{*}id")
        if id_element is not None:
            if id_element.text is not None:
                contributor["id"] = id_element.text
            else:
                contributor["id"] = ""
        else:
            contributor["id"] = ""
        # total number: 0-1
        ip_element = contributor_element.find("{*}ip")
        if ip_element is not None:
            if ip_element.text is not None:
                contributor["ip"] = ip_element.text
            else:
                contributor["ip"] = ""
        else:
            contributor["ip"] = ""
        # attribute (optional)
        if "deleted" in contributor_element.attrib:
            contributor["deleted"] = contributor_element.attrib["deleted"]
        else:
            contributor["deleted"] = ""
        return contributor

    def _find_text_element(self, text_element):
        """Find text.

        :param Element text_element: text element

        :returns: text
        :rtype: dict
        """
        text = {}
        if text_element.text is not None:
            text["text"] = text_element.text
        else:
            text["text"] = ""
        # attribute (optional)
        if "deleted" in text_element.attrib:
            text["deleted"] = text_element.attrib["deleted"]
        else:
            text["deleted"] = ""
        # attribute (optional)
        if "id" in text_element.attrib:
            text["id"] = text_element.attrib["id"]
        else:
            text["id"] = ""
        # attribute (optional)
        if "bytes" in text_element.attrib:
            text["bytes"] = text_element.attrib["bytes"]
        else:
            text["bytes"] = ""
        return text
