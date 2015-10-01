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

See story 007 for how events are records and basic record design.

For implementing Allen's interval algebra, times need to be comparable
and they need to support addition with durations.  There needs to be
some way of elegantly supporting the many data types applications can
use to express times.  Here are some ideas.

* Functions to convert times and durations to computable versions
  * Pros
    * No need to change data
  * Cons
    * Computational overhead or storage overhead for caching

* Let user ensure times and durations are computable
  * Pros
    * Flexible
  * Cons
    * Operations are not guaranteed to work

* Limit types of times and durations to computable ones
  * Pros
    * Operations guaranteed to work
  * Cons
    * Inflexible: some applications may not need computable values

* Leave time computations to the application
  * Pros
    * Nothing to implement
  * Cons
    * Applications must always implement their own time computations

* Define separate algebra object(s) that know how to compute with
  various types of event times.  For example, you could implement the
  interval algebra in terms of date strings like '2015-09-29'.
  * Pros
    * Separates time computation responsibility from events
    * Allows "centralized" support and implementation of time
      computations with events on an as-needed basis.  Think of
      assigning an algebra at the class level.  But then why not just
      define "smart" conversion functions at the class level.
  * Cons
    * Many algebras would need to be implemented, especially if
      supporting computations with mixed types.  Could convert to a
      unifying representation, but what?  Think Julia.

* Define time computation only within an Event subclass and check for
  computable types during construction
  * Pros
    * Separates data storage and computation responsibilities
  * Cons
    * More subclasses?!  Favor composition over inheritance.

For now I think the best option is to leave time computations to the
application.  This option poses the smallest barrier and will lead to
examples of what the needed time computations and appropriate computable
types are.


-----
Copyright (c) 2015 Aubrey Barnard.  This is free software.  See LICENSE
for details.
