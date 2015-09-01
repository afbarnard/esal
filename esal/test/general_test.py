# Tests general functions
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

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
