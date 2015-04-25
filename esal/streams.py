# Operations on event streams.  Event streams are iterables of events.
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools


# Export public API
__all__ = (
    'collect_event_sequences',
    'select',
    )


def _seq_id(event):
    return event.seq

def collect_event_sequences(events):
    """Collects events into sequences by grouping by sequence ID.

    Returns an event sequence stream given an event stream.  The input
    events must already be sorted by sequence ID.
    """
    for _, group in itools.groupby(events, key=_seq_id):
        yield tuple(group) # TODO event sequence objects instead of tuples?
        # tuple() is OK instead of list() as times are about the same:
        # timeit.timeit('tuple(range(1000))')
        # timeit.timeit('list(range(1000))')

def select(events, field, values):
    """Selects events where the value of the indicated field is in the
    given set of values.

    Returns an event stream given an event stream.  The field may be
    indicated by name or index.  The set of values can be any collection
    or other object (e.g. range) that supports 'in'.
    """
    for event in events:
        value = (event[field]
                 if isinstance(field, int)
                 else getattr(event, field))
        if value in values:
            yield event
