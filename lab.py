#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Простенький будильник

Наберите --help для помощи.

"""

import sys
import unittest
from argparse import ArgumentParser, RawTextHelpFormatter, REMAINDER

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as dateparse
from pytimeparse import parse as deltaparse

__version__ = "0.1"

def main():
    parser = parse_args(sys.argv[1:])


def parse_args(args):
    parser = ArgumentParser(description=__doc__)

    parser.add_argument('--version', action='version',
            version="%%(prog)s v%s" % __version__)

    return parser

class TestDoc(unittest.TestCase):
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
            description=__doc__)

    def test_name(self):
        self.assertEqual(self.parser.prog, 'lab.py')

    def test_description(self):
        self.assertNotEqual(self.parser.description, '')
        self.assertNotEqual(self.parser.description.strip(), '')
        self.assertNotEqual(self.parser.description.lstrip(), '')
        self.assertNotEqual(self.parser.description.rstrip(), '')


class TestIn(unittest.TestCase):

    def test_null(self):
        parser = parse_args([])
        self.assertTrue(parser is not None)


if __name__ == '__main__':
    unittest.main()
#    main()
