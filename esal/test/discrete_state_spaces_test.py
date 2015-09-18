# Tests discrete state spaces
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import unittest

from .. import discrete_state_spaces as dss


class PermutationSpaceTest(unittest.TestCase):

    elts_to_space = {
        ('', 0): ('',),
        ('a', 1): ('a',),
        ('ab', 1): ('a', 'b'),
        ('ab', 2): ('ab', 'ba'),
        ('abc', 1): ('a', 'b', 'c'),
        ('abc', 2): ('ab', 'ac', 'ba', 'bc', 'ca', 'cb'),
        ('abc', 3): ('abc', 'acb', 'bac', 'bca', 'cab', 'cba'),
        ('abcd', 3): (
            'abc', 'abd', 'acb', 'acd', 'adb', 'adc',
            'bac', 'bad', 'bca', 'bcd', 'bda', 'bdc',
            'cab', 'cad', 'cba', 'cbd', 'cda', 'cdb',
            'dab', 'dac', 'dba', 'dbc', 'dca', 'dcb',
            ),
        ('abcdef', 2): (
            'ab', 'ac', 'ad', 'ae', 'af',
            'ba', 'bc', 'bd', 'be', 'bf',
            'ca', 'cb', 'cd', 'ce', 'cf',
            'da', 'db', 'dc', 'de', 'df',
            'ea', 'eb', 'ec', 'ed', 'ef',
            'fa', 'fb', 'fc', 'fd', 'fe',
            ),
        }

    def test_init_length_out_of_bounds(self):
        with self.assertRaises(dss.StateSpaceError):
            dss.PermutationSpace(iter('elmnts'), 10)
        with self.assertRaises(dss.StateSpaceError):
            dss.PermutationSpace(iter('elmnts'), -1)

    def test_init_repeated_elements(self):
        with self.assertRaises(dss.StateSpaceError):
            dss.PermutationSpace(iter('elements'), 4)

    def test_init_default_length(self):
        space1 = dss.PermutationSpace(iter('elmnts'), 6)
        space2 = dss.PermutationSpace(iter('elmnts'))
        self.assertEqual(space1.elements, space2.elements)
        self.assertEqual(space1.length, space2.length)
        self.assertEqual(space1.bases, space2.bases)

    def test_empty_elements(self):
        space = dss.PermutationSpace(iter(()), 0)
        self.assertEqual(1, len(space))
        self.assertIn(0, space)
        self.assertIn(iter(()), space)
        self.assertNotIn(1, space)
        self.assertEqual([], space.state_of(0))
        self.assertEqual(0, space.index_of(iter(())))

    def test_zero_length(self):
        space = dss.PermutationSpace(iter('elmnts'), 0)
        self.assertEqual(1, len(space))
        self.assertIn(0, space)
        self.assertIn(iter(()), space)
        self.assertNotIn(1, space)
        self.assertEqual([], space.state_of(0))
        self.assertEqual(0, space.index_of(iter(())))

    # TODO add subTests with Python 3.4

    def test_size(self):
        for params, perms in self.elts_to_space.items():
            space = dss.PermutationSpace(*params)
            self.assertEqual(len(perms), len(space))

    def test_contains(self):
        for params, perms in self.elts_to_space.items():
            space = dss.PermutationSpace(*params)
            for idx, perm in enumerate(perms):
                self.assertIn(idx, space)
                self.assertIn(perm, space)
                self.assertIn(iter(perm), space)
        # Return false types other than integers and permutations
        space = dss.PermutationSpace('elmnts', 3)
        self.assertNotIn(3.0, space)
        self.assertNotIn('bad', space)

    def test_state_of(self):
        for params, perms in self.elts_to_space.items():
            space = dss.PermutationSpace(*params)
            for idx, perm in enumerate(perms):
                self.assertEqual(list(perm), space[idx])
        # Test exceptions
        space = dss.PermutationSpace('elmnts', 5)
        with self.assertRaises(NotImplementedError):
            space[:]
        with self.assertRaises(TypeError):
            space['elm']
        with self.assertRaises(IndexError):
            space[space.size()]

    def test_index_of(self):
        for params, perms in self.elts_to_space.items():
            space = dss.PermutationSpace(*params)
            for idx, perm in enumerate(perms):
                self.assertEqual(idx, space.index_of(iter(perm)))
        # Test exceptions
        space = dss.PermutationSpace('elmnts', 4)
        with self.assertRaises(dss.StateSpaceError):
            space.index_of('elm')
        with self.assertRaises(dss.StateSpaceError):
            space.index_of('elem')
        with self.assertRaises(dss.StateSpaceError):
            space.index_of('elmo')

    def test_space_size(self):
        # Empty
        self.assertEqual(1, dss.PermutationSpace.space_size(0, 0))
        self.assertEqual(1, dss.PermutationSpace.space_size(10, 0))
        # Full
        self.assertEqual(6, dss.PermutationSpace.space_size(3, 3))
        self.assertEqual(120, dss.PermutationSpace.space_size(5, 5))
        # Partial
        self.assertEqual(10, dss.PermutationSpace.space_size(10, 1))
        self.assertEqual(20, dss.PermutationSpace.space_size(5, 2))
        self.assertEqual(60, dss.PermutationSpace.space_size(5, 3))
        self.assertEqual(120, dss.PermutationSpace.space_size(5, 4))
        self.assertEqual(2520, dss.PermutationSpace.space_size(7, 5))


