# Generally useful functions
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

def firsts(items, key=None):
    """Generates the first occurrence of each unique item.

    * items: Iterable of items
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
