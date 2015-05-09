# Tests features from stories
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from .. import engine
from . import data


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
                         engine.count_distinct(
                             engine.project(data.med_events, (0,))))
        # Count distinct event types (event type is field 3)
        self.assertEqual(len(data.drugs) + len(data.conds),
                         engine.count_distinct(
                             engine.project(data.med_events, (3,))))

    def test_story003(self):
        # Count distinct patients that have had warfarin
        self.assertEqual(2,
                         engine.count_distinct(engine.project(
                             engine.select(
                                 data.med_events, _has_warfarin),
                             (0,))))
        # Count distinct types of unobserved events
        self.assertEqual(13,
                         engine.count_distinct(engine.project(
                             engine.select(
                                 data.med_events, _is_unobserved),
                             (3,))))
