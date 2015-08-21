# Event sequences.  An event sequence is an iterable of events where all
# the events have the same sequence ID.
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.


# Event sequence objects

class _EventSequence(object): # TODO?
    """A sequence of events."""

    def __init__(self, sequence_id, events):
        # Initialize members
        self._seq_id = sequence_id
        self._events = []
        self._times = None
        self._duras = None
        self._values = None
        # Set members from 'events' depending on type
        for idx, event in enumerate(events):
            pass
