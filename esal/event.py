# Events and event sequences

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.


import bisect
import collections

from . import interval


class Event:

    __slots__ = ('_type', '_when', '_val')

    def __init__(self, type, when, value=None):
        if not isinstance(when, interval.Interval):
            raise TypeError('Not an `Interval`: {!r}'.format(when))
        self._type = type
        self._when = when
        self._val = value

    def __repr__(self):
        return 'Event({!r}, {!r}, {!r})'.format(
            self.type, self.when, self.value)

    @property
    def type(self):
        return self._type

    @property
    def when(self):
        return self._when

    @property
    def value(self):
        return self._val

    def __eq__(self, other):
        return self is other or (
            isinstance(other, Event) and
            self.when == other.when and
            self.type == other.type and
            self.value == other.value)

    def __hash__(self):
        return hash((self.type, self.when, self.value))


class EventSequence:

    def __init__(self, id, events):
        self._id = id
        self._events = list(events)
        # Sort the events by when they occurred
        self._events.sort(key=lambda e: (e.when.key(), e.type))
        # Build an index of times
        self._keys = [e.when.key() for e in self._events]
        # Build an index of event types to events
        types2evs = collections.defaultdict(list)
        for event in self._events:
            types2evs[event.type].append(event)
        self._types2evs = types2evs

    def __repr__(self):
        return 'EventSequence({!r}, {!r})'.format(
            self._id, self._events)

    def __len__(self):
        return len(self._events)

    def __getitem__(self, index):
        return self._events[index]

    def __iter__(self):
        return iter(self._events)

    events = __iter__

    def types(self):
        return self._types2evs.keys()

    def n_events_of_type(self, type):
        return len(self._types2evs.get(type, ()))

    def events_of_type(self, type):
        return iter(self._types2evs.get(type, ()))

    def _search_for_interval(self, itvl):
        key = itvl.key()
        i1 = bisect.bisect_left(self._keys, key)
        i2 = bisect.bisect_right(self._keys, key, lo=i1)
        return (i1 < i2, i1, i2)

    def events_within(self, interval): # TODO
        raise NotImplementedError()

    def events_overlapping(self, interval): # TODO
        raise NotImplementedError()

    def __contains__(self, item):
        if isinstance(item, interval.Interval):
            is_found, _, _ = self._search_for_interval(item)
            return is_found
        elif isinstance(item, Event):
            is_found, lo, hi = self._search_for_interval(item.when)
            if not is_found:
                return False
            for i in range(lo, hi):
                if self._events[i] == item:
                    return True
            return False
        else:
            return item in self._types2evs

    def before(self, type1, type2):
        if type1 not in self._types2evs or type2 not in self._types2evs:
            return False
        ev1 = self._types2evs[type1][0]
        ev2 = self._types2evs[type2][-1]
        return ev1.when.hi < ev2.when.lo

    def first(self, type):
        if type not in self._types2evs:
            raise ValueError('Event type not found: {!r}'.format(type))
        return self._types2evs[type][0]
