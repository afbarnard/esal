"""
Event Sequence Analysis Library: statistical analysis and
manipulation of event sequence data

Esal ("easel") is a library for the descriptive statistical analysis and
manipulation of event sequences and timelines.  Esal is intended to be
used for exploring event sequence data and preparing data for modeling,
but does not do any modeling itself.  Conceptually, Esal is a
representation for a dataset of sequences / timelines and an associated
set of meaningful operations (selection, counting, transformation).


Concepts
--------

An event describes something that happens, either at a point in time or
over some span of time.  It can be thought of as a 4-tuple

    (sequence-id, when, event-type, value)

where the order of the fields makes the tuples sortable.  The object
that represents *when* an event occurs can be any orderable, which
allows for flexibility in handling anything from point events in
continuous (`float`) or discrete (`int`) time, to intervals of such
times, to dates, to strings (e.g. `'2018-08-06'`).  The value is
optional and when it is omitted, the event is an occurrence event (an
event whose value is effectively `occur = True`).  The sequence
identifier indicates what sequence of events (or timeline) the event
belongs to.  An event normally corresponds to a particular variable,
measurement, or observation of interest, such as rain.  (When did it
start raining?  How long did it rain?  How much rain fell?)

An event sequence is an ordered collection of events that all have the
same sequence identifier.  An event sequence normally describes the
timeline of a particular entity of interest, such as a person.  Events
can be sampled with some pattern or happen over arbitrary intervals, so
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

Copyright (c) 2018 Aubrey Barnard.  This is free, open source software,
released under the MIT license.  See `LICENSE` for details.
"""
# The above text is used by `setup.py`.


# Version
__version__ = '0.2.1'


# Expose core API at the top level
from .event import *
from .interval import *

__all__ = (
    *event.__all__,
    *interval.__all__,
)
