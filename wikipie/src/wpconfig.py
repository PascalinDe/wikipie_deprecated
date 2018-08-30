#    This file is part of WikiPie 0.x.
#    Copyright (C) 2017  Carine Dengler, Heidelberg University (DBS)
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
:synopsis: Command-line interface and configuration file handling.
"""


# standard library imports
import argparse
import multiprocessing
import logging
import logging.config
import configparser

# third party imports
# library specific imports


CONF = "conf/{}"
LOGGING_CONFIG = CONF.format("logging.ini")
CONFIG = CONF.format("config.ini")
LOCALIZATION = CONF.format("{}.ini")


def get_logging_config(file_=LOGGING_CONFIG):
    """Get logging configuration.

    :param str file_: logging configuration file
    """
    logging.config.fileConfig(file_)
    return


def get_config(file_=CONFIG):
    """Get configuration.

    :param str file_: file

    :returns: config
    :rtype: ConfigParser
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.read_file(open(file_))
    return config


def _get_command_line_parser():
    """Get command-line parser.

    :returns: command-line parser
    :rtype: ArgumentParser
    """
    parser = argparse.ArgumentParser(prog="WikiPie 0.x")
    parser.add_argument("xml", help="XML file")
    parser.add_argument(
        "-c", "--categories",
        action="store_true",
        default=False,
        help="keep categories in text"
    )
    parser.add_argument(
        "-p", "--processes",
        default=1,
        type=int,
        choices=list(range(1, multiprocessing.cpu_count())),
        help="number of processes"
    )
    parser.add_argument(
        "-t", "--templates",
        action="store_true",
        default=False,
        help="process templates"
    )
    return parser


def get_command_line_args():
    """Get command-line arguments.

    :returns: args
    :rtype: Namespace
    """
    parser = _get_command_line_parser()
    args = parser.parse_args()
    return args


def get_localization(file_):
    """Get localization.

    :param str file_: file

    :returns: localization
    :rtype: ConfigParser
    """
    localization = configparser.ConfigParser(
        comment_prefixes="%", converters={"list": lambda x: x.split(",")}
    )
    localization.read_file(open(file_))
    return localization
