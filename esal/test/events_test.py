# Tests events
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from .. import events


class EventTest(unittest.TestCase):

    event_fields = ('pt12345', '2015-04-28', 31, 'mi', True)

    def test_getitem_by_index(self):
        event = events.Event(*self.event_fields)
        for index, value in enumerate(self.event_fields):
            self.assertEqual(value, event[index])

    def test_getitem_by_name(self):
        event = events.Event(*self.event_fields)
        for index, name in enumerate(event._fields):
            self.assertEqual(self.event_fields[index], event[name])
