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
    # TODO use len if available
    c = 0
    for item in items:
        c += 1
    return c

def count_distinct(items):
    distinct_items = set()
    for item in items:
        distinct_items.add(item)
    return len(distinct_items)
