# Tests events
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from .. import events
from .. import general


class EventTest(unittest.TestCase):

    event_fields = ('pt12345', '2015-04-28', 31, 'mi', True)

    def setUp(self):
        self.event = events.Event(*self.event_fields)

    def test_getitem_by_index(self):
        for index, value in enumerate(self.event_fields):
            self.assertEqual(value, self.event[index])

    def test_getitem_by_name(self):
        for index, name in enumerate(self.event._fields):
            self.assertEqual(self.event_fields[index], self.event[name])

    def test_sort_key(self):
        key = general.iterable_sort_key(self.event_fields)
        self.assertEqual(key, self.event.sort_key())


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

    def test_value_of(self):
        for index, name in enumerate(self.names):
            self.assertEqual(name, self.header.value_of(self.names, name))
            self.assertEqual(name, self.header.value_of(self.names, index))
