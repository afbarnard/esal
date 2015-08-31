# Tests event sequences
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools
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
        expected = list(itools.chain(
                reversed(data.binary_events[10:13]),
                reversed(data.binary_events[13:16]),
                reversed(data.binary_events[16:19]),
                reversed(data.binary_events[19:21]),
                reversed(data.binary_events[21:24])))
        actual = list(sequences.order_concurrent_events(
                data.binary_events[10:], ordering=reverse))
        self.assertEqual(expected, actual)

    def test_timeline_to_sequence(self):
        expected = list(data.binary_events[10:])
        for idx, ev in enumerate(expected):
            expected[idx] = events.Event(
                ev.seq, idx, ev.dura, ev.ev, ev.val)
        actual = list(sequences.timeline_to_sequence(
                data.binary_events[10:]))
        self.assertEqual(expected, actual)
