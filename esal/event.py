# Events and event sequences

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.


import heapq
import operator
import sys

from . import interval
from . import sorted_search as sose


# Export public API
__all__ = (
    'Event',
    'EventSequence',
)


class Event:

    __slots__ = ('_when', '_type', '_val')

    def __init__(self, when, type, value=None):
        """
        Create an event of the given type that occurs over the given time
        span with the given value.

        when: When the event occurred.  Any orderable.
        type: Event type.  Any hashable.
        value: Arbitrary value associated with the event.  Optional.
            If you want this `Event` to be hashable, then its value must
            also be hashable.
        """
        self._when = when
        self._type = type
        self._val = value

    def __repr__(self):
        return 'Event({!r}, {!r}, {!r})'.format(
            self.when, self.type, self.value)

    @property
    def when(self):
        return self._when

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._val

    def key(self):
        return (self.when, self.type, self.value)

    def __eq__(self, other):
        return self is other or (
            isinstance(other, Event) and
            self.when == other.when and
            self.type == other.type and
            self.value == other.value)

    def __hash__(self):
        return hash(self.key())


class EventSequence:

    def __init__(self, events, facts=None, id_=None):
        """
        Create a sequence from the given events and facts.

        events: Iterable of events.
        facts: Iterable of (key, value) pairs, the atemporal
            information about this sequence.
        id_: Arbitrary sequence identifier.
        """
        # Store ID and facts
        self._id = id_ if id_ is not None else id(self)
        self._facts = dict(facts) if facts else {}
        # Store the events by ascending `when`
        evs = [(e.when, e) for e in events]
        evs.sort(key=lambda p: (p[0], p[1].type))
        # Keep the `when`s to use as an index
        whens_events = tuple(zip(*evs))
        self._whens, self._events = (whens_events
                                     if whens_events
                                     else ((), ()))
        # Build an index of event types to events
        types2evs = {}
        for idx, event in enumerate(self._events):
            typ = event.type
            if typ in types2evs:
                types2evs[typ].append(idx)
            else:
                types2evs[typ] = [idx]
        self._types2evs = types2evs
        self._when_type = (type(self._events[0].when)
                           if len(self._events) > 0
                           else object)

    def __repr__(self):
        return ('EventSequence(id_={!r}, facts={!r}, events={!r})'
                .format(self._id, self._facts, self._events))

    @property
    def id(self):
        return self._id

    def __len__(self):
        return len(self._events)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._events[index]
        else:
            return self._facts[index]

    def __setitem__(self, key, val):
        if isinstance(key, int):
            raise Exception('Integers index events, but events are '
                            'read-only, so integer indices are not '
                            'allowed: {!r}'.format(key))
        self._facts[key] = val

    def __iter__(self):
        return iter(self._events)

    def facts(self):
        if self._facts is not None:
            return self._facts.items()
        else:
            return ()

    def events(self, *types):
        if not types:
            yield from self._events
        else:
            for event_index in heapq.merge(
                    *(self._types2evs.get(t, ()) for t in types)):
                yield self._events[event_index]

    def types(self):
        return self._types2evs.keys()

    def has_fact(self, key):
        return key in self._facts

    def fact(self, key, default=None):
        return self._facts.get(key, default)

    def n_events_of_type(self, type):
        return len(self._types2evs.get(type, ()))

    def events_between(self, when_lo=None, when_hi=None):
        """
        Return a tuple containing the events in the given interval
        (inclusive).

        when_lo: Lower bound or unlimited if `None`.
        when_hi: Upper bound or unlimited if `None`.
        """
        # Find the events in the interval
        if when_lo is not None and when_hi is not None:
            _, (lo, hi) = sose.binary_search(
                self._whens, when_lo, target_key_hi=when_hi,
                target=sose.Target.range)
        elif when_lo is not None:
            _, lo = sose.binary_search(
                self._whens, when_lo, target=sose.Target.lo)
            hi = len(self)
        elif when_hi is not None:
            _, hi = sose.binary_search(
                self._whens, when_hi, target=sose.Target.hi)
            lo = 0
        else:
            lo = 0
            hi = len(self)
        # Return the slice with the selected events
        return self._events[lo:hi]

    def has_event(self, event):
        found, (lo, hi) = sose.binary_search(
            self._whens, event.when, target=sose.Target.range)
        if not found:
            return False
        found, (lo, hi) = sose.binary_search(
            self._events, event.type, lo=lo, hi=hi,
            target=sose.Target.range, key=lambda i, x: x.type)
        if not found:
            return False
        for i in range(lo, hi):
            if self._events[i] == event:
                return True
        return False

    def has_type(self, type):
        return type in self._types2evs

    def has_when(self, when):
        found, _ = sose.binary_search(
            self._whens, when, target=sose.Target.any)
        return found

    def __contains__(self, item):
        if isinstance(item, Event):
            return self.has_event(item)
        elif isinstance(item, self._when_type):
            return self.has_when(item)
        else:
            return item in self._types2evs

    def has_types(self, *types):
        for type in types:
            if type not in self._types2evs:
                return False
        return True # ENH return proof, perhaps as separate method 'occur'?

    def first(self, type, after=None, strict=True):
        ev_idxs = self._types2evs.get(type)
        if ev_idxs is None:
            return (False, None)
        if after is None:
            idx = ev_idxs[0]
            return (True, (idx, self._events[idx]))
        # Find the first event after the given when.  Search for the
        # range equalling when to accommodate both strictly after and
        # not strictly after.
        _, (lo, hi) = sose.binary_search(
            ev_idxs,
            after,
            key=lambda i, x: self._whens[x],
            target=sose.Target.range,
        )
        if strict and hi < len(ev_idxs):
            idx = ev_idxs[hi]
            return (True, (idx, self._events[idx]))
        elif not strict and lo < len(ev_idxs):
            idx = ev_idxs[lo]
            return (True, (idx, self._events[idx]))
        else:
            return (False, None)

    def before(self, type1, type2, *types, strict=True):
        if len(types) == 0:
            t1_idxs = self._types2evs.get(type1)
            t2_idxs = self._types2evs.get(type2)
            if t1_idxs and t2_idxs:
                lte_cmp = operator.lt if strict else operator.le
                return lte_cmp(self._whens[t1_idxs[0]],
                               self._whens[t2_idxs[-1]])
            else:
                return False
        else:
            min_t = self._whens[0]
            for type in (type1, type2, *types):
                ev_idxs = self._types2evs.get(type, ())
                if not ev_idxs:
                    return False
                _, lo = sose.binary_search(
                    ev_idxs,
                    min_t,
                    key=lambda i, x: self._whens[x],
                    target=sose.Target.lo,
                )
                if lo < len(ev_idxs):
                    min_t = self._whens[ev_idxs[lo]]
                    if strict:
                        found, hi = sose.binary_search(
                            self._whens, min_t, target=sose.Target.hi)
                        if hi < len(self._whens):
                            min_t = self._whens[hi]
                        elif found:
                            min_t = self._whens[-1]
                        else:
                            return False
                else:
                    return False
            return True

    def subsequence(self, when_lo=None, when_hi=None):
        """
        Return a copy of this event sequence that contains only the events
        in the given interval (inclusive).

        when_lo: Lower bound or unlimited if `None`.
        when_hi: Upper bound or unlimited if `None`.
        """
        return self.copy(
            events=self.events_between(when_lo, when_hi))

    def pprint(self, margin=0, indent=2, file=sys.stdout): # TODO format `when`s and `value`s
        margin_space = ' ' * margin
        indent_space = ' ' * indent
        file.write(margin_space)
        file.write('EventSequence(\n')
        file.write(margin_space)
        file.write(indent_space)
        file.write('id: ')
        file.write(str(self.id))
        file.write('\n')
        if self._facts:
            for k in sorted(self._facts.keys()):
                file.write(margin_space)
                file.write(indent_space)
                file.write(str(k))
                file.write(': ')
                file.write(str(self._facts[k]))
                file.write('\n')
        for e in self._events:
            file.write(margin_space)
            file.write(indent_space)
            file.write(str(e.when))
            file.write(': ')
            file.write(str(e.type))
            if e.value is not None:
                file.write(' ')
                file.write(str(e.value))
            file.write('\n')
        file.write(margin_space)
        file.write(')\n')

    def copy(self, events=None, facts=None, id_=None):
        """
        Copy this event sequence, replacing existing fields with the given
        values.
        """
        return EventSequence(
            events=events if events is not None else self.events(),
            facts=facts if facts is not None else self.facts(),
            id_=id_ if id_ is not None else self.id,
        )
