# Tests events
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from .. import events
from .. import general


class HeaderTest(unittest.TestCase):

    names = ('kew', 'peyo', 'sef', 'ster', 'nati', 'umb', 'roge')

    def setUp(self):
        self.header = events.Header(self.names)

    def test_len(self):
        self.assertEqual(len(self.names), len(self.header))

    def test_getitem(self):
        for index, name in enumerate(self.names):
            self.assertEqual(index, self.header[name])
            self.assertEqual(index, self.header[index])

    def test_name_of(self):
        for index, name in enumerate(self.names):
            self.assertEqual(name, self.header.name_of(index))

    def test_index_of(self):
        for index, name in enumerate(self.names):
            self.assertEqual(index, self.header.index_of(name))


class EventTest(unittest.TestCase):

    """Thoroughly tests Event according to the desired properties listed
    in story 007.
    """

    event_fields = ('pt12345', '2015-04-28', 31, 'mi', True)

    def setUp(self):
        self.event = events.Event(*self.event_fields)

    def test_construction_by_name_value_pairs(self):
        self.event = events.Event(time=3.3, ev='c', seq=111)
        self.assertEqual(111, self.event.seq)
        self.assertEqual(3.3, self.event.time)
        self.assertEqual('c', self.event.ev)
        self.assertIsNone(self.event.dura)
        self.assertIsNone(self.event.val)

    def test_access_field_by_index(self):
        for index, value in enumerate(self.event_fields):
            self.assertEqual(value, self.event[index])

    def test_access_field_by_name(self):
        for index, name in enumerate(self.event.header.names):
            self.assertEqual(self.event_fields[index], self.event[name])

    def test_access_field_by_attribute(self):
        for index, name in enumerate(self.event.header.names):
            self.assertEqual(
                self.event_fields[index], getattr(self.event, name))

    def test_read_only_attributes(self):
        for index, name in enumerate(self.event.header.names):
            with self.assertRaises(AttributeError):
                setattr(self.event, name, index)

    def test_read_only_items(self):
        for index, name in enumerate(self.event.header.names):
            with self.assertRaises(TypeError):
                self.event[index] = name

    def test_len(self):
        self.assertEqual(5, len(self.event))

    def test_iter(self):
        for idx, field in enumerate(self.event):
            self.assertEqual(self.event_fields[idx], field)

    def test_contains(self):
        for field in self.event_fields:
            self.assertIn(field, self.event)

    def test_eq(self):
        event2 = events.Event(*self.event_fields)
        self.assertEqual(self.event, event2)

    def test_hash(self):
        event2 = events.Event(*self.event_fields)
        self.assertEqual(hash(self.event), hash(event2))

    def test_repr(self):
        rep = "Event(seq='pt12345', time='2015-04-28', dura=31, ev='mi', val=True)"
        self.assertEqual(rep, repr(self.event))

    def test_sort_key(self):
        key = general.iterable_sort_key(self.event_fields)
        self.assertEqual(key, self.event.sort_key())
