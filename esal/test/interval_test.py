# Tests `interval.py`.

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from ..interval import AllenRelation, Interval


class AllenRelationTest(unittest.TestCase):

    def test_inverse(self):
        self.assertEqual(AllenRelation.before.inverse(),
                         AllenRelation.after)
        self.assertEqual(AllenRelation.abut_before.inverse(),
                         AllenRelation.abut_after)
        self.assertEqual(AllenRelation.overlap_before.inverse(),
                         AllenRelation.overlap_after)
        self.assertEqual(AllenRelation.outside_end.inverse(),
                         AllenRelation.inside_end)
        self.assertEqual(AllenRelation.outside.inverse(),
                         AllenRelation.inside)
        self.assertEqual(AllenRelation.inside_begin.inverse(),
                         AllenRelation.outside_begin)
        self.assertEqual(AllenRelation.equal.inverse(),
                         AllenRelation.equal)
        self.assertEqual(AllenRelation.outside_begin.inverse(),
                         AllenRelation.inside_begin)
        self.assertEqual(AllenRelation.inside.inverse(),
                         AllenRelation.outside)
        self.assertEqual(AllenRelation.inside_end.inverse(),
                         AllenRelation.outside_end)
        self.assertEqual(AllenRelation.overlap_after.inverse(),
                         AllenRelation.overlap_before)
        self.assertEqual(AllenRelation.abut_after.inverse(),
                         AllenRelation.abut_before)
        self.assertEqual(AllenRelation.after.inverse(),
                         AllenRelation.before)

    def test_is_inverse(self):
        self.assertTrue(AllenRelation.equal.is_inverse(
            AllenRelation.equal))
        self.assertTrue(AllenRelation.before.is_inverse(
            AllenRelation.after))
        self.assertFalse(AllenRelation.before.is_inverse(
            AllenRelation.inside_end))


class AllenAlgebraTest(unittest.TestCase):

    def test_before(self):
        itvl1 = Interval(32, 56)
        itvl2 = Interval(81, 97)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.before, rel)

    def test_abut_before(self):
        itvl1 = Interval(15, 64)
        itvl2 = Interval(64, 80)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.abut_before, rel)

    def test_abut_before_empty(self):
        itvl1 = Interval(32, 32)
        itvl2 = Interval(32, 79)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.abut_before, rel)

    def test_overlap_before(self):
        itvl1 = Interval(5, 57)
        itvl2 = Interval(20, 88)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.overlap_before, rel)

    def test_outside_end(self):
        itvl1 = Interval(2, 99)
        itvl2 = Interval(6, 99)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.outside_end, rel)

    def test_outside(self):
        itvl1 = Interval(1, 76)
        itvl2 = Interval(51, 72)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.outside, rel)

    def test_inside_begin(self):
        itvl1 = Interval(35, 59)
        itvl2 = Interval(35, 64)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.inside_begin, rel)

    def test_equal(self):
        itvl1 = Interval(11, 78)
        itvl2 = Interval(11, 78)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.equal, rel)

    def test_outside_begin(self):
        itvl1 = Interval(65, 84)
        itvl2 = Interval(65, 69)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.outside_begin, rel)

    def test_inside(self):
        itvl1 = Interval(43, 54)
        itvl2 = Interval(26, 95)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.inside, rel)

    def test_inside_end(self):
        itvl1 = Interval(67, 73)
        itvl2 = Interval(8, 73)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.inside_end, rel)

    def test_overlap_after(self):
        itvl1 = Interval(38, 90)
        itvl2 = Interval(1, 71)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.overlap_after, rel)

    def test_abut_after_empty(self):
        itvl1 = Interval(20, 20)
        itvl2 = Interval(1, 20)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.abut_after, rel)

    def test_abut_after(self):
        itvl1 = Interval(7, 32)
        itvl2 = Interval(5, 7)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.abut_after, rel)

    def test_after(self):
        itvl1 = Interval(90, 95)
        itvl2 = Interval(15, 33)
        rel = itvl1.allen_relation(itvl2)
        self.assertEqual(AllenRelation.after, rel)
