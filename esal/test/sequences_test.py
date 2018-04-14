# Tests event sequences
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools
import random
import unittest

from . import data
from .. import events
from .. import sequences


class SequenceTests(unittest.TestCase):

    def test_order_concurrent_events(self):
        # Use reverse as the ordering transformation.  Write own to
        # handle iterables.
        def reverse(iterable):
            return reversed(list(iterable))

        # Use sequence 2 because it has the most events
        expected = list(data.seq_concurrent_events[i] for i in (
                2, 1, 0, # Time 0
                6, 5, 4, 3, # Time 1
                8, 7, # Time 2
                13, 12, 11, 10, 9, # Time 3
                ))
        actual = list(sequences.order_concurrent_events(
                data.seq_concurrent_events, ordering=reverse))
        self.assertEqual(expected, actual)

    def test_timeline_to_sequence(self):
        expected = list(data.seq_rand2_15)
        for idx, ev in enumerate(expected):
            expected[idx] = events.Event(
                ev.seq, idx, ev.end, ev.typ, ev.val)
        actual = list(sequences.timeline_to_sequence(
                data.seq_rand2_15))
        self.assertEqual(expected, actual)


class EventSequenceTest(unittest.TestCase):

    # Collection of test events in sorted order.  Must include duplicate
    # events.
    event_tuples = (
        # id, time, duration, event, value
        (319, 0, None, 'f', 'hi'),
        (319, 1, None, 'a', None),
        (319, 1, 1, 'd', 0),
        (319, 3, 4.3, 'a', None),
        (319, 4, None, 'a', -7),
        (319, 4, None, 'c', None), # 5
        (319, 4, None, 'c', None),
        (319, 4, 7.0, 'e', 'ok'),
        (319, 4, 7.0, 'f', 'lo'),
        (319, 5, 4, 'f', None),
        (319, 6, None, 'd', None), # 10
        (319, 6, None, 'd', True),
        (319, 6, 0, 'e', None),
        (319, 6, 8, 'c', -8.5),
        (319, 7, 3, 'a', True),
        (319, 9, 0.3, 'c', 6), # 15
        (319, 9, 1.0, 'b', -9.3),
        (319, 9, 3, 'b', -1.2),
        )

    events = tuple(itools.starmap(events.Event, event_tuples))

    def setUp(self):
        self.evseq = sequences.EventSequence(self.events)

    def test_init_sort_events(self):
        # Shuffle events before construction
        events_shuffled = list(self.events)
        random.shuffle(events_shuffled)
        es = sequences.EventSequence(events_shuffled)
        self.assertSequenceEqual(self.events, es.events)

    def test_len(self):
        self.assertEqual(len(self.event_tuples), len(self.evseq))

    def test_sequence(self):
        """Indirectly tests __getitem__"""
        self.assertSequenceEqual(self.events, self.evseq)

    def test_times(self):
        expected = (
            0, 1, 1, 3, 4, 4, 4, 4, 4, 5,
            6, 6, 6, 6, 7, 9, 9, 9,
            )
        actual = tuple(self.evseq.times())
        self.assertEqual(expected, actual)

    def test_types(self):
        expected = (
            'f', 'a', 'd', 'a', 'a', 'c', 'c', 'e', 'f', 'f',
            'd', 'd', 'e', 'c', 'a', 'c', 'b', 'b',
            )
        actual = tuple(self.evseq.types())
        self.assertSequenceEqual(expected, actual)

    def test_contains_event(self):
        self.assertIn(self.events[9], self.evseq)
        self.assertNotIn(events.Event(), self.evseq)

    def test_contains_field_value(self):
        self.assertIn(('val', None), self.evseq)
        self.assertIn(('val', True), self.evseq)
        self.assertIn(('typ', 'e'), self.evseq)
        self.assertIn(('end', 8.0), self.evseq)
        self.assertIn(('time', 7), self.evseq)
        self.assertNotIn(('time', 8), self.evseq)
        self.assertNotIn(('seq', 320), self.evseq)

    def test_match(self):
        self.assertEqual(16, self.evseq.match(typ='b'))
        self.assertEqual(8, self.evseq.match(val='lo', typ='f'))
        self.assertEqual(13, self.evseq.match(typ='c', end=8, time=6))
        self.assertIsNone(self.evseq.match(typ='f', val='ok'))
        self.assertIsNone(self.evseq.match(time=8))

    def test_match_bounds(self):
        self.assertEqual(14, self.evseq.match(typ='a', start=5))
        self.assertEqual(
            13, self.evseq.match(typ='c', start=10, stop=15))
        self.assertIsNone(self.evseq.match(typ='f', start=10))
        self.assertIsNone(self.evseq.match(typ='b', stop=16))
        self.assertIsNone(self.evseq.match(typ='c', start=7, stop=13))
        self.assertIsNone(self.evseq.match(start=3, stop=3))

    def test_matches(self):
        expected = (1, 5, 6, 10)
        actual = tuple(self.evseq.matches(end=None, val=None))
        self.assertEqual(expected, actual)
        expected = ()
        actual = tuple(self.evseq.matches(time=8))
        self.assertEqual(expected, actual)
