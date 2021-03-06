#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Простенький будильник

Наберите --help для помощи.

"""

from __future__ import (absolute_import, division, print_function,
                        with_statement, unicode_literals)

import sys
import unittest
from argparse import ArgumentParser, RawTextHelpFormatter, REMAINDER
import subprocess
import time

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as dateparse
from pytimeparse import parse as deltaparse

import os.path
import alsaaudio

__version__ = "0.1"

SAFETY_LIMIT = timedelta(hours=15)
ALARM_CMD = ['mpv', '-loop=inf', '/home/vlad/mandala.mp3']


def loud(loudness):
    m = alsaaudio.Mixer()
    if loudness < 0:
        m.setvolume(0)
    elif loudness > 100:
        m.setvolume(100)
    else:
        m.setvolume(loudness)
    return m.getvolume()[0]


def main():

    loudness = 50
    parser = parse_args(sys.argv[1:])

    args = parser.parse_args()
    delay = args.parser(' '.join(args.timespec_list))

    args, leftovers = parser.parse_known_args()

    if args.track is not None:
        print("Setting alarm melody as '%s'" % args.track)
        ALARM_CMD[2] = args.track

    if args.volume is not None:
        print("setting volume to %s" % args.volume)
        loudness = int(args.volume)

    if delay > SAFETY_LIMIT:
        raise Exception("The delay is too big: %s" % time_delta(delay))

    print("Sleeping for %s" % time_delta(delay))
    time.sleep(delay.total_seconds())

    loud(loudness)

    subprocess.call(ALARM_CMD)


def time_delta(delta):

    result = []
    days = delta.days // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60

    if days > 0:
        result.append('%s days' % days)

    if minutes > 0:
        result.append('%s minutes' % minutes)
    if seconds > 0:
        result.append('%s seconds' % seconds)
    return ', '.join(result)


def parse_in(timespec):
    return timedelta(seconds=deltaparse(timespec))


def parse_args(args):

    parser = ArgumentParser(description=__doc__)

    parser.add_argument('--version', action='version',
                        version="%%(prog)s v%s" % __version__)

    parser.add_argument('-t', '--track',
                        help='give full path to melody in your filesystem')
    parser.add_argument('-v', '--volume', help='it will set loundess')

    subparsers = parser.add_subparsers(description='time to wake up')

    parser_in = subparsers.add_parser('in',
                                      help='wake up after some time left.\
                                            For example: in 5 minutes')
    parser_in.set_defaults(parser=parse_in)
    parser_in.add_argument('timespec_list', nargs=REMAINDER)

    parser_at = subparsers.add_parser('at',
                                      help='wake up at specific time.\
                                            For example: at 5 AM')
    parser_at.set_defaults(parser=parse_at)
    parser_at.add_argument('timespec_list', nargs=REMAINDER)

    return parser


def parse_at(timespec):

    now = datetime.now()
    date = dateparse(timespec)

    if date < now:
        date += relativedelta(days=+1)

    if date < now:
        raise Exception("oversleep")

    return date - datetime.now()


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


class TestAt(unittest.TestCase):

    def test_null(self):
        parser = parse_args([])
        self.assertTrue(parser is not None)


class TestSettings(unittest.TestCase):

    def test_filename_empty(self):
        self.assertNotEqual(ALARM_CMD[2], '')
        self.assertNotEqual(ALARM_CMD[2].strip(), '')
        self.assertNotEqual(ALARM_CMD[2].lstrip(), '')
        self.assertNotEqual(ALARM_CMD[2].rstrip(), '')

    def test_filenull(self):
        self.assertTrue(ALARM_CMD[2] is not None)

    def test_fileexists(self):
        self.assertTrue(os.path.exists(ALARM_CMD[2]) is True)

    def test_volume_settings_same(self):
        val = loud(50)
        self.assertIn(int(val), range(49, 52))

    def test_volume1(self):
        val = loud(0)
        self.assertEqual(int(val), 0)

    def test_volume2(self):
        val = loud(-1)
        self.assertGreaterEqual(int(val), 0)

    def test_volume3(self):
        val = loud(-1000)
        self.assertGreaterEqual(int(val), 0)

    def test_volume4(self):
        val = loud(-9999)
        self.assertGreaterEqual(int(val), 0)

    def test_volume5(self):
        val = loud(100)
        self.assertAlmostEquals(int(val), 100)

    def test_volume6(self):
        val = loud(100)
        self.assertLessEqual(int(val), 100)


if __name__ == '__main__':

    # unittest.main()
    main()
