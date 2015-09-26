# Tests general functions
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import datetime
import unittest

from .. import general


class FirstsTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual((), tuple(general.firsts(())))

    def test_unique(self):
        expected = tuple(range(10, 0, -1))
        actual = tuple(general.firsts(range(10, 0, -1)))
        self.assertEqual(expected, actual)

    def test_repeated(self):
        nums = (3, 3, 4, 0, 4, 4, 3, 2, 1, 4, 4, 1, 3, 3, 0)
        expected = (3, 4, 0, 2, 1)
        actual = tuple(general.firsts(nums))
        self.assertEqual(expected, actual)

    def test_keyfunc(self):
        pairs = (
            (5, 'a'), (6, 'a'), (0, 'a'), (0, 'a'), (5, 'b'),
            (4, 'a'), (0, 'a'), (1, 'c'), (9, 'b'), (0, 'b'),
            )
        expected = ((5, 'a'), (5, 'b'), (1, 'c'))
        actual = tuple(general.firsts(pairs, key=lambda p: p[1]))
        self.assertEqual(expected, actual)


class GetItemsTest(unittest.TestCase):

    items = (
        15, 14, 5, 9, 2,
        1, 9, 15, 5, 9,
        1, 9, 13, 10, 5,
        8, 16, 2, 16, 18,
        )
    indices1 = (0, 14, 1, 13, 8, 5, 5)
    items1 = (15, 5, 14, 10, 5, 1, 1)
    indices2 = (0, 4, 12, 17, 18, 19, 19)
    items2 = (15, 2, 13, 2, 16, 18, 18)

    def test_empty_items_indexable(self):
        expected = ()
        actual = tuple(general.getitems((), iter((1, 2, 3))))
        self.assertEqual(expected, actual)

    def test_empty_items_iterable(self):
        expected = ()
        actual = tuple(general.getitems(iter(()), iter((1, 2, 3))))
        self.assertEqual(expected, actual)

    def test_empty_indices_indexable(self):
        expected = ()
        actual = tuple(general.getitems(self.items, iter(())))
        self.assertEqual(expected, actual)

    def test_empty_indices_iterable(self):
        expected = ()
        actual = tuple(general.getitems(iter(self.items), iter(())))
        self.assertEqual(expected, actual)

    def test_indexable_items(self):
        expected = self.items1
        actual = tuple(general.getitems(
                self.items, iter(self.indices1)))
        self.assertEqual(expected, actual)

    def test_iterable_items_sorted_indices(self):
        expected = self.items2
        actual = tuple(general.getitems(
                iter(self.items), iter(self.indices2)))
        self.assertEqual(expected, actual)

    def test_iterable_items_unsorted_indices(self):
        expected = self.items1
        actual = tuple(general.getitems(
                iter(self.items), iter(self.indices1)))
        self.assertEqual(expected, actual)


class WindowsTest(unittest.TestCase):

    items = (8, 6, 3, 8, 9, 4, 7, 3, 8, 2, 7)

    def test_empty_items(self):
        expected = ()
        actual = tuple(general.windows(iter(()), 5))
        self.assertEqual(expected, actual)

    def test_empty_window(self):
        expected = ()
        actual = tuple(general.windows(iter(self.items), 0))
        self.assertEqual(expected, actual)

    def test_single_items(self):
        expected = ((8,), (6,), (3,), (8,), (9,), (4,))
        actual = tuple(general.windows(iter(self.items[:6]), 1))
        self.assertEqual(expected, actual)

    def test_window_equals_length(self):
        expected = (self.items,)
        actual = tuple(general.windows(
            iter(self.items), len(self.items)))
        self.assertEqual(expected, actual)

    def test_window_smaller_than_length(self):
        expected = (
            self.items[0:5],
            self.items[1:6],
            self.items[2:7],
            self.items[3:8],
            self.items[4:9],
            self.items[5:10],
            )
        actual = tuple(general.windows(iter(self.items[:10]), 5))
        self.assertEqual(expected, actual)

    def test_window_larger_than_length(self):
        expected = (self.items,)
        actual = tuple(general.windows(
            iter(self.items), len(self.items) + 1))
        self.assertEqual(expected, actual)


class FullyQualifiedTypeNameTest(unittest.TestCase):

    names_objects = (
        ('builtins.NoneType', None),
        ('builtins.bool', False),
        ('builtins.int', 0),
        ('builtins.float', 0.0),
        ('builtins.str', ''),
        ('builtins.tuple', ()),
        ('builtins.list', []),
        ('builtins.dict', {}),
        )

    def test_builtin_objects(self):
        for name, obj in self.names_objects:
            self.assertEqual(name, general.fq_typename(obj))

    def test_builtin_types(self):
        for name, obj in self.names_objects:
            self.assertEqual(name, general.fq_typename(type(obj)))

    def test_nested_modules(self):
        self.assertEqual(
            'esal.test.general_test.FullyQualifiedTypeNameTest',
            general.fq_typename(self))


class UniversalSortKeyTest(unittest.TestCase):

    objects = (False, 0, 0.0, '', (), [], {})

    def test_none(self):
        self.assertEqual((), general.universal_sort_key(None))

    def test_builtin_objects(self):
        for obj in self.objects:
            expected = (general.fq_typename(obj), obj)
            actual = general.universal_sort_key(obj)
            self.assertEqual(expected, actual)

    def test_builtin_objects_keyfunc(self):
        for obj in self.objects:
            expected = (general.fq_typename(obj), str(obj))
            actual = general.universal_sort_key(obj, key=str)
            self.assertEqual(expected, actual)


class IterableSortKeyTest(unittest.TestCase):

    # Include types None < int < float < str < datetime.date
    tuples = (
        (None, None),
        (None, 735865),
        (None, 735866),
        (None, 735865.0),
        (None, 735866.0),
        (None, '735865'),
        (None, '735866'),
        (None, datetime.date(2015, 9, 24)),
        (None, datetime.date(2015, 9, 25)),
        (461, None),
        (461, 735865),
        (461, 735866),
        (461, 735865.0),
        (461, 735866.0),
        (461, '735865'),
        (461, '735866'),
        (461, datetime.date(2015, 9, 24)),
        (461, datetime.date(2015, 9, 25)),
        (461.0, None),
        (461.0, 735865),
        (461.0, 735866),
        (461.0, 735865.0),
        (461.0, 735866.0),
        (461.0, '735865'),
        (461.0, '735866'),
        (461.0, datetime.date(2015, 9, 24)),
        (461.0, datetime.date(2015, 9, 25)),
        ('461', None),
        ('461', 735865),
        ('461', 735866),
        ('461', 735865.0),
        ('461', 735866.0),
        ('461', '735865'),
        ('461', '735866'),
        ('461', datetime.date(2015, 9, 24)),
        ('461', datetime.date(2015, 9, 25)),
        )

    def test_iterable_sort_key(self):
        srtd = sorted(reversed(self.tuples),
                      key=general.iterable_sort_key)
        self.assertSequenceEqual(self.tuples, srtd)
