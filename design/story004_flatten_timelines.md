Story 4: Flatten multivariate timelines into sequences
======================================================


Convert multivariate timelines with events occurring at the same time
(as in dynamic Bayesian networks or other multivariate temporal models
that proceed in steps) into flat sequences by ordering concurrent events
so that all the events in the timeline have a total order.  In other
words, break up groups of events that occur at the same time so that the
sequence has a flat (rather than nested) structure.  Optionally replace
times with the time step numbers of the new total order to fully convert
the timeline into a sequence.

* Examples of ordering concurrent events:
  * Data order (no change)
  * Nth (or slice) in data order
  * Random reorder
  * Sample n
  * Sample n in order


Design
------

Here a sequence means some iterable of events with the same sequence ID
and sorted by time.

* Function for ordering concurrent events within a sequence.

* Function for replacing times with sequence numbers within a sequence.

* Function for mapping a function across sequences given an event stream
  sorted by sequence ID.

* Ordering of concurrent events will be controlled by a parameter, a
  function that takes an iterable of concurrent events and returns an
  iterable of events.  These events then become part of the flattened
  sequence, in order.


-----
Copyright (c) 2015 Aubrey Barnard.  This is free software.  See LICENSE
for details.
