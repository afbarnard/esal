# Generally useful functions
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools


def firsts(items, key=None):
    """Generates the first occurrence of each unique item.

    * items: Iterable of items.
    * key: Function computing the key for each item.  The key determines
      whether an item is unique.  If key is 'None', the item is its own
      key.

    Uses memory proportional to the number of unique keys.
    """
    seen = set()
    for item in items:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            yield item

def _getitems_indexable(indexable_items, indices):
    if indexable_items: # __bool__ calls __len__, which was assumed
        for idx in indices:
            yield indexable_items[idx]

def _getitems_iterable(iterable_items, indices):
    # This is basically a one-sided merge join algorithm when given
    # sorted indices.  It is one-sided in the sense that the item index
    # will keep increasing and will not be repeated but some of the
    # given indices may be repeated.

    # Sort the indices in a way that notes the original order
    sorted_pairs = sorted(zip(indices, itools.count()))
    # Return if the indices are empty
    if not sorted_pairs:
        return
    # Setup
    item_iter = iter(iterable_items)
    item_idx = 0
    items = [None] * len(sorted_pairs)
    # Catch iteration termination
    try:
        item = next(item_iter)
        # Get an item (by index) for each of the specified indices
        for index, order in sorted_pairs:
            while item_idx < index:
                item = next(item_iter)
                item_idx += 1
            items[order] = item
    except StopIteration:
        pass
    # Return if the iterable is empty
    if item_idx == 0:
        return
    # Generate the items
    for item in items:
        yield item

def getitems(items, indices):
    """Generates the items at the given indices.

    * items: Iterable of items.
    * indices: Iterable of indices of the items to return.

    If 'items' is indexable then the items are accessed by index.
    Otherwise, if 'items' is only iterable, then the indices are joined
    against the items.  The join algorithm expects that there are many
    more items than indices, and so uses memory proportional to the
    number of indices.
    """
    if hasattr(items, '__getitem__') and hasattr(items, '__len__'):
        return _getitems_indexable(items, indices)
    else:
        return _getitems_iterable(items, indices)
