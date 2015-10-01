Story 6: Queries on Event Sequences
===================================


Here are queries to be asked of event sequences.  An event sequence is
an ordered collection of events.  (For conceptual details of events, see
story 005.)  A timeline is a type of event sequence where the times
(either discrete or continuous) have meaningful differences.

* When does it start?
* When does it stop?
* What is its duration?
* How many events does it contain?
* What types of events does it contain?
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

How much functionality to build in versus treating as data storage and
processing externally?

* Event sequence object
  * Fields: sequence ID, start, duration, list of events
  * List of events sorted by start time then by duration
  * Methods for above queries

* Methods
  * __len__: return number of events
  * __getitem__: access events by index, in sorted order
  * types: return event types as a flat sequence given an ordering
    function.  Optional filter for selecting certain event types?
    (Rename 'ev' -> 'type' in Event to support this method.)
  * times: return times as a flat sequence, no need to reorder as they
    will be sorted
  * index: forward to underlying list
  * __contains__: return True if sequence exactly contains a given Event
    object, or return True if given a (name::str, object) pair and the
    sequence contains an event whose named field equals the given object
  * match: return the index of the first event that matches the given
    Event field values, or None.  Optional start index.  Need special
    value 'Any' as default for field values so None can be matched.
  * matches: return an iterable of all the matches that would be
    returned from successive calls to 'match'.  Empty iterable means no
    matches.

* Other filtering can be covered by using collection features.


-----
Copyright (c) 2015 Aubrey Barnard.  This is free software.  See LICENSE
for details.
