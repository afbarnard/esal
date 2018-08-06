# Tests `sorted_search.py`

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.


import math
import random
import unittest

from ..sorted_search import Target, binary_search, _binary_search


class BinarySearchTest(unittest.TestCase):

    #       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
    odds = [1, 1, 1, 3, 3, 3, 5, 5, 5, 7, 7, 7, 9, 9, 9]
    evns = [2, 2, 2, 4, 4, 4, 6, 6, 6, 8, 8, 8]

    #        0   1   2   3   4   5   6   7   8   9
    uniq = [ 0,  5,  7, 11, 13, 21, 25, 30, 31, 36,
            40, 45, 46, 50, 71, 77, 82, 83, 84, 93]

    def test_empty(self):
        self.assertEqual(
            (False, 0), binary_search([], 1, target=Target.any))
        self.assertEqual(
            (False, 0), binary_search([], 1, target=Target.lo))
        self.assertEqual(
            (False, 0), binary_search([], 1, target=Target.hi))
        self.assertEqual(
            (False, (0, 0)), binary_search([], 1, target=Target.range))

    def test_not_find(self):
        for nums, xs in ((BinarySearchTest.odds, range(0, 11, 2)),
                        (BinarySearchTest.evns, range(1, 11, 2))):
            for x in xs:
                idx = 3 * (x - (x % 2)) // 2
                for target in Target:
                    expected = ((False, idx)
                                if target != Target.range
                                else (False, (idx, idx)))
                    actual = binary_search(nums, x, target=target)
                    self.assertEqual(expected, actual)

    def test_find_any(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 11, 2)),
                         (BinarySearchTest.evns, range(2, 10, 2))):
            for x in xs:
                lo = 3 * (x - 2 + (x % 2)) // 2
                hi = lo + 3
                actual = binary_search(nums, x, target=Target.any)
                self.assertTrue(actual[0], (nums, x))
                self.assertLessEqual(lo, actual[1], (nums, x))
                self.assertGreater(hi, actual[1], (nums, x))

    def test_find_lo(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 11, 2)),
                         (BinarySearchTest.evns, range(2, 10, 2))):
            for x in xs:
                idx = 3 * (x - 2 + (x % 2)) // 2
                expected = (True, idx)
                actual = binary_search(nums, x, target=Target.lo)
                self.assertEqual(expected, actual, (nums, x))

    def test_find_hi(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 11, 2)),
                         (BinarySearchTest.evns, range(2, 10, 2))):
            for x in xs:
                idx = 3 * (x - 2 + (x % 2)) // 2
                expected = (True, idx + 3)
                actual = binary_search(nums, x, target=Target.hi)
                self.assertEqual(expected, actual, (nums, x))

    def test_not_find_range(self):
        nums = BinarySearchTest.uniq
        # Below
        self.assertEqual((False, (0, 0)), binary_search(
            nums, -100, target_key_hi=-10, target=Target.range))
        # Between neighboring numbers
        for hi_idx in range(1, len(nums)):
            lo_idx = hi_idx - 1
            x_lo = nums[lo_idx] + 1
            x_hi = nums[hi_idx] - 1
            expected = (False, (hi_idx, hi_idx))
            actual = binary_search(nums, x_lo, target_key_hi=x_hi,
                                   target=Target.range)
            self.assertEqual(expected, actual, (nums, (x_lo, x_hi)))
        # Above
        self.assertEqual((False, (len(nums),) * 2), binary_search(
            nums, 100, target_key_hi=110, target=Target.range))

    def test_find_range(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 11, 2)),
                         (BinarySearchTest.evns, range(2, 10, 2))):
            for x in xs:
                idx = 3 * (x - 2 + (x % 2)) // 2
                expected = (True, (idx, idx + 3))
                actual = binary_search(nums, x, target=Target.range)
                self.assertEqual(expected, actual, (nums, x))

    def test_find_range_loeq_hieq(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 9, 2)),
                         (BinarySearchTest.evns, range(2, 8, 2))):
            for x in xs:
                idx = 3 * (x - 2 + (x % 2)) // 2
                expected = (True, (idx, idx + 6))
                x_hi = x + 2
                actual = binary_search(nums, x, target_key_hi=x_hi,
                                       target=Target.range)
                self.assertEqual(expected, actual, (nums, (x, x_hi)))

    def test_find_range_loeq_hine(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 9, 2)),
                         (BinarySearchTest.evns, range(2, 8, 2))):
            for x in xs:
                idx = 3 * (x - 2 + (x % 2)) // 2
                expected = (True, (idx, idx + 6))
                x_hi = x + 3
                actual = binary_search(nums, x, target_key_hi=x_hi,
                                       target=Target.range)
                self.assertEqual(expected, actual, (nums, (x, x_hi)))

    def test_find_range_lone_hieq(self):
        for nums, xs in ((BinarySearchTest.odds, range(0, 8, 2)),
                         (BinarySearchTest.evns, range(1, 7, 2))):
            for x in xs:
                idx = 3 * (x - (x % 2)) // 2
                expected = (True, (idx, idx + 6))
                x_hi = x + 3
                actual = binary_search(nums, x, target_key_hi=x_hi,
                                       target=Target.range)
                self.assertEqual(expected, actual, (nums, (x, x_hi)))

    def test_find_range_lone_hine(self):
        for nums, xs in ((BinarySearchTest.odds, range(-2, 10, 2)),
                         (BinarySearchTest.evns, range(-1,  9, 2))):
            for x in xs:
                idx = 3 * (x - (x % 2)) // 2
                expected = (True, (max(idx, 0),
                                   min(idx + 6, len(nums))))
                x_hi = x + 4
                actual = binary_search(nums, x, target_key_hi=x_hi,
                                       target=Target.range)
                self.assertEqual(expected, actual, (nums, (x, x_hi)))

    def test_not_find_bounds(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 11, 2)),
                         (BinarySearchTest.evns, range(2, 10, 2))):
            for x in xs:
                idx = 3 * (x - 2 + (x % 2)) // 2
                for target in Target:
                    expected = ((False, idx)
                                if target != Target.range
                                else (False, (idx, idx)))
                    actual = binary_search(
                        nums, x, hi=idx, target=target)
                    self.assertEqual(expected, actual, (nums, x))
                    expected = ((False, idx + 3)
                                if target != Target.range
                                else (False, (idx + 3,) * 2))
                    actual = binary_search(
                        nums, x, lo=idx + 3, target=target)
                    self.assertEqual(expected, actual, (nums, x))

    def test_find_bounds(self):
        for nums, xs in ((BinarySearchTest.odds, range(1, 11, 2)),
                         (BinarySearchTest.evns, range(2, 10, 2))):
            for x in xs:
                idx = 3 * (x - 2 + (x % 2)) // 2
                lo = random.randrange(idx + 1)
                hi = random.randrange(idx + 3, len(nums) + 1)
                expected = (True, idx)
                actual = binary_search(
                    nums, x, lo=lo, hi=hi, target=Target.lo)
                self.assertEqual(expected, actual, (nums, x))
                expected = (True, idx + 3)
                actual = binary_search(
                    nums, x, lo=lo, hi=hi, target=Target.hi)
                self.assertEqual(expected, actual, (nums, x))
                expected = (True, (idx, idx + 3))
                actual = binary_search(
                    nums, x, lo=lo, hi=hi, target=Target.range)
                self.assertEqual(expected, actual, (nums, x))
                actual = binary_search(
                    nums, x, lo=lo, hi=hi, target=Target.any)
                self.assertTrue(actual[0], (nums, x))
                self.assertLessEqual(idx, actual[1], (nums, x))
                self.assertGreater(idx + 3, actual[1], (nums, x))

    def test_empty_bounds(self):
        nums = BinarySearchTest.odds
        expected = (False, 7)
        actual = binary_search(nums, 5, lo=7, hi=7, target=Target.any)
        self.assertEqual(expected, actual, (nums, 5))

    def test_bounds_out_of_bounds(self):
        nums = BinarySearchTest.odds
        expected = (True, 6)
        actual = binary_search(
            nums, 5, lo=-1, hi=(3 * len(nums)), target=Target.lo)
        self.assertEqual(expected, actual, (nums, 5))

    def test_unsorted(self):
        nums = [random.randrange(10) for _ in range(20)]
        for x in (-1, 10):
            actual = binary_search(nums, x)
            self.assertFalse(actual[0], (nums, x))

    def test_key_func_item(self):
        nums = BinarySearchTest.uniq
        for x in (8, 9):
            expected = (x == 9, 3)
            actual = binary_search(nums, x, key=lambda i, x: x - 2)
            self.assertEqual(expected, actual, (nums, x))

    def test_key_func_index(self):
        keys = BinarySearchTest.uniq
        nums = [random.randrange(10) for _ in range(len(keys))]
        for x in (76, 77):
            expected = (x == 77, 15)
            actual = binary_search(nums, x, key=lambda i, x: keys[i])
            self.assertEqual(expected, actual, (nums, x))

    def test_floats(self):
        nums = [
            0.006084507472282841, 0.035440080884487800,
            0.167276786230118320, 0.210249204406030120,
            0.491932710890211500, 0.626274208056601500,
            0.990542440162194500,
        ]
        for idx, n in enumerate(nums):
            for x in (n - 1e-3, n, n + 1e-3):
                expected = (x == n, idx + int(x > n))
                actual = binary_search(nums, x)
                self.assertEqual(expected, actual, (nums, x))
        for idx in range(len(nums) - 2):
            n1 = nums[idx]
            n2 = nums[idx + 2]
            expected = (True, (idx, idx + 3))
            actual = binary_search(
                nums, n1 - 1e-3, target_key_hi=n2 + 1e-3,
                target=Target.range)
            self.assertEqual(expected, actual, (nums, (n1, n2)))

    def test_right_insertion_bounds(self):
        nums = list(range(15))
        # Decreasing hi_gt
        expected = (True, 0, 0, 1)
        actual = _binary_search(nums, 0, 0, target=Target.lo)
        self.assertEqual(expected, actual, (nums, (0, 0)))
        # Increasing hi_le
        expected = (True, 14, 14, 15)
        actual = _binary_search(nums, 14, 14, target=Target.lo)
        self.assertEqual(expected, actual, (nums, (14, 14)))
        # Decreasing hi_le (only first one assigned)
        expected = (True, 0, 7, 15)
        actual = _binary_search(nums, 0, 15, target=Target.lo)
        self.assertEqual(expected, actual, (nums, (0, 15)))
        # All together now
        expected = (True, 4, 4, 5)
        actual = _binary_search(nums, 4, 4, target=Target.lo)
        self.assertEqual(expected, actual, (nums, (4, 4)))
