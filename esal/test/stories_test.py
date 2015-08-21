# Tests features from stories
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from . import data
from .. import engine
from .. import events
from .. import sequences
from .. import streams


# Selection predicates

def _has_warfarin(event):
    return event.ev == 'd_warfarin'

def _is_unobserved(event):
    return event.val is None


class StoryTests(unittest.TestCase):

    def test_story001(self):
        # Count all events
        self.assertEqual(len(data.med_events),
                         engine.count(data.med_events))
        # Count selected warfarin events
        self.assertEqual(2,
                         engine.count(engine.select(
                             data.med_events, _has_warfarin)))

    def test_story002(self):
        # Count distinct patients (sequence ID is field 0)
        self.assertEqual(10,
                         engine.count(engine.distinct(
                             engine.project(data.med_events, (0,)))))
        # Count distinct event types (event type is field 3)
        self.assertEqual(len(data.drugs) + len(data.conds),
                         engine.count(engine.distinct(
                             engine.project(data.med_events, (3,)))))

    def test_story003(self):
        # Count distinct patients that have had warfarin
        self.assertEqual(2,
                         engine.count(engine.distinct(engine.project(
                             engine.select(
                                 data.med_events, _has_warfarin),
                             (0,)))))
        # Count distinct types of unobserved events
        self.assertEqual(13,
                         engine.count(engine.distinct(engine.project(
                             engine.select(
                                 data.med_events, _is_unobserved),
                             (3,)))))

    def test_story004(self):
        # Order events in reverse by their name and then strip times to
        # convert to sequences
        def reverse_events_to_sequences(seq):
            return sequences.timelines_to_sequences(
                sequences.order_concurrent_events(
                    seq,
                    ordering=lambda evs: sorted(
                        evs, key=lambda e: e.ev, reverse=True)))
        ev_idxs = (
            (1, 0, 3, 2, 6, 5, 4), # Seq 0
            (9, 8, 7), # Seq 1
            (12, 11, 10, 15, 14, 13, 18, 17, 16, 20, 19, 23, 22, 21), # Seq 2
            )
        expected = []
        for seq in ev_idxs:
            for idx, ev_idx in enumerate(seq):
                ev = data.simple_concurrent_events[ev_idx]
                expected.append(events.Event(
                        ev.seq, idx, ev.dura, ev.ev, ev.val))
        actual = list(streams.map_sequences_as_events(
                reverse_events_to_sequences,
                data.simple_concurrent_events))
        self.assertEqual(expected, actual)