class ProductSpaceTest(unittest.TestCase):

    elts_to_space = {
        ('', 0): ('',),
        ('a', 1): ('a',),
        ('ab', 1): ('a', 'b'),
        ('ab', 2): ('aa', 'ab', 'ba', 'bb'),
        ('abc', 1): ('a', 'b', 'c'),
        ('abc', 2): (
            'aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc',
            ),
        ('abc', 3): (
            'aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'aca', 'acb', 'acc',
            'baa', 'bab', 'bac', 'bba', 'bbb', 'bbc', 'bca', 'bcb', 'bcc',
            'caa', 'cab', 'cac', 'cba', 'cbb', 'cbc', 'cca', 'ccb', 'ccc',
            ),
        ('abcd', 3): (
            'aaa', 'aab', 'aac', 'aad', 'aba', 'abb', 'abc', 'abd',
            'aca', 'acb', 'acc', 'acd', 'ada', 'adb', 'adc', 'add',
            'baa', 'bab', 'bac', 'bad', 'bba', 'bbb', 'bbc', 'bbd',
            'bca', 'bcb', 'bcc', 'bcd', 'bda', 'bdb', 'bdc', 'bdd',
            'caa', 'cab', 'cac', 'cad', 'cba', 'cbb', 'cbc', 'cbd',
            'cca', 'ccb', 'ccc', 'ccd', 'cda', 'cdb', 'cdc', 'cdd',
            'daa', 'dab', 'dac', 'dad', 'dba', 'dbb', 'dbc', 'dbd',
            'dca', 'dcb', 'dcc', 'dcd', 'dda', 'ddb', 'ddc', 'ddd',
            ),
        ('abcdef', 2): (
            'aa', 'ab', 'ac', 'ad', 'ae', 'af',
            'ba', 'bb', 'bc', 'bd', 'be', 'bf',
            'ca', 'cb', 'cc', 'cd', 'ce', 'cf',
            'da', 'db', 'dc', 'dd', 'de', 'df',
            'ea', 'eb', 'ec', 'ed', 'ee', 'ef',
            'fa', 'fb', 'fc', 'fd', 'fe', 'ff',
            ),
        }

    def test_init_length_out_of_bounds(self):
        with self.assertRaises(dss.StateSpaceError):
            dss.ProductSpace(iter('elmnts'), 10)
        with self.assertRaises(dss.StateSpaceError):
            dss.ProductSpace(iter('elmnts'), -1)

    def test_init_repeated_elements(self):
        with self.assertRaises(dss.StateSpaceError):
            dss.ProductSpace(iter('elements'), 4)

    def test_init_default_length(self):
        space1 = dss.ProductSpace(iter('elmnts'), 6)
        space2 = dss.ProductSpace(iter('elmnts'))
        self.assertEqual(space1.elements, space2.elements)
        self.assertEqual(space1.length, space2.length)

    def test_empty_elements(self):
        space = dss.ProductSpace(iter(()), 0)
        self.assertEqual(1, len(space))
        self.assertIn(0, space)
        self.assertIn(iter(()), space)
        self.assertNotIn(1, space)
        self.assertEqual([], space.state_of(0))
        self.assertEqual(0, space.index_of(iter(())))

    def test_zero_length(self):
        space = dss.ProductSpace(iter('elmnts'), 0)
        self.assertEqual(1, len(space))
        self.assertIn(0, space)
        self.assertIn(iter(()), space)
        self.assertNotIn(1, space)
        self.assertEqual([], space.state_of(0))
        self.assertEqual(0, space.index_of(iter(())))

    def test_size(self):
        for params, perms in self.elts_to_space.items():
            space = dss.ProductSpace(*params)
            self.assertEqual(len(perms), len(space))

    def test_contains(self):
        for params, perms in self.elts_to_space.items():
            space = dss.ProductSpace(*params)
            for idx, perm in enumerate(perms):
                self.assertIn(idx, space)
                self.assertIn(perm, space)
                self.assertIn(iter(perm), space)
        # Return false types other than integers and permutations
        space = dss.ProductSpace('elmnts', 3)
        self.assertNotIn(3.0, space)
        self.assertNotIn('bad', space)

    def test_state_of(self):
        for params, perms in self.elts_to_space.items():
            space = dss.ProductSpace(*params)
            for idx, perm in enumerate(perms):
                self.assertEqual(list(perm), space[idx])
        # Test exceptions
        space = dss.ProductSpace('elmnts', 5)
        with self.assertRaises(NotImplementedError):
            space[:]
        with self.assertRaises(TypeError):
            space['elm']
        with self.assertRaises(IndexError):
            space[space.size()]

    def test_index_of(self):
        for params, perms in self.elts_to_space.items():
            space = dss.ProductSpace(*params)
            for idx, perm in enumerate(perms):
                self.assertEqual(idx, space.index_of(iter(perm)))
        # Test exceptions
        space = dss.ProductSpace('elmnts', 4)
        with self.assertRaises(dss.StateSpaceError):
            space.index_of('elm')
        with self.assertRaises(dss.StateSpaceError):
            space.index_of('melee')
        with self.assertRaises(dss.StateSpaceError):
            space.index_of('elmo')

    def test_space_size(self):
        # Empty
        self.assertEqual(1, dss.ProductSpace.space_size(0, 0))
        self.assertEqual(1, dss.ProductSpace.space_size(10, 0))
        # Full
        self.assertEqual(27, dss.ProductSpace.space_size(3, 3))
        self.assertEqual(3125, dss.ProductSpace.space_size(5, 5))
        # Partial
        self.assertEqual(10, dss.ProductSpace.space_size(10, 1))
        self.assertEqual(25, dss.ProductSpace.space_size(5, 2))
        self.assertEqual(125, dss.ProductSpace.space_size(5, 3))
        self.assertEqual(625, dss.ProductSpace.space_size(5, 4))
        self.assertEqual(16807, dss.ProductSpace.space_size(7, 5))


