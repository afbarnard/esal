Story 5: Event Queries and Allen's Interval Algebra
===================================================


Here are queries to be asked of events.  Abstractly, an event is an
interval and may be labeled with an event type and/or a value.  The
interval may be empty, in which case it is a point event.  Events may
represent discrete or continuous time.  Events may belong to a
particular sequence or timeline.

* When does it start?
* When does it stop?
* What is its duration?
* What is its event type?
* What is its value?


Allen's Interval Algebra
------------------------

Here are the queries for the possible temporal relations between event X
and event Y.

* Is X before Y?
* Does X meet Y?  (Does the end of X equal the start of Y?)
* Does X overlap Y?
* Does X start Y?
* Is X during Y?
* Does X finish Y?
* Does X equal Y?


Design
------

TODO Extend existing NamedTuple or make a new class?


-----
Copyright (c) 2015 Aubrey Barnard.  This is free software.  See LICENSE
for details.
