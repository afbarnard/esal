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

    def test_collect_sequences(self):
        expected = (
            data.seq_abcdef,
            data.seq_concurrent_events,
            data.seq_unsorted,
            data.seq_sorted
            )
        actual = tuple(
            tuple(seq) for seq in
            streams.collect_sequences(
                itools.chain.from_iterable(expected)))
        self.assertEqual(expected, actual)

    def test_flatten(self):
        def range_generator(start, stop):
            for i in range(start, stop):
                yield i
        iterable = [
            range(5),
            ([(5,), 6], 7, [8, 9, 10], ((11,), (12,), [[[13]]])),
            [[(map(lambda x: x + 14, range(3)),), 17],
             iter((18, 19)),
             ((((20,),),),),
             [range_generator(21, 24), [range_generator(24, 30)]]],
            '30',
            ]
        expected = list(range(30))
        expected.append('30')
        actual = list(streams.flatten(iterable))
        self.assertEqual(expected, actual)

    def test_map_sequences_as_events_to_values(self):
        """Tests mapping sequences to values."""
        seqs = (
            data.seq_len1,
            data.seq_abcdef,
            data.seq_concurrent_events,
            data.seq_unsorted,
            data.seq_sorted,
            )
        expected = tuple(len(s) for s in seqs)
        actual = tuple(streams.map_sequences_as_events(
                engine.count, itools.chain.from_iterable(seqs)))
        self.assertEqual(expected, actual)

    def test_map_sequences_as_events_to_sequences(self):
        """Tests mapping sequences to sequences."""
        def first3(iterable):
            for idx, item in enumerate(iterable):
                yield item
                if idx >= 2:
                    break
        seqs = (
            data.seq_len1,
            data.seq_abcdef,
            data.seq_concurrent_events,
            data.seq_unsorted,
            data.seq_sorted,
            )
        expected = list(itools.chain.from_iterable(
                map(lambda s: itools.islice(s, 3), seqs)))
        actual = list(streams.map_sequences_as_events(
                first3, itools.chain.from_iterable(seqs)))
        self.assertEqual(expected, actual)

    def test_select_events(self):
        """Tests select for a collection of values."""
        expected = tuple(data.evs_for_selection[i] for i in
                         (0, 1, 2, 6, 7, 9, 10, 16))
        actual = tuple(streams.select(
                data.evs_for_selection, 'typ', ('a', 'b', 'c')))
        self.assertEqual(expected, actual)

    def test_select_times(self):
        """Tests select for a range of values."""
        expected = tuple(data.evs_for_selection[i] for i in
                         (0, 1, 2, 3, 5, 7, 9, 11, 12, 14, 15, 16, 18))
        actual = tuple(streams.select(
                data.evs_for_selection, 'time', range(4)))
        self.assertEqual(expected, actual)
