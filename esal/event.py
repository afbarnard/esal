# Events and event sequences

# Copyright (c) 2018-2019 Aubrey Barnard.
#
# This is free software released under the MIT License.  See `LICENSE`
# for details.


import builtins
import heapq
import itertools as itools
import operator
import sys

from . import interval
from . import sorted_search as sose


# Export public API
__all__ = (
    'Event',
    'EventSequence',
    'mk_union_aggregator',
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
    """A read-only sequence of events optimized for querying"""

    def __init__(self, events, facts=None, id=None):
        """
        Create a sequence from the given events and facts.

        events:
            Iterable of `esal.Event`.
        facts:
            Iterable of (key, value) pairs, the atemporal information
            about this sequence.
        id:
            Arbitrary sequence identifier.
        """
        # Store ID and facts
        self._id = id if id is not None else builtins.id(self)
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

    # Printing

    def __repr__(self):
        return ('EventSequence(id={!r}, facts={!r}, events={!r})'
                .format(self._id, self._facts, self._events))

    def pprint(self, margin=0, indent=2, file=sys.stdout): # TODO format `when`s and `value`s # TODO redo in terms of `print`?
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

    # Properties

    @property
    def id(self):
        return self._id

    # Collection emulation

    def __len__(self):
        """Return the number of events contained in this sequence."""
        return len(self._events)

    n_events = __len__

    def __getitem__(self, index):
        """
        Return the event(s) or fact indicated by the given integer index
        (event), slice (events), or key (fact).

        index: int | slice | object
        """
        if isinstance(index, (int, slice)):
            return self._events[index]
        else:
            return self._facts[index]

    def __setitem__(self, key, val): # TODO remove in favor of some method of modification by derivation
        if isinstance(key, int):
            raise Exception('Integers index events, but events are '
                            'read-only, so integer indices are not '
                            'allowed: {!r}'.format(key))
        self._facts[key] = val

    def __iter__(self):
        """Return iterator over this sequence's events."""
        return iter(self._events)

    def __contains__(self, item):
        """
        Whether this sequence contains the given item.

        item:
            An `esal.Event`, a when, or an event type.
        """
        if isinstance(item, Event):
            return self.has_event(item)
        elif isinstance(item, self._when_type):
            return self.has_when(item)
        else:
            return item in self._types2evs

    # Basic fact queries

    def facts(self):
        """
        Return the facts of this sequence as a set of (key, value) pairs.
        """
        return self._facts.items()

    def fact_keys(self):
        """Return the keys of the facts of this sequence."""
        return self._facts.keys()

    def has_fact(self, key):
        """Whether this sequence has a fact with the given key."""
        return key in self._facts

    def fact(self, key, default=None):
        """
        Return the value of the fact with the given key or `default`.

        default:
            Value to return when this sequence does not have a fact with
            the given key.
        """
        return self._facts.get(key, default)

    # Basic event queries

    def events(self, *types):
        """
        Yield events of the specified types (or all events).

        types:
            Types of events to yield.  When not specified, yield events
            of all types.
        """
        if not types:
            yield from self._events
        else:
            for event_index in heapq.merge(
                    *(self._types2evs.get(t, ()) for t in types)):
                yield self._events[event_index]

    def types(self):
        """Return the event types in this sequence."""
        return self._types2evs.keys()

    def has_type(self, type):
        """Whether this sequence contains an event with the given type."""
        return type in self._types2evs

    def has_types(self, *types): # ENH return proof, perhaps as separate method 'occur'?
        """
        Whether this sequence contains an event with each of the given event
        types.
        """
        for type in types:
            if type not in self._types2evs:
                return False
        return True

    def n_events_of_type(self, type):
        """Return the number of events in this sequence of the given type."""
        return len(self._types2evs.get(type, ()))

    def has_when(self, when): # TODO return proof?
        """Whether this sequence contains an event with the given when."""
        found, _ = sose.binary_search(
            self._whens, when, target=sose.Target.any)
        return found

    def has_event(self, event): # TODO return proof?
        """Whether this sequence contains the given `esal.Event`."""
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

    # TODO span?

    # Advanced queries

    def first(self, type=None, after=None, strict=True):
        if type is None and after is None:
            return (True, (0, self._events[0]))
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

    def last(self, type=None, before=None, strict=True): # TODO
        return (False, None)

    def events_after(self, when_lo=None, strict=True): # TODO
        return ()

    def events_before(self, when_hi=None, strict=True): # TODO
        return ()

    def events_between(self, when_lo=None, when_hi=None, strict=True):
        """
        Return a tuple containing the events in the given interval.

        when_lo:
            Lower bound or unlimited if `None`.
        when_hi:
            Upper bound or unlimited if `None`.
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

    def events_overlapping(self, when_lo=None, when_hi=None, strict=True): # TODO
        return ()

    def transitions(self, *types):
        """
        Yield transitions of the specified types of events (or all
        transitions).

        A transition occurs when an interval event starts or stops or
        when a point event occurs.  All the transitions that occur at
        the same time are yielded at once as a tuple (when, starts,
        stops, points).  Grouping by time allows one to decide what
        happens first according to application needs.  The following
        diagrams illustrate some possibilities.

                     (a) <, >=     (b) <, =, >      (c) <=, =, >=
            stop     <---)         <---)            <---]
            point         [--->         (*)           [*]
            start         [--->            (--->      [--->

        In (a), intervals abut and points are considered to start but
        not stop.  There is one transition.  In (b), all intervals and
        points are exclusive (open).  There are two transitions.  In
        (c), points last the entire duration of "when" and intervals are
        inclusive (closed).  There are two transitions.

        types:
            Types of events of transitions to yield.  When not
            specified, yields events of all types.
        """
        def gen_txs(event_idxs):
            for idx in event_idxs:
                ev = self._events[idx]
                # Generate start and end transitions.  Point events
                # generate only a start impulse.
                if isinstance(ev.when, interval.Interval):
                    # Point interval
                    if ev.when.lo == ev.when.hi:
                        yield (ev.when.lo, 1, ev)
                    # Interval with positive length
                    else:
                        yield (ev.when.lo, 1, ev)
                        yield (ev.when.hi, 0, ev)
                else:
                    # Point event
                    yield (ev.when, 1, ev)
        def txs_sort_key(t):
            return (t[0], -t[1])
        def txs_grp_key(t):
            return t[0]
        if not types:
            types = sorted(self._types2evs.keys())
        # Generate the transitions for the events of each type
        txs = []
        for typ in types:
            txs.append(sorted(gen_txs(self._types2evs.get(typ, ())),
                              key=txs_sort_key))
        for when, txs_evs in itools.groupby(
                heapq.merge(*txs, key=txs_sort_key), key=txs_grp_key):
            points = []
            starts = []
            stops = []
            for _, tx, ev in txs_evs:
                if (not isinstance(ev.when, interval.Interval) or
                        ev.when.lo == ev.when.hi):
                    points.append(ev)
                elif tx == 0:
                    stops.append(ev)
                else:
                    starts.append(ev)
            yield (when, starts, stops, points)

    def before(self, type1, type2, *types, strict=True): # TODO rename: has_subsequence? # TODO return proof?
        """
        Whether this sequence contains events of the given types in the
        given order.
        """
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

    # Modification by derivation

    def copy(self, events=None, facts=None, id=None):
        """
        Copy this event sequence, replacing existing fields with the given
        values (if any).
        """
        return EventSequence(
            events=events if events is not None else self.events(),
            facts=facts if facts is not None else self.facts(),
            id=id if id is not None else self.id,
        )

    def subsequence(self, when_lo=None, when_hi=None): # TODO take indices?
        """
        Return a copy of this event sequence that contains only the events
        in the given interval (inclusive).

        when_lo:
            Lower bound or unlimited if `None`.
        when_hi:
            Upper bound or unlimited if `None`.
        """
        return self.copy(
            events=self.events_between(when_lo, when_hi))

    def aggregate_events(self, aggregator, types=None):
        """
        Apply the given aggregator separately to the events of each given
        type.  Return a new event sequence containing the aggregated
        events plus all the untouched, pre-existing information.

        aggregator: Function that takes a list, the current aggregation,
            and the current event, and that returns a list, the updated
            aggregation.
        types: Types of events to separately aggregate.  (Events of
            other types are left alone.)
        """
        if types is None:
            types = self._types2evs.keys()
        events = []
        for type in types:
            aggregated = []
            for ev_idx in self._types2evs.get(type, ()):
                aggregated = aggregator(
                    aggregated, self._events[ev_idx])
            events.extend(aggregated)
        for type in self._types2evs.keys() - types:
            events.extend(self._events[i] for i in self._types2evs[type])
        return self.copy(events=events)


def mk_union_aggregator(min_len=0, max_gap=0):
    """
    Make and return a function that aggregates events by unioning their
    intervals.

    Accumulates the values of aggregated events into a list.  Uses the
    event type of the first event in a group of aggregated events.

    min_len: Minimum length of an interval.  Useful for giving length to
        point events.
    max_gap: Maximum length between intervals to be unioned.
    """
    def ensure_length(event, length):
        when = event.when
        if isinstance(when, interval.Interval):
            if when.length() < length:
                when = interval.Interval(when.lo, length=length)
        else:
            when = interval.Interval(when, length=length)
        return Event(when, event.type, [event.value])
    def union_aggregator(events, event):
        this_event = ensure_length(event, min_len)
        if len(events) == 0:
            events.append(this_event)
            return events
        last_event = events[-1]
        if this_event.when.lo - last_event.when.hi <= max_gap:
            last_event.value.append(this_event.value[0])
            when = interval.Interval(
                last_event.when.lo, this_event.when.hi)
            events[-1] = Event(when, last_event.type, last_event.value)
        else:
            events.append(this_event)
        return events
    return union_aggregator
