# Event streams and their operations.  Event streams are iterables of
# events.
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools


# Export public API
__all__ = (
    'collect_event_sequences',
    'select',
    )


# Private accessor functions

def _seq_id(event):
    return event.seq


# Functions on event streams

def collect_event_sequences(events):
    """Collects events into sequences by grouping by sequence ID.

    Returns an event sequence stream given an event stream.  The input
    events must already be sorted by sequence ID.
    """
    for _, sequence in itools.groupby(events, key=_seq_id):
        # Keep event sequences as iterables rather than instantiating to
        # any particular collection
        yield sequence

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
