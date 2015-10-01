# Event sequences.  An event sequence is an iterable of events where all
# the events have the same sequence ID.
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import collections.abc
import itertools as itools
import random

from . import events
from .general import Any


# Export public API
__all__ = (
    'data_order',
    'random_order',
    'order_concurrent_events',
    'timelines_to_sequences',
    )


# Private accessor functions

def _time(event):
    return event.time


# Some orderings

def data_order(events):
    return events

def random_order(events):
    events = list(events)
    random.shuffle(events)
    return events


# Functions on sequences

def order_concurrent_events(timeline, ordering=data_order):
    """Orders concurrent events in a timeline according to the given
    ordering so as to create a total order of events.

    * timeline: Iterable of events in temporal order (sorted by time)
    * ordering: Function (iterable of events) -> (iterable of events).
      The input events for the given ordering function will have equal
      times (concurrent events).  The ordering function should output
      events in their total order.  The default ordering function is
      data order (identity function).

    Returns an iterable of events where the events are in their total
    order.
    """
    for _, concurrent_events in itools.groupby(timeline, key=_time):
        for event in ordering(concurrent_events):
            yield event

def timeline_to_sequence(timeline, start=0):
    """Converts a timeline to a sequence by replacing event times with
    event indices.

    * timeline: Iterable of events
    * start: Start number for numbering events

    Returns an iterable of events where the events have indices in the
    order of `timeline` instead of times.
    """
    for order, event in enumerate(timeline, start):
        yield events.Event(
            event.seq, order, event.dura, event.typ, event.val)

def make_timeline_to_sequence_flattener(ordering=data_order, start=0):
    """Makes a function that will order concurrent events and convert
    them to a sequence.

    * ordering: Function to order concurrent events
    * start: Start number for numbering events

    See order_concurrent_events and timeline_to_sequence for details.
    """
    def flattener(timeline):
        return timeline_to_sequence(
            order_concurrent_events(timeline, ordering), start)
    return flattener


class EventSequence(collections.abc.Sequence):
    """A collection of events in temporal order."""

    def __init__(self, events):
        self.events = sorted(events, key=lambda e: e.sort_key())

    def __len__(self):
        return len(self.events)

    def __getitem__(self, key):
        return self.events[key]

    def __contains__(self, obj):
        """Returns whether this event sequence contains an event with
        the given value of the named field or whether this event
        sequence contains the given object.

        * obj: A (field_name::str, value) pair or some object (typically
          an Event).  If 'obj' is a (::str, ::object) pair, this
          searches for an Event with a field with the given value.
          Otherwise, this just searches for the given object (which must
          be an Event to succeed).
        """
        if (isinstance(obj, tuple) and len(obj) == 2 and
                isinstance(obj[0], str)):
            field, value = obj
            return value in (ev[field] for ev in self.events)
        else:
            return obj in self.events

    def times(self):
        """Returns the times of the events in sequence order."""
        yield from (ev.time for ev in self.events)

    def types(self):
        """Returns the types of the events in sequence order."""
        yield from (ev.typ for ev in self.events)

    def match(self, seq=Any, time=Any, dura=Any, typ=Any, val=Any,
              start=0, stop=None):
        """Returns the index of the first event that matches the given
        field values.

        Matching works as for Event.matches.  Providing 'start' and
        'stop' limits the search to that slice, like for list.index.
        """
        stop = len(self.events) if stop is None else stop
        for idx in range(start, stop):
            if self.events[idx].matches(seq, time, dura, typ, val):
                return idx
        return None

    def matches(self, seq=Any, time=Any, dura=Any, typ=Any, val=Any):
        """Returns the indices of all the matches that would be returned
        by successive calls to 'match'.
        """
        yield from (idx for idx, event in enumerate(self.events)
                    if event.matches(seq, time, dura, typ, val))
