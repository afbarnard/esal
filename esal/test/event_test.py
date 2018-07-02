# Tests `event.py`

# Copyright (c) 2018 Aubrey Barnard.  This is free software.  See
# LICENSE for details.


import operator
import string
import unittest

from ..event import Event, EventSequence


class EventSequenceTest(unittest.TestCase):

    #  0: e, l
    #  2: z
    #  3: s, t, y
    #  4: k
    #  5: v, w, y
    #  6: l
    #  9: e, h
    # 10: d
    # 11: k
    # 12: b
    # 13: f
    # 14: l
    # 16: q
    # 18: q
    evs = (
        Event('y', 3), Event('e', 0), Event('z', 2), Event('t', 3),
        Event('y', 5), Event('w', 5), Event('l', 14), Event('h', 9),
        Event('k', 4), Event('e', 9), Event('v', 5), Event('s', 3),
        Event('l', 6), Event('f', 13), Event('q', 18), Event('k', 11),
        Event('b', 12), Event('l', 0), Event('d', 10), Event('q', 16),
    )

    def setUp(self):
        self.evs = EventSequenceTest.evs
        self.es = EventSequence(0, self.evs)

    def test_has_type(self):
        types = set(e.type for e in self.evs)
        for t in string.ascii_lowercase:
            self.assertEqual(t in types, self.es.has_type(t), t)

    def test_has_when(self):
        whens = set(e.when for e in self.evs)
        for w in range(20):
            self.assertEqual(w in whens, self.es.has_when(w), w)

    def test_has_event(self):
        events = set(self.evs)
        for t in string.ascii_lowercase:
            for w in range(20):
                e = Event(t, w)
                self.assertEqual(e in events, self.es.has_event(e), e)

    def test___contains__(self):
        types = set(e.type for e in self.evs)
        whens = set(e.when for e in self.evs)
        events = set(self.evs)
        for t in string.ascii_lowercase:
            for w in range(20):
                e = Event(t, w)
                self.assertEqual(t in types, t in self.es, t)
                self.assertEqual(w in whens, w in self.es, w)
                self.assertEqual(e in events, e in self.es, e)

    def test_events(self):
        self.evs = sorted(self.evs, key=lambda e: (e.when, e.type))
        self.assertSequenceEqual(self.evs, tuple(self.es.events()))

    def test_n_events_of_type(self):
        for t in string.ascii_lowercase:
            count = sum(1 for e in self.evs if e.type == t)
            self.assertEqual(count, self.es.n_events_of_type(t), t)

    def test_events_of_type(self):
        for t in string.ascii_lowercase:
            events = [e for e in self.evs if e.type == t]
            self.assertCountEqual(events, self.es.events_of_type(t), t)

    def test_has_types(self):
        all_types = set(string.ascii_lowercase)
        has_types = set(e.type for e in self.evs)
        hasnt_types = all_types - has_types
        self.assertTrue(self.es.has_types(*has_types), has_types)
        self.assertFalse(self.es.has_types(*has_types, *hasnt_types),
                         hasnt_types)

    def test_first(self):
        evs_by_when = [(e.when, e) for e in self.evs]
        evs_in_order = sorted(
            evs_by_when, key=lambda x: (x[0], x[1].type))
        for t in string.ascii_lowercase:
            ts = [x for x in evs_in_order if x[1].type == t]
            if ts:
                first = ts[0]
                first_idx = evs_in_order.index(first)
                expected = (True, (first_idx, first[1]))
            else:
                expected = (False, None)
            self.assertEqual(expected, self.es.first(t), t)

    def test_first_after(self):
        evs_by_when = [(e.when, e) for e in self.evs]
        evs_in_order = sorted(
            evs_by_when, key=lambda x: (x[0], x[1].type))
        for t in string.ascii_lowercase:
            ts = [x for x in evs_in_order if x[1].type == t]
            for w in range(20):
                for strict, lte in ((False, operator.le),
                                    (True, operator.lt)):
                    ts_after = [x for x in ts if lte(w, x[0])]
                    if ts_after:
                        first = ts_after[0]
                        first_idx = evs_in_order.index(first)
                        expected = (True, (first_idx, first[1]))
                    else:
                        expected = (False, None)
                    self.assertEqual(
                        expected,
                        self.es.first(t, after=w, strict=strict),
                        (t, w, strict))

    def test_before_pairs(self):
        for t1 in string.ascii_lowercase:
            t1s = [e.when for e in self.evs if e.type == t1]
            first_t1 = min(t1s) if t1s else None
            for t2 in string.ascii_lowercase:
                t2s = [e.when for e in self.evs if e.type == t2]
                last_t2 = max(t2s) if t2s else None
                # Strict less than
                lte = first_t1 < last_t2 if t1s and t2s else False
                self.assertEqual(lte, self.es.before(t1, t2), (t1, t2))
                # Less than or equal
                lte = first_t1 <= last_t2 if t1s and t2s else False
                self.assertEqual(
                    lte, self.es.before(t1, t2, strict=False), (t1, t2))

    def test_before_ascending(self):
        seqs = (
            # Contiguous
            (('y', 'k', 'y'), True),
            (('l', 'q', 'q'), True), # At end
            (('l', 'e', 't'), False), # Strict!
            (('a', 'b', 'c'), False),
            # Repetitions
            (('e', 'e', 'q', 'q'), True),
            # BDFL? No, DB for life!
            (('b', 'd', 'f', 'l'), False),
            (('d', 'b', 'f', 'l'), True),
            # Sledding on Skye with Kyle?
            (('s', 'l', 'e', 'd'), True),
            (('s', 'k', 'y', 'e', 'l'), True),
            (('s', 'k', 'y', 'l', 'e'), True),
            # Hinges on the end
            (('z', 'v', 'h', 'k', 'f', 'q'), True),
            (('z', 'v', 'h', 'k', 'f', 'b'), False), # Wrong order
            (('z', 'v', 'h', 'k', 'f', 'q', 'a'), False), # No a
        )
        for seq, exists in seqs:
            self.assertEqual(exists, self.es.before(*seq), seq)

    def test_before_monotonic(self):
        seqs = (
            # Words
            (('t', 'h', 'e'), True),
            (('l', 'e', 't'), True),
            (('s', 'h', 'e', 'd'), True),
            (('s', 't', 'y', 'l', 'e', 'd'), True),
            # In one timestep
            (('y', 'w', 'v'), True),
            # Longer
            (('l', 'e', 's', 't', 'w', 'y', 'l', 'e'), True),
            (('l', 'e', 's', 't', 'w', 'y', 'l', 'e', 's'), False),
            # All together now, hinges on end
            (('l', 'e', 'y', 't', 's', 'h', 'e', 'q'), True),
            (('l', 'e', 'y', 't', 's', 'h', 'e', 'a'), False), # No a
        )
        for seq, exists in seqs:
            self.assertEqual(
                exists, self.es.before(*seq, strict=False), seq)
