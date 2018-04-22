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
    args = parser.parse_args()


def parse_args(args):
    parser = ArgumentParser(description=__doc__)

    parser.add_argument('--version', action='version',
            version="%%(prog)s v%s" % __version__)

    subparsers = parser.add_subparsers(description='time to wake up')

    parser_in = subparsers.add_parser('in', help='wake up after some time left. For example: in 5 minutes')
    parser_in.set_defaults(parser=parse_in)
    parser_in.add_argument('timespec_list', nargs=REMAINDER)

    parser_at = subparsers.add_parser('at',help='wake up at specific time. For example: at 5 AM' )
    parser_at.set_defaults(parser=parse_at)
    parser_at.add_argument('timespec_list', nargs=REMAINDER)

    return parser

def parse_in(timespec):
    return timedelta(seconds=deltaparse(timespec))

def parse_at(timespec):
    yield


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
    def test_time1(self):
        parser = parse_args(['in 2 seconds'])
    def test_time2(self):
        parser = parse_args(['in 222222 minutes'])
    def test_time3(self):
        parser = parse_args(['in 5 hours'])



if __name__ == '__main__':
    unittest.main()
#    main()
