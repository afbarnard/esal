# Fundamental data processing operations
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

def select(items, predicate):
    for item in items:
        if predicate(item):
            yield item

def count(items):
    # TODO use len if available
    c = 0
    for item in items:
        c += 1
    return c
