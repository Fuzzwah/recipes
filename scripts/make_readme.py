#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
SYNOPSIS

    python make_readme.py [-h,--help] [-l,--log] [--debug]

DESCRIPTION

    Builds the readme.md file by reading through the recipe files

AUTHOR

    Robert Crouch (rob.crouch@gmail.com)

VERSION

    $Id$
"""

__program__ = "Build recipe repo readme"
__author__ = "Robert Crouch (rob.crouch@gmail.com)"
__copyright__ = "Copyright (C) 2018- Robert Crouch"
__license__ = "LGPL 3.0"
__version__ = "v0.180421a"

import os
import sys
import argparse
import logging, logging.handlers
import configobj

class App(object):
    """ The main class of your application
    """

    def __init__(self, log, args, config):
        self.log = log
        self.args = args
        self.config = config
        self.version = "{}: {}".format(__program__, __version__)

        self.log.info(self.version)
        if self.args.debug:
            print(self.version)

    def build_readme(self):
        """ Builds the readme
        """

        readme = open('README.md', 'w')
        recipes = [f for f in sorted(os.listdir()) if os.path.isfile(f)]
        for r_file in recipes:
            extension = os.path.splitext(r_file)[1][1:]
            if r_file != "README.md" and extension == "md":
                r_file = r_file[:-3]
                r_name = r_file.replace("_", " ")
                readme.write("### [{0}]({1}.md)\n![](https://raw.githubusercontent.com/fuzzwah/recipes/images/pics/thumbs/{1}.jpg)\n".format(r_name, r_file))

        return True


def parse_args(argv):
    """ Read in any command line options and return them
    """

    # Define and parse command line arguments
    parser = argparse.ArgumentParser(description=__program__)
    parser.add_argument("--logfile", help="file to write log to", default="%s.log" % __program__)
    parser.add_argument("--configfile", help="use a different config file", default="config.ini")
    parser.add_argument("--debug", action='store_true', default=False)

    # uncomment this if you want to force at least one command line option
    # if len(sys.argv)==1:
    #   parser.print_help()
    #   sys.exit(1)

    args = parser.parse_args()

    return args

def setup_logging(args):
    """ Everything required when the application is first initialized
    """

    basepath = os.path.abspath(".")

    # set up all the logging stuff
    LOG_FILENAME = os.path.join(basepath, "%s.log" % args.logfile)

    if args.debug:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

    # Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
    # Give the logger a unique name (good practice)
    log = logging.getLogger(__name__)
    # Set the log level to LOG_LEVEL
    log.setLevel(LOG_LEVEL)
    # Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
    # Format each log message like this
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    # Attach the formatter to the handler
    handler.setFormatter(formatter)
    # Attach the handler to the logger
    log.addHandler(handler)

def main(raw_args):
    """ Main entry point for the script.
    """

    # call function to parse command line arguments
    args = parse_args(raw_args)

    # setup logging
    setup_logging(args)

    # connect to the logger we set up
    log = logging.getLogger(__name__)

    if not os.path.isfile(args.configfile):
        config = configobj.ConfigObj()
        config.filename = args.configfile

        config['Section'] = {}
        config['Section']['item'] = 'something'
        config.write()

    # try to read in the config
    try:
        config = configobj.ConfigObj(args.configfile)

    except (IOError, KeyError, AttributeError) as e:
        print("Unable to successfully read config file: %s" % args.configfile)
        sys.exit(0)

    # fire up our base class and get this app cranking!
    app = App(log, args, config)

    # things that the app does go here:
    app.build_readme()

    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))