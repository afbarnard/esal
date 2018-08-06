# Searches on sorted lists

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.


from enum import Enum

from . import general


class Target(Enum):
    """
    Search targets

    * any: existence (any match is OK)
    * lo: left insertion point (first of an equal run)
    * hi: right insertion point (last + 1 of an equal run)
    * range: (lo, hi)
    """
    any = 0
    lo = 1
    hi = 2
    range = 3


# Binary search implemented to support all the search targets (where
# range is implemented by first searching for left and then searching
# for right)
def _binary_search(
        items,
        lo_key,
        hi_key=None,
        key=None,
        lo=None,
        hi=None,
        target=Target.any,
):
    """
    Generalized binary search implementation that supports all
    `Target`s.

    Existence queries are supported by returning as soon as an exemplar
    is found.

    Left / Right insertion point queries are supported by searching for
    the first / last of an equal run such that the equal run is
    precisely the slice [left:right].

    Range queries return the range of the equal run: [left:right].  They
    are supported by tracking and returning the tightest bounds on the
    right insertion point.  Thus, range queries can be implemented by
    first searching for the left insertion point and then searching for
    the right insertion point using the returned bounds.

    In all cases, if the target is not found, then the returned target
    index is the index at which to insert the target item in sorted
    order.

    Return (target found?, target index, right insertion lower bound,
    right insertion upper bound).
    """
    lo = 0 if lo is None else max(lo, 0)
    hi = len(items) if hi is None else min(hi, len(items))
    #print(items, lo, hi)
    #print('t:', lo_key, target, hi_key)
    # Initial values suitable for returning immediately
    mid = hi + 1
    direction = 1
    # Saved comparison results
    lo_dir = -1
    hi_dir = 1
    # Bounds on the right insertion point
    hi_le = lo
    hi_gt = hi
    while lo < hi:
        # Get the next item
        mid = (lo + hi) // 2
        #print('b:', lo, mid, hi, '-', hi_le, hi_gt)
        item = items[mid]
        #print('i:', item)
        # Compare the target key to the item key
        item_key = key(mid, item) if key is not None else item
        direction = general.cmp(lo_key, item_key)
        #print('k:', lo_key, item_key, direction)
        # Keep searching to the left (decrease hi)
        if direction < 0 or (direction == 0 and target == Target.lo):
            # Ensure progress by not repeating the hi bound
            hi = (mid if mid < hi else hi - 1)
            # Save the comparison result
            hi_dir = direction
            # Update the bounds on the right insertion point
            if hi_key is not None:
                dir_hi_key = (general.cmp(hi_key, item_key)
                              if hi_key != lo_key else direction)
                #print('k:', hi_key, item_key, dir_hi_key)
                if dir_hi_key < 0:
                    hi_gt = hi
                elif hi > hi_le:
                    hi_le = hi
        # Keep searching to the right (increase lo)
        elif direction > 0 or (direction == 0 and target == Target.hi):
            # Ensure progress by not repeating the lo bound
            lo = (mid if mid > lo else lo + 1)
            # Save the comparison result
            lo_dir = direction
            # Update the lower bound on the right insertion point
            if hi_key is not None and lo > hi_le:
                hi_le = lo
        # Found any target
        else: # direction == 0 and target == Target.any
            return (True, mid, hi_le, hi_gt)
    # At the end of the loop `lo` is at either the left or right
    # insertion point depending on the desired target
    #print('b:', lo, mid, hi, '-', hi_le, hi_gt)
    # Retrieve a comparison result if `lo` isn't at `mid`
    if lo != mid:
        direction = lo_dir * hi_dir
    # Return whether the target was found, its location, and bounds on
    # the right insertion point
    return (direction == 0, lo, hi_le, hi_gt)


def binary_search(
        items,
        target_key,
        target_key_hi=None,
        key=None,
        lo=None,
        hi=None,
        target=Target.any,
):
    """
    Search for a target key using binary search and return (found?,
    index / range).

    The returned index / range is as follows according to the desired
    target:
    * Target.lo: lo
    * Target.hi: hi
    * Target.any: Any `x` such that `lo <= x < hi`
    * Target.range: (lo, hi)
    Where:
    * `lo` is the smallest index s.t. `target_key <= key(items[lo])`
    * `hi` is the smallest index s.t. `target_key_hi < key(items[hi])`
    Thus, the slice of items matching the target key(s) is `[lo:hi]`.

    Arguments:
    * items: Indexable such that its keys are sorted.
    * target_key: What to search for.  Keys must be orderable.
    * key: Key function taking arguments (index, item) that returns the
      sort key for the item at the given index.  (This allows one to
      have a separate array of keys.)  If `None`, items are their own
      keys.
    * lo: Initial lower bound index (inclusive)
    * hi: Initial upper bound index (exclusive)
    * target: What in the items to target: existence, low index, high
      index, or the whole range.  See `Target`.
    * target_key_hi: If searching for a range, search for target keys k
      in `target_key <= k < target_key_hi`.  (Ignored otherwise.)
    """
    if target == Target.range:
        if target_key_hi is None:
            target_key_hi = target_key
        _, lo_idx, hi_le, hi_gt = _binary_search(
            items, target_key, target_key_hi, key, lo, hi, Target.lo)
        _, hi_idx, _, _ = _binary_search(
            items, target_key_hi, None, key, hi_le, hi_gt, Target.hi)
        return (lo_idx < hi_idx, (lo_idx, hi_idx))
    else:
        found, idx, _, _ = _binary_search(
            items, target_key, None, key, lo, hi, target)
        return (found, idx)
