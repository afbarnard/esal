Event Sequence Analysis Library
===============================


Esal ("easel") is a library for the statistical analysis and
manipulation of event sequences.  Esal is intended to be used for
exploring event sequence data and preparing data for modeling, but does
not do any modeling itself.  Conceptually, Esal is a representation for
a dataset of sequences and an associated set of meaningful operations
(selection, counting, transformation).


Concepts
--------

An event describes something that happens.  It has a symbol indicating
the type of event, a time stamp indicating the start of the event, a
duration, a value, and a sequence identifier.  The sequence identifier
indicates what sequence of events (time line) the event belongs to.  An
event type normally corresponds to a particular variable or measurement
of interest, such as rain.  (When did it start raining?  How long did it
rain?  How much rain fell?)

An event sequence is an ordered collection of events that all have the
same sequence identifier.  An event sequence normally the describes the
time line of a particular entity of interest, such as a person.  Events
can happen at arbitrary times or be sampled with some pattern so
sequences may be regular, or irregular, or something in between.

To avoid ambiguity, "sequence" will refer solely to an event sequence.
Data structures will be referred to as iterables or collections or with
specific names as appropriate.  A stream is just another name for
iterable.


License
-------

Esal is free, open source software.  It is released under the MIT
license.  See the `LICENSE` file for details.


Features
--------

* Selection and counting of sequences
* Selection and counting of events
* Sampling events and sequences
* Temporal statistics
* Reading/Writing various relational and flat representations


Requirements
------------

* Python 3


-----

Copyright (c) 2015 Aubrey Barnard.  This is free software.  See LICENSE
for details.
