Event Sequence Analysis Library
===============================


Esal ("easel") is a library for the descriptive statistical analysis and
manipulation of event sequences and timelines.  Esal is intended to be
used for exploring event sequence data and preparing data for modeling,
but does not do any modeling itself.  Conceptually, Esal is a
representation for a dataset of sequences / timelines and an associated
set of meaningful operations (selection, counting, transformation).


Features
--------

This project is in the early design and implementation stages.  The
planned features are:

* Selection and counting of sequences
* Selection and counting of events
* Sampling events and sequences
* Temporal statistics
* Reading/Writing various relational and flat representations


Requirements
------------

* Python 3


License
-------

Esal is free, open source software.  It is released under the MIT
license.  See the `LICENSE` file for details.


Concepts
--------

An event describes something that happens, either at a point in time or
over an interval of time.  It has a symbol indicating the type of event,
a time indicating the start of the event, a time indicating the end of
the event (if an interval event), a value, and a sequence identifier.
The sequence identifier indicates what sequence of events (or timeline)
the event belongs to.  An event type normally corresponds to a
particular variable or measurement of interest, such as rain.  (When did
it start raining?  How long did it rain?  How much rain fell?)

An event sequence is an ordered collection of events that all have the
same sequence identifier.  An event sequence normally describes the
timeline of a particular entity of interest, such as a person.  Events
can happen at arbitrary times or be sampled with some pattern so
sequences may be regular, or irregular, or something in between.

A timeline is a type of event sequence where all of the events have
"interpretable" times, that is, times that are analogous to the real
numbers.  Integer times are fine as long as their differences are
meaningful.  Thus a timeline is distinguished from sequences that have
non-meaningful times, such as time steps or other sequential numbering;
such sequences have only ordering and not difference.

To avoid ambiguity, "sequence" will refer solely to an event sequence.
Data structures will be referred to as iterables or collections or with
specific names as appropriate.  A stream is just another name for
iterable.


Contact
-------

* [Aubrey Barnard](https://github.com/afbarnard)

[Open an issue](https://github.com/afbarnard/esal/issues/new) to report
a bug or ask a question.  To contribute, use the regular fork and pull
request work flow.


-----

Copyright (c) 2018 Aubrey Barnard.  This is free software.  See LICENSE
for details.
