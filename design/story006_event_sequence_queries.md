Story 6: Queries on Event Sequences
===================================


Here are queries to be asked of event sequences.  An event sequence is
an ordered collection of events.  (For conceptual details of events, see
story 5.)  A timeline is a type of event sequence where the times
(either discrete or continuous) have meaningful differences.

* When does it start?
* When does it stop?
* What is its duration?
* How many events does it contain?
* What events does it contain?
* What times does it contain?
* Does it contain a particular event/time?
* Does it contain an event at a particular time (in an interval)?
* Does it contain any event at a particular time (in an interval)?
* What are the events in an interval?
* What are the events in temporal order?
* What are the occurrences of a particular event?


Additional Requirements and Considerations
------------------------------------------

* Start and end of sequence can be independent of the events so long as
  the events are within the interval [start, end].  Consider handling
  special "sequence definition" event whose start and duration are that
  of the entire sequence.  Otherwise the start and duration are just the
  minimal bounds of the individual events.

* Must support multiple equal events, like multiple doses of the same
  medication on the same day when times have day granularity.


Design
------

* Event sequence object
  * Fields: sequence ID, start, duration, list of events
  * List of events sorted by start time then by duration
  * Methods for above queries

* --Allow to build indices if desired.  Times to events.  Events to
  times.  Queries will use indices if available.  Indices are binary
  association tables sorted by key.  Keys may occur mutliple times,
  e.g. one table entry for each event-time pair.  Use binary search to
  find entire slice for a key.-- Indices likely overkill for lengths of
  anticipated sequences.


-----
Copyright (c) 2015 Aubrey Barnard.  This is free software.  See LICENSE
for details.
