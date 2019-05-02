# Interval objects and related functionality

# Copyright (c) 2018-2019 Aubrey Barnard.
#
# This is free software released under the MIT License.  See `LICENSE`
# for details.


from enum import Enum

from . import general


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

    # Inverse relations have constants that are negatives of each other

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


def _union(itvl1, itvl2):
    if itvl1.is_empty():
        return (itvl2,)
    elif itvl2.is_empty():
        return (itvl1,)
    elif itvl1.hi < itvl2.lo:
        return (itvl1, itvl2)
    elif itvl2.hi < itvl1.lo:
        return (itvl2, itvl1)
    elif itvl1.hi == itvl2.lo:
        if itvl1.is_hi_open and itvl2.is_lo_open:
            return (itvl1, itvl2)
        else:
            return (Interval(itvl1.lo, itvl2.hi,
                             itvl1.is_lo_open, itvl2.is_hi_open),)
    elif itvl2.hi == itvl1.lo:
        if itvl2.is_hi_open and itvl1.is_lo_open:
            return (itvl2, itvl1)
        else:
            return (Interval(itvl2.lo, itvl1.hi,
                             itvl2.is_lo_open, itvl1.is_hi_open),)
    else:
        lo, lo_open = min((itvl1.lo, itvl1.is_lo_open),
                          (itvl2.lo, itvl2.is_lo_open))
        hi, hi_open = max((itvl1.hi, not itvl1.is_hi_open),
                          (itvl2.hi, not itvl2.is_hi_open))
        hi_open = not hi_open
        return (Interval(lo, hi, lo_open, hi_open),)


def _intersection_bounds(itvl1, itvl2):
    lo, lo_open = max((itvl1.lo, itvl1.is_lo_open),
                      (itvl2.lo, itvl2.is_lo_open))
    hi, hi_open = min((itvl1.hi, not itvl1.is_hi_open),
                      (itvl2.hi, not itvl2.is_hi_open))
    hi_open = not hi_open
    return (lo, hi, lo_open, hi_open)


def _intersection(itvl1, itvl2):
    lo, hi, lo_open, hi_open = _intersection_bounds(itvl1, itvl2)
    # Empty
    if lo > hi:
        return Interval(0, lo_open=True)
    # Either empty or a point depending on if both are closed
    elif lo == hi:
        return Interval(lo, lo_open=(lo_open or hi_open))
    # Overlapping
    else:
        return Interval(lo, hi, lo_open, hi_open)


