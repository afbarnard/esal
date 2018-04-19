# Event sequences.  An event sequence is an iterable of events where all
# the events have the same sequence ID.

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
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
    """
    Orders concurrent events in a timeline according to the given
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
    """
    Converts a timeline to a sequence by replacing event times with event
    indices.

    * timeline: Iterable of events
    * start: Start number for numbering events

    Returns an iterable of events where the events have indices in the
    order of `timeline` instead of times.
    """
    for order, event in enumerate(timeline, start):
        yield events.Event(
            event.seq, order, event.end, event.typ, event.val)


def make_timeline_to_sequence_flattener(ordering=data_order, start=0):
    """
    Makes a function that will order concurrent events and convert them
    to a sequence.

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

    def __init__(self, events, facts=None, seq_id=None):
        # Store events ordered by start time
        self._events = sorted(events, key=lambda e: e.time)
        # Store facts in a dictionary
        self._facts = None
        if facts:
            self._facts = dict(facts)
        # Assign sequence ID, searching for it if necessary
        self._id = seq_id
        idx = 0
        while self._id is None:
            self._id = self._events[idx].seq
            idx += 1
        # Create an index of events by type
        self._typs2idxs = {}
        for idx, ev in enumerate(self._events):
            typ = ev.typ
            idxs = self._typs2idxs.get(typ)
            if idxs is None:
                idxs = []
                self._typs2idxs[typ] = idxs
            idxs.append(idx)

    def __len__(self):
        return len(self._events)

    def __getitem__(self, key):
        return self._events[key]

    def __iter__(self):
        return iter(self._events)

    def __contains__(self, event):
        """
        Return whether this event sequence contains the specified event.

        The event can be specified as an Event object or as an event
        type.
        """
        if isinstance(event, events.Event):
            return self.has_event(event)
        else:
            return self.has_type(event)

    @property
    def id(self):
        return self._id

    def has_type(self, typ):
        return typ in self._typs2idxs

    def has_event(self, event):
        for idx in self._typs2idxs.get(event.typ, ()): # TODO use binary search
            if self[idx] == event:
                return True
        return False

    def events_of_type(self, typ):
        for idx in self._typs2idxs.get(typ, ()):
            yield self[idx]

    def event_types(self):
        return self._typs2idxs.keys()

    events = __iter__

    def events_in(self, start_time=None, end_time=None):
        # Find the index of the event with the given start time
        ev_idx = 0
        if start_time is not None:
            # Find the start time using binary search.  The `bisect`
            # module doesn't work because it doesn't support a separate
            # key like `sorted` does.
            lo = 0
            hi = len(self._events)
            while lo < hi:
                mid = (lo + hi) // 2
                # Find the first occurrence of any times tied with the
                # start.  Make sure to make progress by not repeating
                # the lo or hi bounds.
                if start_time <= self[mid].time:
                    hi = (mid if mid < hi else hi - 1)
                else:
                    lo = (mid if mid > lo else lo + 1)
            ev_idx = lo
        # Generate the events until the end time
        while (ev_idx < len(self._events) and
               (end_time is None or self[ev_idx].time <= end_time)):
            yield self[ev_idx]
            ev_idx += 1

    def times(self):
        """Return the times of the events in sequence order."""
        return (ev.time for ev in self._events)

    def ends(self):
        """Return the end times of the events in sequence order."""
        return (ev.end for ev in self._events)

    def types(self):
        """Return the types of the events in sequence order."""
        return (ev.typ for ev in self._events)

    def facts(self):
        if self._facts is not None:
            return self._facts.items()
        else:
            return ()

    def time_span(self):
        return (min(e.time for e in self._events),
                max(e.end for e in self._events)) # FIXME handle None

    def subsequence(self, start_time=None, end_time=None):
        return EventSequence(
            self.events_in(start_time, end_time), self.facts(), self.id)

    def match(self, seq=Any, time=Any, end=Any, typ=Any, val=Any,
              start=0, stop=None):
        """
        Return the index of the first event that matches the given field
        values.

        Matching works as for Event.matches.  Providing 'start' and
        'stop' limits the search to that slice, like for list.index.
        """
        stop = len(self._events) if stop is None else stop
        for idx in range(start, stop):
            if self._events[idx].matches(seq, time, end, typ, val):
                return idx
        return None

    def matches(self, seq=Any, time=Any, end=Any, typ=Any, val=Any):
        """
        Return the indices of all the matches that would be returned by
        successive calls to 'match'.
        """
        return (idx for idx, event in enumerate(self._events)
                if event.matches(seq, time, end, typ, val))
