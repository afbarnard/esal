Event Sequence Analysis Library
===============================


Esal ("easel") is a library for representing and querying event
sequences and timelines.


Features
--------

This project is in the early design and implementation stages.  The
implemented features are:

* Event objects
* Event sequence data structure for the efficient querying of event
  sequences
* Interval objects
* Allen's interval algebra (constant-time implementation that uses only
  a few comparisons)

Other features have already been implemented but haven't yet been
organized into an official API.  Feel free to look through the code.
Suggestions are welcome.


Requirements
------------

* Python 3


Install
-------

    pip3 install [--user] https://github.com/afbarnard/esal/archive/<name>.zip#egg=esal

Replace `<name>` with the name of the tag, branch, or commit you want to
install, e.g. "master" or "v0.2.0".  If you don't have a `pip3`, replace
it with `python3 -m pip`.  For more information, see the [Pip
documentation]( https://pip.pypa.io/).


Test
----

    python3 -m unittest esal/test/*.py


License
-------

Esal is free, open source software.  It is released under the MIT
License.  See the `LICENSE` file for details.


Concepts
--------

See the [package documentation](
https://github.com/afbarnard/esal/blob/master/esal/__init__.py) for a
conceptual overview of events and sequences.


Contact
-------

* [Aubrey Barnard](https://github.com/afbarnard)

[Open an issue](https://github.com/afbarnard/esal/issues/new) to report
a bug or ask a question.  To contribute, use the regular fork and pull
request work flow.


-----

Copyright (c) 2015, 2018-2019 Aubrey Barnard.

This is free software released under the MIT License.  See `LICENSE` for
details.
