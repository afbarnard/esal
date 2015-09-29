Story 7: Events as Record Objects
=================================


Records
-------

A record is a fixed-size, possibly read-only, ordered collection of
heterogeneous fields where the fields are accessible by name, index, and
as attributes.  A record also has a header which describes the names,
types, and order of the fields.  Thus a record is like a hybrid of a
struct, a tuple, and a dict.  A record can be thought of as a row in a
table and a table can be thought of as a collection of records that have
the same header.

Features:

* Fixed-size, ordered collection of fields with heterogeneous types
  * Support typical collection operations (as in collections.abc):
    * Iterable
    * Container
    * Sequence
    * Hashable
    * Comparable for equality
  * Would be nice to support typical dictionary operations:
    * Iterable as keys, values, items
* Access to fields by
  * Index (constant time), for collection-like behavior
  * Name (constant time).  This is important for supporting arbitrary
    database-like queries and other operations that can work by only
    specifying field names.
  * Attribute (constant time), for object-like behavior
* Any value can be None ("nullable" is the database sense)
* Constructable from (partial) iterable of name-value pairs (other
  values default to None)
* Read-only
* Hashable
* Lightweight
* Ability to attach methods to make a particular type of record more
  functional as an object (e.g. Allen's interval algebra for events)
* Extras
  * To/From dict
  * New record as modification of existing record
  * Slicing, perhaps implemented as a view


Events as Records
-----------------

An event is just a record with the necessary fields: sequence ID, time,
duration, event, value.


Design
------

* Record need only have a reference to the header (perhaps as part of
  the class definition) and all dictionary-style access can be supported
  via the header.  There is no need for each record to have its own name
  dictionary.  This means each object needs to have an extra field, the
  reference to the header, or the object must be of a class and the
  class contains the header information.

* Event needs to be a class of some kind in order to easily and cleanly
  support additional methods.  Here are the options:

  * namedtuple
    * Pros
      * Read-only collection support already exists, including hashing,
        equality
    * Cons
      * No dictionary support
      * Supporting additional methods, class attributes, documentation,
        etc. ungainly but works (see existing implementation)
      * All functionality that doesn't already exist in namedtuple would
        have to re-implemented for each type of record
      * Not possible to customize __init__ (must override __new__)

  * Subclass of namedtuple
    * Pros
      * Read-only collection support already exists, including hashing,
        equality
      * Methods, class attributes, documentation defined as part of
        regular class definition
      * Header can easily be part of class definition
    * Cons
      * Each type of record has to be re-implemented
      * Not possible to customize __init__ (must override __new__) (?)

  * Plain class with fields
    * Pros
      * Flexible, direct implementation
    * Cons
      * Must implement everything oneself
      * Read-only unenforceable

  * Plain class wrapping a tuple
    * Pros
      * Can just forward to tuple methods
    * Cons
      * Must forward methods
        * Performance
        * Still have to implement everything
      * Must define properties for attribute access

  * Subclass of OrderedDict
    * Pros
      * Supports everything out of the box
    * Cons
      * Not read-only, would have to override methods to enforce
      * Memory: each object would have a dictionary and a list

  * Generated class a la namedtuple
    * Pros
      * Write once, support all kinds of records as needed
    * Cons
      * Still have issue of extending a particular type of record, but
        could subclass generated class

  * Metaclasses?

Based on the above analysis, it seems wisest to start with implementing
Event as a subclass of a (custom) namedtuple.  For supporting many
different kinds of records, the best option seems to be creating a class
generator similar to namedtuple, but with all the desired functionality
(mainly this would be adding dictionary-like functionality to what
already exists in namedtuple).  Further, implementing Event as a
subclass of namedtuple will show whether subclassing a generated class
is a reasonable way of customizing records.
