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