class Interval:
    """Interval for any orderable type"""

    __slots__ = ('_lo', '_hi', '_lopen', '_hopen', '_length', '_key')

    def __init__(
            self,
            lo,
            hi=None,
            lo_open=False,
            hi_open=False,
            length=None,
    ):
        """
        Create an interval with the given bounds.  The bounds must be
        orderable.

        lo: Lower bound.
        hi: Upper bound.  Omit to create a point.
        lo_open: Whether the interval *excludes* the lower bound.
        hi_open: Whether the interval *excludes* the upper bound.
        length: Length of the interval.  Useful when the bounds do not
            support subtraction.

        A point interval is one where the bounds are equal and closed,
        e.g. "•(8, 8)•".  An empty interval is one where the bounds are
        equal and open, e.g. "◦(8, 8)◦".

        If the bounds support subtraction, then the length of the
        interval will be computed automatically.  Otherwise, you can
        supply your own length.  Similarly, an interval can be
        constructed from `lo` and `length` if the two can be added
        together to set `hi`.

        Examples:

        >>> Interval(8)  # point interval
        >>> Interval(8, lo_open=True)  # empty interval
        >>> Interval(0.0, float('inf'), hi_open=True)  # non-negative reals: •(0,∞)◦
        >>> Interval('a', 'b', length=1)
        >>> 'b' in Interval('a', 'c')  # -> True
        >>> Interval('b', 'c') in Interval('a', 'd')  # -> True
        >>> Interval('b', 'c').allen_relation(Interval('a', 'd'))  # -> <AllenRelation.inside: 2>
        """
        # Default hi to lo or compute it based on the length
        if hi is None:
            if length is None:
                hi = lo
            else:
                hi = lo + length
        # Check that lo <= hi
        if lo > hi:
            raise ValueError(
                'Bad interval bounds: (lo: {!r}) </= (hi: {!r})'
                .format(lo, hi))
        # Compute the length if not provided and if possible
        if length is None:
            try:
                length = hi - lo
            except TypeError:
                pass
        # Make sure point / empty intervals are sensible: both bounds
        # must be open (empty) or both must be closed (point), the
        # length should be zero
        if lo == hi:
            lo_open = lo_open or hi_open
            hi_open = lo_open
            if length is None:
                length = 0
        # Setup the interval from the sane values
        self._lo = lo
        self._hi = hi
        self._lopen = lo_open
        self._hopen = hi_open
        self._length = length
        self._key = None

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

    def is_empty(self):
        return (self._lo == self._hi and
                self._lopen and self._hopen)

    def is_point(self):
        return (self._lo == self._hi and
                not (self._lopen or self._hopen))

    def length(self):
        return self._length

    def key(self):
        if self._key is None:
            self._key = (self.lo, self.is_lo_open,
                         self.hi, not self.is_hi_open)
        return self._key

    def __eq__(self, other):
        return self is other or (
            type(other) is Interval and
            (self.key() == other.key() or
             self.is_empty() and other.is_empty()))

    def __hash__(self):
        if self.is_empty():
            return 0
        else:
            return hash(self.key())

    def __lt__(self, other):
        if other.is_empty():
            return False
        if self.is_empty():
            return True
        return self.key() < other.key()

    def __le__(self, other):
        if self.is_empty():
            return True
        if other.is_empty():
            return False
        return self.key() <= other.key()

    def __gt__(self, other):
        if self.is_empty():
            return False
        if other.is_empty():
            return True
        return self.key() > other.key()

    def __ge__(self, other):
        if other.is_empty():
            return True
        if self.is_empty():
            return False
        return self.key() >= other.key()

    def __repr__(self):
        return 'Interval({!r}, {!r}, {!r}, {!r}, {!r})'.format(
            self.lo,
            self.hi,
            self.is_lo_open,
            self.is_hi_open,
            self.length(),
        )

    def __str__(self):
        return '{}({}, {}){}'.format(
            '◦' if self.is_lo_open else '•',
            self.lo,
            self.hi,
            '◦' if self.is_hi_open else '•',
        )

    # Python set API

    def __contains__(self, item):
        if isinstance(item, Interval):
            return item.issubset(self)
        return (self.lo < item < self.hi or
                (not self.is_lo_open and self.lo == item) or
                (not self.is_hi_open and self.hi == item))

    def issubset(self, other):
        if self.is_empty():
            return True
        if self.lo < other.lo or self.hi > other.hi:
            return False
        return ((self.lo > other.lo or
                 self.is_lo_open >= other.is_lo_open) and
                (self.hi < other.hi or
                 self.is_hi_open >= other.is_hi_open))

    def union(self, *others):
        itvls = [self]
        itvls.extend(others)
        itvls.sort(key=lambda i: (i.lo, i.hi))
        unioned = [itvls[0]]
        for itvl in itvls[1:]:
            unioned[-1:] = _union(unioned[-1], itvl)
        if len(unioned) > 1:
            return CompoundInterval(*unioned)
        else:
            return unioned[0]

    def intersects(self, other):
        lo, hi, lo_open, hi_open = _intersection_bounds(self, other)
        # Empty
        if lo > hi:
            return False
        # Either empty or a point depending on if both are closed
        elif lo == hi:
            return not (lo_open or hi_open)
        # Overlapping
        else:
            return True

    def intersection(self, *others):
        itvl = self
        for other in others:
            itvl = _intersection(itvl, other)
            if itvl.is_empty():
                break
        return itvl

    def difference(self, *others): # TODO
        raise NotImplementedError()

    def symmetric_difference(self, other): # TODO
        raise NotImplementedError()

    # Allen's interval algebra

    def allen_relation(self, other):
        # Order the lo bound wrt the other bounds.  There are 5
        # possibilities, so convert to a base 5 number.
        cmp_lolo = general.cmp(self.lo, other.lo)
        cmp_lohi = general.cmp(self.lo, other.hi)
        lo_num = cmp_lolo + cmp_lohi + 2
        # Order the hi bound wrt the other bounds
        cmp_hilo = general.cmp(self.hi, other.lo)
        cmp_hihi = general.cmp(self.hi, other.hi)
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


class CompoundInterval:

    def __init__(self, *intervals):
        if not intervals:
            raise ValueError('No intervals passed to constructor.')
        _intervals = []
        for itvl in intervals:
            if not isinstance(itvl, Interval):
                raise TypeError('Not an Interval: {!r}'.format(itvl))
            _intervals.append(itvl)
        self._intervals = sorted(_intervals, key=lambda i: (i.lo, i.hi))
        self._hi = max(i.hi for i in self._intervals)

    @property
    def lo(self):
        return self._intervals[0].lo

    @property
    def hi(self):
        return self._hi

    def is_empty(self):
        return all(i.is_empty() for i in self._intervals)

    def length(self):
        """
        Return the sum of the known lengths of the intervals in this
        compound interval or `None` if all of the lengths are unknown.
        """
        lengths = [i.length() for i in self._intervals]
        lengths = [l for l in lengths if l is not None]
        if lengths:
            return sum(lengths)
        else:
            return None

    def __contains__(self, item):
        return any(i.__contains__(item) for i in self._intervals)

    def __len__(self):
        return len(self._intervals)

    def __iter__(self):
        return iter(self._intervals)

    def __repr__(self):
        return 'CompoundInterval({!r})'.format(self._intervals)
