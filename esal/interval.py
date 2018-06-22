# Interval objects and related functionality

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

from enum import Enum


# Export public API
__all__ = (
    'AllenRelation',
    'Interval',
)


class AllenRelation(Enum):
    """
    The relations of Allen's interval algebra.

    https://en.wikipedia.org/wiki/Allen%27s_interval_algebra
    """

    # Inververse relations have constants that are negatives of each
    # other

                        # Sorted order
    before = -6         #  0: a1 a2 b1 b2
    abut_before = -5    #  1: a1 a2=b1 b2
    overlap_before = -4 #  2: a1 b1 a2 b2
    outside_end = -3    #  3: a1 b1 a2=b2
    outside = -2        #  4: a1 b1 b2 a2
                        #  5: a1=a2=b1 b2
    inside_begin = -1   #  6: a1=b1 a2 b2
    equal = 0           #  7: a1=b1 a2=b2
    outside_begin = 1   #  8: a1=b1 b2 a2
    inside = 2          #  9: b1 a1 a2 b2
    inside_end = 3      # 10: b1 a1 a2=b2
    overlap_after = 4   # 11: b1 a1 b2 a2
                        # 12: b1 b2=a1=a2
    abut_after = 5      # 13: b1 b2=a1 a2
    after = 6           # 14: b1 b2 a1 a2

    def is_inverse(self, other):
        return self.value == -other.value

    def inverse(self):
        return AllenRelation(-self.value)


def _cmp(obj1, obj2):
    if obj1 < obj2:
        return -1
    elif obj1 > obj2:
        return 1
    else:
        return 0


class Interval:
    """Interval for any orderable type"""

    # TODO slots

    def __init__(
            self,
            lo,
            hi=None,
            lo_open=False,
            hi_open=False,
            length=None,
    ):
        self._lo = lo
        self._hi = hi if hi is not None else lo
        self._lopen = lo_open
        self._hopen = hi_open
        self._len = length
        # Make sure lo <= hi
        if lo > hi:
            self._lo = hi
            self._hi = lo
        assert self._lo <= self._hi
        # Make sure point intervals are sensible
        if self._lo == self._hi:
            self._lopen = False
            self._hopen = False
            self._len = 0
        # Try to compute the length
        elif length is None:
            try:
                self._len = hi - lo
            except TypeError:
                pass

    @property
    def lo(self):
        return self._lo

    @property
    def hi(self):
        return self._hi

    @property
    def is_lo_open(self):
        return self._lopen

    @property
    def is_hi_open(self):
        return self._hopen

    def __len__(self):
        """
        Return the length of this interval or `None` if the length is
        unknown.
        """
        return self._len

    # Python set API

    def __contains__(self, item):
        return (self.lo < item < self.hi or
                (not self.is_lo_open and self.lo == item) or
                (not self.is_hi_open and self.hi == item))

    def issubset(self, other):
        pass # TODO

    def union(self, *others):
        pass # TODO

    def intersection(self, *others):
        pass # TODO

    def difference(self, *others):
        pass # TODO

    def symmetric_difference(self, other):
        pass # TODO

    # Allen's interval algebra

    def allen_relation(self, other):
        # Order the lo bound wrt the other bounds.  There are 5
        # possibilities, so convert to a base 5 number.
        cmp_lolo = _cmp(self.lo, other.lo)
        cmp_lohi = _cmp(self.lo, other.hi)
        lo_num = cmp_lolo + cmp_lohi + 2
        # Order the hi bound wrt the other bounds
        cmp_hilo = _cmp(self.hi, other.lo)
        cmp_hihi = _cmp(self.hi, other.hi)
        hi_num = cmp_hilo + cmp_hihi + 2
        # The hi number must be at least the lo number.  This limits the
        # possibilities to [5, 4, 3, 2, 1].  The cumulative sums of this
        # are the lo bases.  Use these facts to calculate the number
        # corresponding to the Allen relation.
        lo_bases = [0, 5, 9, 12, 14]
        allen_num = lo_bases[lo_num] + hi_num - lo_num
        # Correct for if both lo and hi equal an endpoint of the other
        # interval.  (Allen's algebra doesn't distinguish these cases.)
        # These are (lo=1, hi=1) -> 5 and (lo=3, hi=3) -> 12.  Since 12
        # is "abut after", make 5 be "abut before" for symmetry.  This
        # breaks the sorted order but it maintains inverses.
        if allen_num > 12:
            allen_num -= 2
        elif allen_num > 5:
            allen_num -= 1
        elif allen_num == 5:
            allen_num = 1
        # The Allen number is now in [0:12].  Convert it to an
        # enumeration number and return the relation.
        return AllenRelation(allen_num - 6)
