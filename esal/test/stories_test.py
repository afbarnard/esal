# Tests features from stories
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools
import unittest

from . import data
from .. import engine
from .. import events
from .. import sequences
from .. import streams


# Selection predicates

def _has_warfarin(event):
    return event.typ == 'd_warfarin'

def _is_unobserved(event):
    return event.val is None


class StoryTests(unittest.TestCase):

    def test_story001(self):
        # Count all events
        self.assertEqual(len(data.med_events),
                         engine.count(data.med_events))
        # Count selected warfarin events
        actual = engine.count(
            engine.select(data.med_events, _has_warfarin))
        self.assertEqual(2, actual)

    def test_story002(self):
        # Count distinct patients (sequence ID is field 0)
        actual = engine.count(
            engine.distinct(engine.project(data.med_events, (0,))))
        self.assertEqual(10, actual)
        # Count distinct event types (event type is field 3)
        actual = engine.count(
            engine.distinct(engine.project(data.med_events, (3,))))
        self.assertEqual(len(data.drugs) + len(data.conds), actual)

    def test_story003(self):
        # Count distinct patients that have had warfarin
        actual = engine.count(engine.distinct(engine.project(
                    engine.select(data.med_events, _has_warfarin),
                    (0,))))
        self.assertEqual(2, actual)
        # Count distinct types of unobserved events
        actual = engine.count(engine.distinct(engine.project(
                    engine.select(data.med_events, _is_unobserved),
                    (3,))))
        self.assertEqual(13, actual)

    def test_story004(self):
        # Order events in reverse by their name and then strip times to
        # convert to sequences.  Number events starting at 1.
        rev_evs_to_seqs = sequences.make_timeline_to_sequence_flattener(
            ordering=lambda evs: sorted(
                evs, key=lambda e: e.typ, reverse=True),
            start=1)
        seqs = (
            data.seq_concurrent_events,
            data.seq_sorted,
            data.seq_rand1_08,
            )
        index_maps = (
            (2, 1, 0, 6, 5, 4, 3, 8, 7, 13, 12, 11, 10, 9),
            (1, 2, 0, 3, 4, 6, 5, 9, 8, 7, 10),
            (1, 0, 4, 3, 2, 5, 6, 7),
            )
        expected = []
        for seq_idx, seq in enumerate(seqs):
            for ev_num, ev_idx in enumerate(index_maps[seq_idx], 1):
                ev = seq[ev_idx]
                expected.append(events.Event(
                        ev.seq, ev_num, ev.end, ev.typ, ev.val))
        actual = list(streams.map_sequences_as_events(
                rev_evs_to_seqs, itools.chain.from_iterable(seqs)))
        self.assertEqual(expected, actual)
