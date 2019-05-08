# Tests `sorted_search.py`

# Copyright (c) 2018-2019 Aubrey Barnard.
#
# This is free software released under the MIT License.  See `LICENSE`
# for details.


import math
import random
import unittest

from ..sorted_search import (
    Target, binary_search, _binary_search, multi_search, mk_bat)


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


class MultiSearchTest(unittest.TestCase):

    #       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
    srtd = [1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 7, 7, 8, 8, 9]

    tbl = [
        (7, 5, 3, 9, 8), #  0
        (7, 5, 8, 7, 1), #  1
        (5, 6, 3, 6, 5), #  2
        (7, 6, 2, 7, 4), #  3
        (7, 6, 4, 0, 8), #  4
        (0, 1, 3, 5, 8), #  5
        (0, 8, 0, 7, 4), #  6
        (6, 4, 5, 4, 5), #  7
        (8, 7, 3, 2, 1), #  8
        (2, 6, 4, 4, 8), #  9

        (2, 6, 4, 4, 8), # 10 (9)
        (6, 4, 5, 4, 5), # 11 (7)
        (7, 5, 3, 9, 8), # 12 (0)
        (5, 6, 3, 6, 5), # 13 (2)
        (7, 6, 4, 0, 8), # 14 (4)
        (8, 7, 3, 2, 1), # 15 (8)
        (7, 6, 4, 0, 8), # 16 (4)
        (7, 5, 8, 7, 1), # 17 (1)
        (6, 4, 5, 4, 5), # 18 (7)
        (5, 6, 3, 6, 5), # 19 (2)
    ]

    def cols_bats(self):
        cols = tuple(zip(*self.tbl))
        bats = [mk_bat(c) for c in cols]
        return cols, bats

    def test_search_single_sorted_array(self):
        tgt_exps = [
            (0, (False, set(), [(0, 0)])),
            (1, (True, set([0, 1]), [(0, 2)])),
            (5, (True, set(range(9, 15)), [(9, 15)])),
            (9, (True, set([19]), [(19, 20)])),
        ]
        for tgt, exp in tgt_exps:
            with self.subTest(tgt):
                actual = multi_search((self.srtd,), (tgt,))
                self.assertEqual(exp, actual)

    def test_search_5_columns(self):
        _, bats = self.cols_bats()
        keys = [lambda i, x: x] * 5
        args_exps = [
            # Fail column 1
            ((tuple(range(5)), (1, 2, 3, 4, 5)),
             (False, set(), [(2, 2), None, None, None, None])),
            # Fail column 2
            ((tuple(range(5)), (2, 7, 7, 4, 5)),
             (False, set(), [(2, 4), (17, 19), None, None, None])),
            # Fail column 3
            ((tuple(range(5)), (0, 8, 3, 8, 7)),
             (False, set(), [(0, 2), (19, 20), (2, 10), None, None])),
            # Fail column 4
            ((tuple(range(5)), (6, 4, 5, 0, 9)),
             (False, set(), [(7, 10), (1, 4), (15, 18), (0, 3), None])),
            # Fail column 5
            ((tuple(range(5)), (7, 5, 3, 9, 5)),
             (False, set(),
              [(10, 18), (4, 8), (2, 10), (18, 20), (6, 12)])),
            # Find unique
            ((tuple(range(5)), (0, 1, 3, 5, 8)),
             (True, set([5]),
              [(0, 2), (0, 1), (2, 10), (10, 11), (12, 20)])),
            # Find multiple
            ((tuple(range(5)), (6, 4, 5, 4, 5)),
             (True, set([7, 11, 18]),
              [(7, 10), (1, 4), (15, 18), (5, 10), (6, 12)])),
        ]
        for args, exp in args_exps:
            with self.subTest(args):
                bat_idxs, tgt = args
                bats_ = tuple(bats[i] for i in bat_idxs)
                actual = multi_search(bats_, tgt, keys)
                self.assertEqual(exp, actual)

    def test_1_sorted_1_binary_association_table(self):
        cols = list(zip(*sorted(t[:2] for t in self.tbl)))
        cols[1] = mk_bat(cols[1])
        keys = [None, lambda i, x: x]
        tgt_exps = [
            ((0, 0), (False, set(), [(0, 2), (0, 0)])),
            ((0, 8), (True, set([1]), [(0, 2), (19, 20)])),
            ((1, 1), (False, set(), [(2, 2), None])),
            ((2, 4), (False, set(), [(2, 4), (1, 4)])),
            ((7, 5), (True, set(range(10, 14)), [(10, 18), (4, 8)])),
            ((7, 6), (True, set(range(14, 18)), [(10, 18), (8, 17)])),
            ((8, 8), (False, set(), [(18, 20), (19, 20)])),
            ((9, 9), (False, set(), [(20, 20), None])),
        ]
        for tgt, exp in tgt_exps:
            with self.subTest(tgt):
                actual = multi_search(cols, tgt, keys)
                self.assertEqual(exp, actual)
