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
