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
:synopsis:
"""


# standard library imports
import unittest

# third party imports
import pymongo

# library specific imports


# mongoDB
HOST = "localhost"
PORT = 27017

# mongoDB name
DB = "dev"

# collection name(s)
TEMPLATE = "template"
ARTICLE = "article"
INCLUSION = "inclusion"
LINK = "IWL"


class TestTemplateParser(unittest.TestCase):
    """Test template parser."""
    CLIENT = pymongo.MongoClient()

    def test_params_00(self):
        """Test params."""
        page = self.CLIENT[DB][TEMPLATE].aggregate([{"$sample": {"size": 1}}])
        page = list(page)[0]
        params = page["params"]
        for param in params:
            start_doc, end_doc = param["start_doc"], param["end_doc"]
            self.assertEqual(
                param["covered_text"], page["content"][start_doc:end_doc]
            )
        return


class TestArticleParser(unittest.TestCase):
    """Test article parser."""
    CLIENT = pymongo.MongoClient()

    def test_links_00(self):
        """Test links."""
        page = self.CLIENT[DB][ARTICLE].aggregate([{"$sample": {"size": 1}}])
        page = list(page)[0]
        links = self.CLIENT[DB][LINK].find({"WP_page_id": page["_id"]})
        for link in links:
            start_doc, end_doc = link["start_doc"], link["end_doc"]
            covered_text = link["covered_text"]
            self.assertEqual(page["content"][start_doc:end_doc], covered_text)
        return

    def test_inclusions_00(self):
        """Test inclusions."""
        page = self.CLIENT[DB][ARTICLE].aggregate([{"$sample": {"size": 1}}])
        page = list(page)[0]
        inclusions = self.CLIENT[DB][INCLUSION].find(
            {"WP_page_id": page["_id"]}
        )
        for inclusion in inclusions:
            start_doc, end_doc = inclusion["start_doc"], inclusion["end_doc"]
            covered_text = inclusion["template"]
            self.assertEqual(page["content"][start_doc:end_doc], covered_text)
        return
