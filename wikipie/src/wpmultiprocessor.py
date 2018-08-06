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
:synopsis: Multiprocessing module, handles parallel processing.
"""


# standard library imports
import os
import sys
import logging
import multiprocessing

# third party imports

# library specific imports
import src.wpmongo
import src.wpmarkupparser


class Multiprocessor(object):
    """Parallel processing.

    :ivar int processes: number of processes
    :ivar str host: host
    :ivar str port: port
    :ivar str db: mongoDB
    :ivar str username: username
    :ivar str password: password
    :ivar Parser parser: parser
    :ivar Queue queue: queue
    """

    def __init__(self, args, config, pages, localization=None):
        """Initialize parallel processor.

        :param Namespace args: command-line arguments
        :param ConfigParser config: config
        :param generator pages: pages
        :param Parser parser: parser
        """
        self.args = args
        self.localization = localization
        self.processes = args.processes
        self.host = config["mongoDB"]["host"]
        self.port = config["mongoDB"].getint("port")
        self.db = config["mongoDB"]["db"]
        self.username = config["mongoDB"]["username"]
        self.password = config["mongoDB"]["password"]
        self.queue = multiprocessing.JoinableQueue()
        for page in pages:
            self.queue.put(page)
        # put sentinels on the queue
        for _ in range(self.processes):
            self.queue.put(None)
        return

    def _worker(self):
        """Worker."""
        raise NotImplementedError

    def process(self):
        """Process pages."""
        try:
            logger = multiprocessing.get_logger().getChild(__name__)
            workers = []
            for _ in range(self.processes):
                workers.append(
                    multiprocessing.Process(target=self._worker, daemon=True)
                )
                workers[-1].start()
            self.queue.join()
            for worker in workers:
                worker.join()
        except Exception:
            logger.exception("failed to process pages")
            raise
        return


class TemplateMultiprocessor(Multiprocessor):
    """Parallel processing (templates)."""

    def _worker(self):
        """Worker."""
        logger = multiprocessing.get_logger().getChild(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        pid = os.getpid()
        wpmongo = src.wpmongo.WPMongo(
            pid, self.db, self.host, self.port, self.username, self.password
        )
        parser = src.wpmarkupparser.parser.TemplateParser(
            localization=self.localization
        )
        pages = []
        for page in iter(self.queue.get, None):
            logger.info(
                "worker %s processes template %s", pid, page.title
            )
            page = parser.parse(page)
            pages.append(page)
            # insert page records
            if len(pages) == wpmongo.MAX_BULK_SIZE:
                wpmongo.insert_pages(pages)
                pages = []
            self.queue.task_done()
        # insert leftover page records
        if pages:
            wpmongo.insert_pages(pages)
        logger.info("worker %s emptied queue", pid)
        self.queue.task_done()
        logger.info("worker %s unblocked queue", pid)
        return


class ArticleMultiprocessor(Multiprocessor):
    """Parallel processing (articles)."""

    def _worker(self):
        """Worker."""
        logger = multiprocessing.get_logger().getChild(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        pid = os.getpid()
        wpmongo = src.wpmongo.WPMongo(
            pid, self.db, self.host, self.port, self.username, self.password
        )
        parser = src.wpmarkupparser.parser.ArticleParser(
            self.args, localization=self.localization
        )
        pages = []
        for page in iter(self.queue.get, None):
            logger.info(
                "worker %s processes article %s", pid, page.title
            )
            page = parser.parse(page)
            pages.append(page)
            # insert page records
            if len(pages) == wpmongo.MAX_BULK_SIZE:
                wpmongo.insert_pages(pages)
                pages = []
            if page.inclusions:
                wpmongo.insert_inclusions(page.pageid, page.inclusions)
            if page.links:
                wpmongo.insert_links(page.pageid, page.links)
            self.queue.task_done()
        # insert leftover records
        if pages:
            wpmongo.insert_pages(pages)
        logger.info("worker %s emptied queue", pid)
        self.queue.task_done()
        logger.info("worker %s unblocked queue", pid)
        wpmongo.close()
        return
