# Common test data
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

from .. import events


# Raw tuples for simple events
#
# >>> sorted((random.randrange(3), random.randrange(10), random.choice('abcde')) for i in range(10))
simple_event_tuples = (
    (0, 1, 'a'),
    (0, 1, 'b'),
    (0, 4, 'd'),
    (0, 5, 'c'),
    (1, 6, 'a'),
    (2, 0, 'e'),
    (2, 1, 'a'),
    (2, 2, 'b'),
    (2, 4, 'd'),
    (2, 6, 'b'),
    )

# Event tuples for simple events
simple_events = tuple(
    map(lambda tup: events.Event(seq=tup[0], time=tup[1], ev=tup[2]),
        simple_event_tuples))
