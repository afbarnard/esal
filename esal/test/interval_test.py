# Tests `interval.py`.

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import datetime
import unittest

from ..interval import AllenRelation, Interval, CompoundInterval


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


class IntervalTest(unittest.TestCase):

    def test_construct_bad_lo_hi(self):
        for lo, hi in (
                (2, 1),
                ('2018-11-01', '2018-10-31'),
                (datetime.date(2018, 11, 1),
                 datetime.date(2018, 10, 31)),
        ):
            with self.assertRaises(ValueError):
                Interval(lo, hi)
        # Negative length should also result in the same error
        with self.assertRaises(ValueError):
            Interval(2, length=-1)

    def test_construct_compute_length(self):
        # Type that supports subtraction
        i = Interval(3, 8)
        self.assertEqual(3, i.lo)
        self.assertEqual(8, i.hi)
        self.assertEqual(5, i.length())
        # Type that does not support subtraction
        i = Interval('2018-10-31', '2018-11-01')
        self.assertEqual('2018-10-31', i.lo)
        self.assertEqual('2018-11-01', i.hi)
        self.assertEqual(None, i.length())

    def test_construct_from_lo_length(self):
        i = Interval(3, length=5)
        self.assertEqual(3, i.lo)
        self.assertEqual(8, i.hi)
        self.assertEqual(5, i.length())
        i = Interval(datetime.date(2018, 10, 31),
                     length=datetime.timedelta(1))
        self.assertEqual(datetime.date(2018, 10, 31), i.lo)
        self.assertEqual(datetime.date(2018, 11, 1), i.hi)
        self.assertEqual(datetime.timedelta(1), i.length())
        # Non-integer zero length.  The type of the zero must be
        # preserved.
        i = Interval(datetime.date(2018, 10, 31),
                     length=datetime.timedelta(0))
        self.assertEqual(datetime.date(2018, 10, 31), i.lo)
        self.assertEqual(datetime.date(2018, 10, 31), i.hi)
        self.assertEqual(datetime.timedelta(0), i.length())

    def test_construct_point(self):
        # Types that support subtraction
        i = Interval(3)
        self.assertEqual(3, i.lo)
        self.assertEqual(3, i.hi)
        self.assertEqual(0, i.length())
        i = Interval(datetime.date(2018, 10, 31))
        self.assertEqual(datetime.date(2018, 10, 31), i.lo)
        self.assertEqual(datetime.date(2018, 10, 31), i.hi)
        self.assertEqual(datetime.timedelta(0), i.length())
        # Type that does not support subtraction
        i = Interval('2018-10-31')
        self.assertEqual('2018-10-31', i.lo)
        self.assertEqual('2018-10-31', i.hi)
        self.assertEqual(0, i.length())

    def test_is_point(self):
        i = Interval(3)
        self.assertTrue(i.is_point(), i)
        i = Interval(3, lo_open=True)
        self.assertFalse(i.is_point(), i)
        i = Interval(3, hi_open=True)
        self.assertFalse(i.is_point(), i)

    def test_is_empty(self):
        i = Interval(3)
        self.assertFalse(i.is_empty(), i)
        i = Interval(3, lo_open=True)
        self.assertTrue(i.is_empty(), i)
        i = Interval(3, hi_open=True)
        self.assertTrue(i.is_empty(), i)

    _orderings = (
        # Empty (empty is always less than non-empty)
        (Interval(52, lo_open=True), Interval(5, 21), 'lt'),
        (Interval(50, lo_open=True), Interval(50, lo_open=True), 'eq'),
        (Interval(2, lo_open=True), Interval(46, lo_open=True), 'eq'),
        (Interval(7, 26), Interval(27, lo_open=True), 'gt'),
        # Before
        (Interval(8, 54), Interval(61, 98), 'lt'),
        # Abut before
        (Interval(46, 50), Interval(50, 57), 'lt'),
        # Overlap before
        (Interval(39, 60), Interval(57, 71), 'lt'),
        # Outside end
        (Interval(5, 54, True, True), Interval(47, 54, True, True), 'lt'),
        (Interval(7, 85, True, True), Interval(83, 85, True, False), 'lt'),
        (Interval(21, 99, True, False), Interval(46, 99, True, True), 'lt'),
        (Interval(1, 25, True, False), Interval(20, 25, True, False), 'lt'),
        # Outside
        (Interval(3, 70), Interval(36, 67), 'lt'),
        # Inside begin
        (Interval(29, 73, False, True), Interval(29, 96, False, True), 'lt'),
        (Interval(2, 25, False, True), Interval(2, 43, True, True), 'lt'),
        (Interval(52, 62, True, True), Interval(52, 92, False, True), 'gt'),
        (Interval(2, 7, True, True), Interval(2, 47, True, True), 'lt'),
        # Equal
        (Interval(30, 36, False, True), Interval(30, 36, False, True), 'eq'),
        (Interval(1, 9, False, True), Interval(1, 9, False, False), 'lt'),
        (Interval(37, 39, False, True), Interval(37, 39, True, True), 'lt'),
        (Interval(11, 42, False, True), Interval(11, 42, True, False), 'lt'),
        (Interval(9, 73, False, False), Interval(9, 73, False, True), 'gt'),
        (Interval(35, 49, False, False), Interval(35, 49, False, False), 'eq'),
        (Interval(18, 82, False, False), Interval(18, 82, True, True), 'lt'),
        (Interval(16, 40, False, False), Interval(16, 40, True, False), 'lt'),
        (Interval(66, 94, True, True), Interval(66, 94, False, True), 'gt'),
        (Interval(34, 43, True, True), Interval(34, 43, False, False), 'gt'),
        (Interval(54, 75, True, True), Interval(54, 75, True, True), 'eq'),
        (Interval(35, 48, True, True), Interval(35, 48, True, False), 'lt'),
        (Interval(44, 63, True, False), Interval(44, 63, False, True), 'gt'),
        (Interval(9, 13, True, False), Interval(9, 13, False, False), 'gt'),
        (Interval(3, 50, True, False), Interval(3, 50, True, True), 'gt'),
        (Interval(22, 33, True, False), Interval(22, 33, True, False), 'eq'),
        # Outside begin
        (Interval(60, 90, False, True), Interval(60, 87, False, True), 'gt'),
        (Interval(17, 45, False, True), Interval(17, 38, True, True), 'lt'),
        (Interval(62, 76, True, True), Interval(62, 70, False, True), 'gt'),
        (Interval(16, 54, True, True), Interval(16, 34, True, True), 'gt'),
        # Inside
        (Interval(57, 58), Interval(0, 95), 'gt'),
        # Inside end
        (Interval(44, 49, True, True), Interval(25, 49, True, True), 'gt'),
        (Interval(25, 73, True, True), Interval(7, 73, True, False), 'gt'),
        (Interval(81, 94, True, False), Interval(12, 94, True, True), 'gt'),
        (Interval(82, 96, True, False), Interval(41, 96, True, False), 'gt'),
        # Overlap after
        (Interval(29, 96), Interval(28, 42), 'gt'),
        # Abut after
        (Interval(42, 72), Interval(41, 42), 'gt'),
        # After
        (Interval(97, 99), Interval(86, 87), 'gt'),
    )

    def test___eq__(self):
        for i1, i2, cmp_exp in IntervalTest._orderings:
            cmp_act = i1 == i2
            self.assertEqual(cmp_exp == 'eq', cmp_act, (i1, i2))
        # Check with different type
        self.assertNotEqual(Interval(1, 2), 3)

    def test___lt__(self):
        for i1, i2, cmp_exp in IntervalTest._orderings:
            cmp_act = i1 < i2
            self.assertEqual(cmp_exp == 'lt', cmp_act, (i1, i2))

    def test___le__(self):
        for i1, i2, cmp_exp in IntervalTest._orderings:
            cmp_act = i1 <= i2
            self.assertEqual(cmp_exp in ('lt', 'eq'), cmp_act, (i1, i2))

    def test___gt__(self):
        for i1, i2, cmp_exp in IntervalTest._orderings:
            cmp_act = i1 > i2
            self.assertEqual(cmp_exp == 'gt', cmp_act, (i1, i2))

    def test___ge__(self):
        for i1, i2, cmp_exp in IntervalTest._orderings:
            cmp_act = i1 >= i2
            self.assertEqual(cmp_exp in ('gt', 'eq'), cmp_act, (i1, i2))

    _subsets = (
        # Empty
        (Interval(0, lo_open=True), Interval(1, lo_open=True), True),
        (Interval(0, lo_open=True), Interval(1), True),
        (Interval(0, lo_open=True), Interval(1, 3), True),
        # Before / After
        (Interval(24, 69), Interval(83, 86), False),
        (Interval(50, 65), Interval(41, 43), False),
        # Abut
        (Interval(0, 82), Interval(82, 83), False),
        (Interval(36, 81), Interval(20, 36), False),
        # Overlap
        (Interval(3, 28), Interval(4, 99), False),
        (Interval(87, 98), Interval(42, 95), False),
        # Inside / Outside
        (Interval(55, 93), Interval(16, 94, True, True), True),
        (Interval(2, 68), Interval(7, 50, True, True), False),
        # Start
        (Interval(7, 11, True, False), Interval(7, 18, True, True),
         True),
        (Interval(80, 93, True, False), Interval(80, 97, False, True),
         True),
        (Interval(36, 90, False, False), Interval(36, 96, True, True),
         False),
        (Interval(32, 82, False, False), Interval(32, 99, False, True),
         True),
        # Finish
        (Interval(64, 89, False, True), Interval(23, 89, True, True),
         True),
        (Interval(54, 90, False, True), Interval(42, 90, True, False),
         True),
        (Interval(40, 73, False, False), Interval(27, 73, True, True),
         False),
        (Interval(77, 89, False, False), Interval(25, 89, True, False),
         True),
        # Equal
        (Interval(22, 39, True, True), Interval(22, 39, True, True),
         True),
        (Interval(43, 74, True, False), Interval(43, 74, True, True),
         False),
        (Interval(43, 92, False, True), Interval(43, 92, True, True),
         False),
        (Interval(21, 57, False, False), Interval(21, 57, True, True),
         False),
        (Interval(88, 93, True, False), Interval(88, 93, True, False),
         True),
        (Interval(27, 81, False, True), Interval(27, 81, False, True),
         True),
        (Interval(22, 85), Interval(22, 85), True),
    )

    def test_issubset(self):
        for i1, i2, is_subset_of in IntervalTest._subsets:
            if is_subset_of:
                self.assertTrue(i1.issubset(i2), (i1, i2))
            else:
                self.assertFalse(i1.issubset(i2), (i1, i2))

    _unions = (
        # Empty
        ((Interval(3, lo_open=True), Interval(21, lo_open=True)),
         Interval(3, lo_open=True)),
        ((Interval(37, lo_open=True), Interval(53, 96)),
         Interval(53, 96)),
        # Before / After
        ((Interval(11, 13), Interval(26, 62)),
         (Interval(11, 13), Interval(26, 62))),
        # Abut
        ((Interval(44, 45, True, True), Interval(45, 96, True, True)),
         (Interval(44, 45, True, True), Interval(45, 96, True, True))),
        ((Interval(53, 88, True, False), Interval(88, 98, True, True)),
         Interval(53, 98, True, True)),
        ((Interval(30, 60, True, True), Interval(60, 89, False, True)),
         Interval(30, 89, True, True)),
        ((Interval(42, 64), Interval(64, 77)), Interval(42, 77)),
        # Overlap
        ((Interval(20, 58, True, True), Interval(34, 86, True, True)),
         Interval(20, 86, True, True)),
        ((Interval(0, 65, True, True), Interval(47, 98, True, False)),
         Interval(0, 98, True, False)),
        ((Interval(66, 77, False, True), Interval(75, 95, True, True)),
         Interval(66, 95, False, True)),
        ((Interval(14, 67, False, True), Interval(23, 75, True, False)),
         Interval(14, 75)),
        # Inside / Outside
        ((Interval(82, 83, True, True), Interval(68, 96, True, True)),
         Interval(68, 96, True, True)),
        ((Interval(42, 59, True, True), Interval(10, 72, True, False)),
         Interval(10, 72, True, False)),
        ((Interval(17, 26, True, True), Interval(15, 64, False, True)),
         Interval(15, 64, False, True)),
        ((Interval(55, 59, True, True), Interval(3, 99)),
         Interval(3, 99)),
        # Start
        ((Interval(7, 78, True, True), Interval(7, 31, True, True)),
         Interval(7, 78, True, True)),
        ((Interval(26, 97, False, True), Interval(26, 52, True, True)),
         Interval(26, 97, False, True)),
        ((Interval(26, 27, True, True), Interval(26, 68, False, True)),
         Interval(26, 68, False, True)),
        ((Interval(34, 37), Interval(34, 48)), Interval(34, 48)),
        # Finish
        ((Interval(25, 44, True, True), Interval(7, 44, True, True)),
         Interval(7, 44, True, True)),
        ((Interval(5, 77, True, True), Interval(29, 77, True, False)),
         Interval(5, 77, True, False)),
        ((Interval(7, 51, True, False), Interval(45, 51, True, True)),
         Interval(7, 51, True, False)),
        ((Interval(64, 91), Interval(81, 91)), Interval(64, 91)),
        # Equal
        ((Interval(47, 90, True, True), Interval(47, 90, True, True)),
         Interval(47, 90, True, True)),
        ((Interval(0, 61, True, False), Interval(0, 61, True, False)),
         Interval(0, 61, True, False)),
        ((Interval(52, 54, False, True), Interval(52, 54, False, True)),
         Interval(52, 54, False, True)),
        ((Interval(14, 20, False, False), Interval(14, 20, False, False)),
         Interval(14, 20, False, False)),
        # Multiple
        ((Interval(15, 30), Interval(17, 81), Interval(27, 83)),
         Interval(15, 83)),
        ((Interval(2, 7), Interval(13, 84), Interval(87, 94)),
         (Interval(2, 7), Interval(13, 84), Interval(87, 94))),
    )

    def test_union(self):
        for intervals, u_exp in IntervalTest._unions:
            for itvls in (intervals, tuple(reversed(intervals))):
                u_act = itvls[0].union(*itvls[1:])
                if isinstance(u_act, CompoundInterval):
                    u_act = tuple(u_act)
                self.assertEqual(u_exp, u_act)

    _intersections = (
        # Empty
        ((Interval(28, lo_open=True), Interval(35, 87, True, True)),
         Interval(0, lo_open=True)),
        ((Interval(39, lo_open=True), Interval(1, 61, True, True)),
         Interval(0, lo_open=True)),
        ((Interval(94, lo_open=True), Interval(4, 69, True, True)),
         Interval(0, lo_open=True)),
        # Before / After
        ((Interval(31, 62), Interval(74, 91)),
         Interval(0, lo_open=True)),
        # Abut
        ((Interval(1, 43, True, True), Interval(43, 76, True, True)),
         Interval(43, lo_open=True)),
        ((Interval(38, 97, True, False), Interval(97, 99, True, True)),
         Interval(97, lo_open=True)),
        ((Interval(13, 19, True, True), Interval(19, 85, False, True)),
         Interval(19, lo_open=True)),
        ((Interval(50, 53), Interval(53, 96)), Interval(53)),
        # Overlap
        ((Interval(2, 56, True, True), Interval(5, 80, True, True)),
         Interval(5, 56, True, True)),
        ((Interval(13, 63, True, False), Interval(22, 89, True, True)),
         Interval(22, 63, True, False)),
        ((Interval(6, 63, True, True), Interval(59, 93, False, True)),
         Interval(59, 63, False, True)),
        ((Interval(11, 58), Interval(24, 71)), Interval(24, 58)),
        # Inside / Outside
        ((Interval(13, 53, True, True), Interval(9, 98, True, True)),
         Interval(13, 53, True, True)),
        ((Interval(27, 31, True, False), Interval(7, 82, True, True)),
         Interval(27, 31, True, False)),
        ((Interval(72, 79, False, True), Interval(66, 86, True, True)),
         Interval(72, 79, False, True)),
        ((Interval(5, 14), Interval(4, 89)), Interval(5, 14)),
        # Start
        ((Interval(27, 35, True, True), Interval(27, 39, True, True)),
         Interval(27, 35, True, True)),
        ((Interval(0, 33, False, True), Interval(0, 98, True, True)),
         Interval(0, 33, True, True)),
        ((Interval(29, 39, False, True), Interval(29, 47, False, True)),
         Interval(29, 39, False, True)),
        ((Interval(2, 56), Interval(2, 80)), Interval(2, 56)),
        # Finish
        ((Interval(12, 61, True, True), Interval(43, 61, True, True)),
         Interval(43, 61, True, True)),
        ((Interval(49, 81, True, False), Interval(57, 81, True, True)),
         Interval(57, 81, True, True)),
        ((Interval(6, 99, True, False), Interval(97, 99, True, False)),
         Interval(97, 99, True, False)),
        ((Interval(11, 43), Interval(25, 43)), Interval(25, 43)),
        # Equal
        ((Interval(70, 87, True, True), Interval(70, 87, True, True)),
         Interval(70, 87, True, True)),
        ((Interval(37, 83, True, False), Interval(37, 83, True, False)),
         Interval(37, 83, True, False)),
        ((Interval(5, 61, False, True), Interval(5, 61, False, True)),
         Interval(5, 61, False, True)),
        ((Interval(6, 24), Interval(6, 24)), Interval(6, 24)),
        # Multiple
        ((Interval(0, 53), Interval(37, 67), Interval(50, 73)),
         Interval(50, 53)),
    )

    def test_intersection(self):
        for intervals, i_exp in IntervalTest._intersections:
            for itvls in (intervals, tuple(reversed(intervals))):
                i_act = itvls[0].intersection(*itvls[1:])
                self.assertEqual(i_exp, i_act)

    def test_intersects(self):
        for intervals, i_exp in IntervalTest._intersections:
            for itvls in (intervals, tuple(reversed(intervals))):
                self.assertEqual(not i_exp.is_empty(),
                                 itvls[0].intersects(itvls[1]))
