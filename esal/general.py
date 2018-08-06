# Generally useful functions

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
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

def windows(items, window_size):
    """Generates all the contiguous subsequences (windows) of the given size
    in item iteration order.

    * items: Iterable of items.  Instantiated as a tuple if not already
      indexable.
    * window_size: Size of the windows to generate.
    """
    # If the window size is zero, there are no windows
    if window_size <= 0:
        return
    # Instantiate iterable if necessary
    if (not hasattr(items, '__getitem__')
            or not hasattr(items, '__len__')):
        items = tuple(items)
    # If the number of items is zero, there are no windows
    if not items:
        return
    # If the window size is the same or larger than the number of items,
    # there is only one window
    if window_size >= len(items):
        yield items
        return
    # Generate each window
    for start in range(len(items) - window_size + 1):
        yield items[start:start + window_size]

def fq_typename(obj):
    """Returns the fully-qualified type name of an object.

    If the object is a type, returns its fully-qualified name.
    """
    typ = type(obj) if not isinstance(obj, type) else obj
    return '{}.{}'.format(typ.__module__, typ.__qualname__)

def universal_sort_key(obj, key=None):
    """Returns a universal sort key for an object.

    A universal sort key allows an object to be sorted with other
    objects of heterogeneous types without type errors.

    The key for None is (), which sorts before any other universal sort
    key.

    * key: Function to make a sort key from 'obj'.
    """
    if obj is None:
        return ()
    else:
        qualname = fq_typename(obj)
        if key is None:
            return (qualname, obj)
        else:
            return (qualname, key(obj))

def iterable_sort_key(iterable, key=universal_sort_key):
    """Returns a tuple of sort keys, one key for each item in the given
    iterable.

    * key: Function to make a sort key from an item.
    """
    return tuple(key(item) for item in iterable)


class _Any(object):

    """Any is a singleton class that represents all values, a sort of
    complement to None.  Any can be used like None (e.g. 'value is Any')
    but is distinguishable from None.  Its main use is as a placeholder
    or default value when None will not work because None is in the set
    of valid values.
    """

    _instance = None

    __slots__ = ()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

Any = _Any()


def cmp(obj1, obj2):
    if obj1 < obj2:
        return -1
    elif obj1 > obj2:
        return 1
    else:
        return 0
