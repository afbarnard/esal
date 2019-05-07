"""
Event Sequence Analysis Library: representing and querying event
sequences / timelines.


Concepts
--------

An event describes something that happens, either at a point in time or
over some span of time.  While a raw event record in your data might
have several fields such as

    (sequence-id, from-when, to-when, what-1, what-2, value-1, value-2),

an event in the abstract is the 3-tuple

    (when, event-type, value).

where the order of the fields makes both types of tuples sortable by
time.  An event object represents just such a 3-tuple.  For example, the
above event record might be represented as the event object with
compound fields

    esal.Event(esal.Interval(from, to), (what1, what2), (val1, val2)).

An event object omits the sequence ID because that is a property of a
collection of events (an event sequence or timeline), and it would be
redundant for events to repeatedly store it.

Event objects are intended to be flexible yet useful.  The object that
represents *when* an event occurs can be any orderable, which allows for
flexibility in handling anything from point events in continuous
(`float`) or discrete (`int`) time, to intervals of such times, to
dates, to strings (e.g. `'2018-08-06'`).  The value is optional and when
it is omitted, the event is an occurrence event (an event whose value is
conceptually `occur = True`).  An event normally corresponds to a
particular variable, measurement, or observation of interest, such as
rain.  (When did it start raining?  How long did it rain?  How much rain
fell?)

An event sequence is an ordered collection of events that all have the
same sequence identifier.  An event sequence normally describes the
timeline of a particular entity of interest, such as a person or place
(e.g. the weather observations from a particular station).  Events can
be sampled with some pattern or happen over arbitrary intervals, so
sequences may be regular, or irregular, or something in between.

A timeline is a type of event sequence where all of the events have
"interpretable" times.  That is, the times are analogous to the real
numbers in that the differences between when they occur are meaningful.
Thus, "timelines" are distinguished from "sequences" by having
meaningful times; sequences have only meaningful ordering, such as time
steps or incremental numbering.

To avoid ambiguity, "sequence" will refer solely to an event sequence.
Data structures will be referred to as iterables or collections or with
specific names as appropriate.  A stream is just another name for
iterable.


-----

Copyright (c) 2018-2019 Aubrey Barnard.  This is free, open source
software, released under the MIT license.  See `LICENSE` for details.
"""
# The above text is used by `setup.py`.


# Version
__version__ = '0.4.0'


# Expose core API at the top level
from .event import *
from .interval import *

__all__ = (
    *event.__all__,
    *interval.__all__,
)
