"""
Event Sequence Analysis Library: statistical analysis and
manipulation of event sequence data

Esal ("easel") is a library for the descriptive statistical analysis and
manipulation of event sequences and timelines.  Esal is intended to be
used for exploring event sequence data and preparing data for modeling,
but does not do any modeling itself.  Conceptually, Esal is a
representation for a dataset of sequences/timelines and an associated
set of meaningful operations (selection, counting, transformation).

The core concept is an event, which can be though of as a 5-tuple
(sequence-id, start-time, stop-time, event-type, value).  The stop time
and value are optional.

Copyright (c) 2018 Aubrey Barnard.  This is free software.  See LICENSE
for details.
"""
# The above text is used by `setup.py`.


# Version
__version__ = '0.1.0'


# Expose core API at the top level
from .events import *
