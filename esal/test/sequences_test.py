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