class CompositeSpaceTest(unittest.TestCase):

    states = (
        # 'abc' permutation length 1
        'a', 'b', 'c',
        # 'abc' permutation length 2
        'ab', 'ac', 'ba', 'bc', 'ca', 'cb',
        # 'kqrs' product length 2
        'kk', 'kq', 'kr', 'ks',
        'qk', 'qq', 'qr', 'qs',
        'rk', 'rq', 'rr', 'rs',
        'sk', 'sq', 'sr', 'ss',
        # 'elmnts' permutation length 2
        'el', 'em', 'en', 'et', 'es',
        'le', 'lm', 'ln', 'lt', 'ls',
        'me', 'ml', 'mn', 'mt', 'ms',
        'ne', 'nl', 'nm', 'nt', 'ns',
        'te', 'tl', 'tm', 'tn', 'ts',
        'se', 'sl', 'sm', 'sn', 'st',
        # 'xyz' permutation length 3
        'xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx',
        # 'defghijklm' product length 1
        'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        # 'nop' product length 3
        'nnn', 'nno', 'nnp', 'non', 'noo', 'nop', 'npn', 'npo', 'npp',
        'onn', 'ono', 'onp', 'oon', 'ooo', 'oop', 'opn', 'opo', 'opp',
        'pnn', 'pno', 'pnp', 'pon', 'poo', 'pop', 'ppn', 'ppo', 'ppp',
        )

    def setUp(self):
        self.space = dss.CompositeSpace(
            dss.PermutationSpace('abc', 1),
            dss.PermutationSpace('abc', 2),
            dss.ProductSpace('kqrs', 2),
            dss.PermutationSpace('elmnts', 2),
            dss.PermutationSpace('xyz', 3),
            dss.ProductSpace('defghijklm', 1),
            dss.ProductSpace('nop', 3),
            )

    def test_empty(self):
        self.space = dss.CompositeSpace()
        self.assertEqual(0, len(self.space))
        self.assertNotIn(0, self.space)
        self.assertNotIn(iter(()), self.space)

    def test_size(self):
        self.assertEqual(len(self.states), len(self.space))

    def test_contains(self):
        for idx, state in enumerate(self.states):
            self.assertIn(idx, self.space)
            self.assertIn(state, self.space)
            self.assertIn(iter(state), self.space)

    def test_state_of(self):
        for idx, state in enumerate(self.states):
            self.assertEqual(list(state), self.space[idx])

    def test_index_of(self):
        for idx, state in enumerate(self.states):
            self.assertEqual(idx, self.space.index_of(iter(state)))


