# Tests event stream operations
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from .. import streams
from . import data


class EventStreamOperationsTest(unittest.TestCase):

    def test_collect_event_sequences(self):
        expected = (
            data.simple_events[0:4],
            data.simple_events[4:5],
            data.simple_events[5:10],
            )
        actual = tuple(streams.collect_event_sequences(data.simple_events))
        self.assertEqual(expected, actual)

    def test_select_events(self):
        """Tests select for a collection of values."""
        expected = (
            data.simple_events[0:2] +
            data.simple_events[4:5] +
            data.simple_events[6:8] +
            data.simple_events[9:10]
            )
        actual = tuple(streams.select(data.simple_events, 'ev', ('a', 'b')))
        self.assertEqual(expected, actual)

    def test_select_times(self):
        """Tests select for a range of values."""
        expected = (
            data.simple_events[0:2] +
            data.simple_events[5:8]
            )
        actual = tuple(streams.select(data.simple_events, 'time', range(3)))
        self.assertEqual(expected, actual)
