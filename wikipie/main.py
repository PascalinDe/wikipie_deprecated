#    WikiPie 0.x
#    Copyright (C) 2017  Carine Dengler
#
#    This program is free software: you can redistribute it and/or modify
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
:synopsis: Main routine, manages pipeline.
"""


# standard library imports
import time
import logging

# third party imports

# library specific imports
import src.wppage
import src.wpconfig
import src.wpxmlparser
import src.wpmultiprocessor
import src.wpmarkupparser.parser


def _get_templates(pages):
    """Get templates.

    :param generator pages: template pages
    """
    for page in pages:
        title = page["title"]
        pageid = page["id"]
        redirect = page["redirect"]
        for revision in page["revision"]:
            template = src.wppage.Template(
                title, pageid, redirect,
                revision["id"], revision["text"]["text"]
            )
            yield template


def _get_articles(pages):
    """Get articles.

    :param generator pages: article pages
    """
    for page in pages:
        title = page["title"]
        pageid = page["id"]
        redirect = page["redirect"]
        for revision in page["revision"]:
            article = src.wppage.Article(
                title, pageid, redirect,
                revision["id"], revision["text"]["text"]
            )
            yield article


def process_templates(args, config, pages, localization=None):
    """Process templates.

    :param Namespace args: args
    :param ConfigParser config: config
    :param generator pages: template pages
    """
    try:
        logger = logging.getLogger()
        templates = _get_templates(pages)
        multiprocessor = src.wpmultiprocessor.TemplateMultiprocessor(
            args, config, templates, localization=localization
        )
        multiprocessor.process()
    except Exception:
        logger.exception("failed to process templates")
        raise
    return


def process_articles(args, config, pages, localization=None):
    """Process articles.

    :param Namespace args: args
    :param ConfigParser config: config
    :param generator pages: article pages
    :param ConfigParser localization: localization
    """
    try:
        logger = logging.getLogger()
        articles = _get_articles(pages)
        multiprocessor = src.wpmultiprocessor.ArticleMultiprocessor(
            args, config, articles, localization=localization
        )
        multiprocessor.process()
    except Exception:
        logger.exception("failed to process articles")
        raise
    return


def main():
    """main function."""
    try:
        src.wpconfig.get_logging_config()
    except Exception:
        print("failed to get logging configuration")
        raise SystemExit
    logger = logging.getLogger()
    logger.info("got logging configuration")
    logger.info("get configuration")
    try:
        config = src.wpconfig.get_config()
    except Exception:
        logger.exception("failed to get configuration")
        raise SystemExit
    logger.info("got configuration")
    logger.info("get command-line arguments")
    try:
        args = src.wpconfig.get_command_line_args()
    except Exception:
        raise SystemExit
    logger.info("got command-line arguments")
    logger.info("parse XML file %s", args.xml)
    time0 = time.time()
    try:
        wpxmlparser = src.wpxmlparser.WPXMLParser(args.xml)
    except Exception:
        logger.exception("failed to parse XML file %s", args.xml)
        raise SystemExit
    time1 = time.time() - time0
    logger.info("parsed XML file %s in %f sec", args.xml, time1)
    logger.info("get XML file %s content language", args.xml)
    try:
        # get XML file content language
        lang = wpxmlparser.find_language_attrib()
    except Exception:
        logger.exception(
            "failed to get XML file %s content language", args.xml
        )
        lang = "en"
        logger.warning(
            "falling back to default content language (%s)", lang
        )
    logger.info("got XML file content language (%s)", lang)
    logger.info("get localization (%s)", lang)
    if lang == "en":
        localization = None
    else:
        try:
            # get localization
            localization = src.wpconfig.get_localization(
                src.wpconfig.LOCALIZATION.format(lang)
            )
        except Exception:
            logger.warning("failed to get localization (%s)", lang)
            lang = "en"
            localization = None
            logger.warning("falling back to default localization (%s)", lang)
    logger.info("got localization (%s)", lang)
    if args.templates:
        logger.info("process templates")
        time0 = time.time()
        try:
            # find pages (title, namespace, ID, revision)
            pages = wpxmlparser.find_page_elements(
                prop=("title", "ns", "id", "redirect", "revision")
            )
            # find template pages (namespace number 10)
            pages = (page for page in pages if page["ns"] == "10")
        except Exception:
            logger.warning("failed to find template pages")
            raise SystemExit
        try:
            process_templates(args, config, pages)
        except Exception:
            logger.exception("failed to process templates")
            raise SystemExit
        time1 = time.time() - time0
        logger.info("processed templates in %f sec", time1)
    logger.info("process articles")
    time0 = time.time()
    try:
        # find pages (title, namespace, ID, revision)
        pages = wpxmlparser.find_page_elements(
            prop=("title", "ns", "id", "redirect", "revision")
        )
        # find article pages (namespace number 0)
        pages = (page for page in pages if page["ns"] == "0")
    except Exception:
        logger.warning("failed to find article pages")
        raise SystemExit
    try:
        process_articles(
            args, config, pages, localization=localization
        )
    except Exception:
        logger.exception("failed to process articles")
        raise SystemExit
    time1 = time.time() - time0
    logger.info("processed articles in %f sec", time1)
    return


if __name__ == "__main__":
    main()