class MultiLengthPermutationSpaceTest(CompositeSpaceTest):

    # 5 elements, lengths 1 to 3
    states = (
        'a', 'b', 'c', 'd', 'e',
        'ab', 'ac', 'ad', 'ae',
        'ba', 'bc', 'bd', 'be',
        'ca', 'cb', 'cd', 'ce',
        'da', 'db', 'dc', 'de',
        'ea', 'eb', 'ec', 'ed',
        'abc', 'abd', 'abe', 'acb', 'acd', 'ace',
        'adb', 'adc', 'ade', 'aeb', 'aec', 'aed',
        'bac', 'bad', 'bae', 'bca', 'bcd', 'bce',
        'bda', 'bdc', 'bde', 'bea', 'bec', 'bed',
        'cab', 'cad', 'cae', 'cba', 'cbd', 'cbe',
        'cda', 'cdb', 'cde', 'cea', 'ceb', 'ced',
        'dab', 'dac', 'dae', 'dba', 'dbc', 'dbe',
        'dca', 'dcb', 'dce', 'dea', 'deb', 'dec',
        'eab', 'eac', 'ead', 'eba', 'ebc', 'ebd',
        'eca', 'ecb', 'ecd', 'eda', 'edb', 'edc',
        )

    def setUp(self):
        self.space = dss.MultiLengthPermutationSpace('abcde', 1, 3)

    def test_space_size(self):
        space_size = dss.MultiLengthPermutationSpace.space_size
        self.assertEqual(1, space_size(0))
        self.assertEqual(2, space_size(1))
        self.assertEqual(5, space_size(2))
        self.assertEqual(16, space_size(3))
        self.assertEqual(65, space_size(4))
        self.assertEqual(326, space_size(5))
        self.assertEqual(80, space_size(5, 2, 3))
        self.assertEqual(200, space_size(5, 2, 4))
        self.assertEqual(206, space_size(5, 4))
        self.assertEqual(259898501, space_size(50, 5))


class MultiLengthProductSpaceTest(CompositeSpaceTest):

    # 5 elements, lengths 1 to 3
    states = (
        'a', 'b', 'c', 'd', 'e',
        'aa', 'ab', 'ac', 'ad', 'ae',
        'ba', 'bb', 'bc', 'bd', 'be',
        'ca', 'cb', 'cc', 'cd', 'ce',
        'da', 'db', 'dc', 'dd', 'de',
        'ea', 'eb', 'ec', 'ed', 'ee',
        'aaa', 'aab', 'aac', 'aad', 'aae',
        'aba', 'abb', 'abc', 'abd', 'abe',
        'aca', 'acb', 'acc', 'acd', 'ace',
        'ada', 'adb', 'adc', 'add', 'ade',
        'aea', 'aeb', 'aec', 'aed', 'aee',
        'baa', 'bab', 'bac', 'bad', 'bae',
        'bba', 'bbb', 'bbc', 'bbd', 'bbe',
        'bca', 'bcb', 'bcc', 'bcd', 'bce',
        'bda', 'bdb', 'bdc', 'bdd', 'bde',
        'bea', 'beb', 'bec', 'bed', 'bee',
        'caa', 'cab', 'cac', 'cad', 'cae',
        'cba', 'cbb', 'cbc', 'cbd', 'cbe',
        'cca', 'ccb', 'ccc', 'ccd', 'cce',
        'cda', 'cdb', 'cdc', 'cdd', 'cde',
        'cea', 'ceb', 'cec', 'ced', 'cee',
        'daa', 'dab', 'dac', 'dad', 'dae',
        'dba', 'dbb', 'dbc', 'dbd', 'dbe',
        'dca', 'dcb', 'dcc', 'dcd', 'dce',
        'dda', 'ddb', 'ddc', 'ddd', 'dde',
        'dea', 'deb', 'dec', 'ded', 'dee',
        'eaa', 'eab', 'eac', 'ead', 'eae',
        'eba', 'ebb', 'ebc', 'ebd', 'ebe',
        'eca', 'ecb', 'ecc', 'ecd', 'ece',
        'eda', 'edb', 'edc', 'edd', 'ede',
        'eea', 'eeb', 'eec', 'eed', 'eee',
        )

    def setUp(self):
        self.space = dss.MultiLengthProductSpace('abcde', 1, 3)

    def test_space_size(self):
        space_size = dss.MultiLengthProductSpace.space_size
        self.assertEqual(1, space_size(0))
        self.assertEqual(2, space_size(1))
        self.assertEqual(7, space_size(2))
        self.assertEqual(40, space_size(3))
        self.assertEqual(341, space_size(4))
        self.assertEqual(3906, space_size(5))
        self.assertEqual(150, space_size(5, 2, 3))
        self.assertEqual(775, space_size(5, 2, 4))
        self.assertEqual(781, space_size(5, 4))
        self.assertEqual(318877551, space_size(50, 5))
