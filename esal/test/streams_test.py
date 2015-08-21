# Tests event stream operations
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools
import unittest

from . import data
from .. import engine
from .. import streams


class EventStreamOperationsTest(unittest.TestCase):

    def test_collect_event_sequences(self):
        expected = (
            data.simple_events[0:4],
            data.simple_events[4:5],
            data.simple_events[5:10],
            )
        actual = tuple(
            tuple(seq) for seq in
            streams.collect_event_sequences(data.simple_events))
        self.assertEqual(expected, actual)

    def test_map_sequences_as_events_to_values(self):
        """Tests mapping sequences to values."""
        expected = (7, 3, 14)
        actual = tuple(streams.map_sequences_as_events(
                engine.count, data.simple_concurrent_events))
        self.assertEqual(expected, actual)

    def test_map_sequences_as_events_to_sequences(self):
        """Tests mapping sequences to sequences."""
        def first3(iterable):
            for idx, item in enumerate(iterable):
                yield item
                if idx >= 2:
                    break
        expected = list(itools.chain(
                data.simple_concurrent_events[0:3],
                data.simple_concurrent_events[7:10],
                data.simple_concurrent_events[10:13]))
        actual = list(streams.map_sequences_as_events(
                first3, data.simple_concurrent_events))
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
