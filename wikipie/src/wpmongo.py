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
:synopsis: mongoDB module, handles mongoDB interface.
"""


# standard library imports
import multiprocessing

# third party imports
import pymongo

# library specific imports


def _get_page_record(page):
    """Get page record.

    :param Page page: page

    :returns: page record
    :rtype: dict
    """
    record = {                      # article OR template
        "title": page.title,
        "_id": int(page.pageid),
        "redirect": page.redirect,
        "revid": int(page.revid),
        "content": page.text,
    }
    if hasattr(page, "categories"):   # article
        record["category"] = page.categories
    if hasattr(page, "params"):     # template
        record["params"] = page.params
    return record


def _get_inclusion_record(pageid, inclusion):
    """Get inclusion record.

    :param str pageid: Wikipedia page ID
    :param dict inclusion: inclusion

    :returns: inclusion record
    :rtype: dict
    """
    record = inclusion
    record["WP_page_id"] = int(pageid)
    return record


def _get_link_record(pageid, link):
    """Get link record.

    :param str pageid: Wikipedia page ID
    :param dict link: link

    :returns: link record
    :rtype: dict
    """
    record = link
    record["WP_page_id"] = int(pageid)
    record["sen_id"] = -1
    record["start_sen"] = -1
    record["end_sen"] = -1
    return record


class WPMongo(object):
    """mongoDB interface.

    :cvar int MAX_BULK_SIZE: maximum bulk operation size
    :ivar int pid: process ID
    :ivar str db: mongoDB
    :ivar str host: host
    :ivar str port: port
    """
    # https://docs.mongodb.com/manual/reference/limits/#operations
    MAX_BULK_SIZE = 1000

    def __init__(self, pid, db, host, port, username="", password=""):
        """Connect to mongoDB.

        :param int pid: process ID
        :param str db: mongoDB
        :param str host: host
        :param int port: port
        :param str username: username
        :param str password: password
        """
        try:
            logger = multiprocessing.get_logger().getChild(__name__)
            logger.info(
                "worker %s connects to mongoDB %s (%s, %s)",
                pid, db, host, port
            )
            self.pid = pid
            self.db = db
            self.host = host
            self.port = port
            if username and password:
                self.client = pymongo.MongoClient(
                    host=host, port=port, username=username, password=password
                )
            else:
                self.client = pymongo.MongoClient(host=host, port=port)
        except:
            logger.exception(
                "worker %s failed to connect to mongoDB %s (%s, %s)",
                self.pid, self.db, self.host, self.port
            )
            raise
        return

    def insert_pages(self, pages, collection="article"):
        """Insert page record.

        :param list pages: pages
        :param str collection: collection
        """
        try:
            logger = multiprocessing.get_logger().getChild(__name__)
            records = [_get_page_record(page) for page in pages]
            logger.debug("insert %d pages", len(records))
            self.client[self.db][collection].insert_many(records)
        except pymongo.errors.PyMongoError:
            logger.error("failed to insert pages")
        return

    def insert_inclusions(self, pageid, inclusions, collection="inclusion"):
        """Insert inclusion records.

        :param str pageid: Wikipedia page ID
        :param dict inclusions: inclusions
        :param str collection: collection
        """
        try:
            logger = multiprocessing.get_logger().getChild(__name__)
            records = [
                _get_inclusion_record(pageid, inclusion)
                for inclusion in inclusions
            ]
            logger.debug("insert %d inclusions (%s)", len(records), pageid)
            self.client[self.db][collection].insert_many(records)
        except pymongo.errors.PyMongoError:
            logger.error("failed to insert inclusions (%s)", pageid)
        return

    def insert_links(self, pageid, links, collection="IWL"):
        """Insert links.

        :param str pageid: Wikipedia page ID
        :param dict links: links
        :param str collection: collection
        """
        try:
            logger = multiprocessing.get_logger().getChild(__name__)
            records = [_get_link_record(pageid, link) for link in links]
            logger.debug("insert %d links (%s)", len(records), pageid)
            self.client[self.db][collection].insert_many(records)
        except pymongo.errors.PyMongoError:
            logger.error("failed to insert links (%s)", pageid)
        return

    def close(self):
        """Close connection to mongoDB."""
        try:
            logger = multiprocessing.get_logger().getChild(__name__)
            self.client.close()
        except pymongo.errors.PyMongoError:
            logger.exception(
                "worker %s failed to close connection to mongoDB %s (%s, %s)",
                self.pid, self.db, self.host, self.port
            )
            raise
        logger.info(
            "worker %s closed connection to mongoDB %s (%s, %s)",
            self.pid, self.db, self.host, self.port
        )
        return
