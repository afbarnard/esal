# Fundamental data processing operations
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

def select(items, predicate):
    for item in items:
        if predicate(item):
            yield item

def project(items, field_indices):
    for item in items:
        yield tuple(item[i] for i in field_indices)

def count(items):
    # Return length if already known
    if hasattr(items, '__len__'):
        return len(items)
    # Else count items
    c = 0
    for item in items:
        c += 1
    return c

def distinct(items):
    return set(items)
