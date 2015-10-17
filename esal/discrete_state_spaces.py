# Discrete state spaces useful for sequences
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import bisect
import itertools as itools

from . import general


class StateSpaceError(Exception):
    pass


# TODO refactor to consolidate behavior, perhaps into an abstract superclass DiscreteStateSpace


class PermutationSpace(object):

    def __init__(self, elements, length=None):
        self._elements = tuple(elements)
        self._length = (int(length) if length is not None
                        else len(self._elements))
        if not (0 <= self._length <= len(self._elements)):
            raise StateSpaceError(
                'Length out of bounds [0, {}]: {}'
                .format(len(self._elements), length))
        self._elts_to_idxs = dict(zip(self._elements, itools.count()))
        if len(self._elements) != len(self._elts_to_idxs):
            raise StateSpaceError(
                'Elements are not unique: {}'
                .format(self._elements))
        self._bases = PermutationSpace._permutation_index_bases(
            len(self._elements), self._length)

    @staticmethod
    def _permutation_index_bases(number_elements, state_length):
        if state_length == 0:
            return ()
        bases = [None] * state_length
        bases[-1] = 1
        for idx in range(state_length - 1, 0, -1):
            bases[idx - 1] = bases[idx] * (number_elements - idx)
        return bases

    @staticmethod
    def space_size(number_elements, state_length):
        product = 1
        for n in range(
                number_elements - state_length + 1,
                number_elements + 1):
            product *= n
        return product

    def size(self):
        if len(self._bases) == 0:
            return 1
        else:
            return self._bases[0] * len(self._elements)

    __len__ = size

    def __contains__(self, obj):
        if isinstance(obj, int):
            return 0 <= obj < self.size()
        elif hasattr(obj, '__iter__'):
            # Do membership check without converting to an index
            state = tuple(obj)
            # Length must match
            if len(state) != self._length:
                return False
            # Check each element is valid and used at most once
            in_use = [False] * len(self._elements)
            for element in state:
                if element not in self._elts_to_idxs:
                    return False
                idx = self._elts_to_idxs[element]
                if in_use[idx]:
                    return False
                in_use[idx] = True
            return True
        else:
            return False

    def state_of(self, index):
        # Check index type
        if not isinstance(index, int):
            if isinstance(index, slice):
                raise NotImplementedError('Slices not implemented.')
            raise TypeError(
                'Index must be an integer, not: {}'.format(index))
        # Check for bounds
        if not (0 <= index < self.size()):
            raise IndexError(
                'Index out of bounds [0, {}): {}'
                .format(self.size(), index))
        # The elements available to use in the permutation
        free_elements = list(self._elements)
        # The permutation
        perm = [None] * self._length
        # Build the permutation by repeatedly dividing the given index
        # by the bases and finding the corresponding unused element
        for idx in range(self._length):
            # Which free element to use
            free_idx = index // self._bases[idx]
            perm[idx] = free_elements[free_idx]
            del free_elements[free_idx]
            # Update the index
            index %= self._bases[idx]
        return perm

    __getitem__ = state_of

    def index_of(self, state):
        index = 0
        used = set()
        idx = 0
        for element in state:
            # Check for repeated elements
            if element in used:
                raise StateSpaceError(
                    'Element already used earlier in permutation: {}'
                    .format(element))
            # Count how many elements with lower indices are used
            try:
                element_idx = self._elts_to_idxs[element]
            except KeyError:
                raise StateSpaceError(
                    'Element not in permutation space: {}'
                    .format(element))
            num_lower_used = 0
            for elt in used:
                if self._elts_to_idxs[elt] < element_idx:
                    num_lower_used += 1
            # Add the contribution of this element to the index
            index += (element_idx - num_lower_used) * self._bases[idx]
            used.add(element)
            idx += 1
        if idx != self._length:
            raise StateSpaceError(
                'Length out of bounds [0, {}): {}'
                .format(self._length, idx))
        return index

    def __repr__(self):
        return 'PermutationSpace({}, {})'.format(
            self._elements, self._length)

    @property
    def elements(self):
        return self._elements

    @property
    def state_min_length(self):
        return self._length

    @property
    def state_max_length(self):
        return self._length


class ProductSpace(object):

    def __init__(self, elements, length=None):
        self._elements = tuple(elements)
        self._length = (int(length) if length is not None
                        else len(self._elements))
        if not (0 <= self._length <= len(self._elements)):
            raise StateSpaceError(
                'Length out of bounds [0, {}]: {}'
                .format(len(self._elements), length))
        self._elts_to_idxs = dict(zip(self._elements, itools.count()))
        if len(self._elements) != len(self._elts_to_idxs):
            raise StateSpaceError(
                'Elements are not unique: {}'
                .format(self._elements))

    @staticmethod
    def space_size(number_elements, length):
        return number_elements ** length

    def size(self):
        return len(self._elements) ** self._length

    __len__ = size

    def __contains__(self, obj):
        if isinstance(obj, int):
            return 0 <= obj < self.size()
        elif hasattr(obj, '__iter__'):
            # Do membership check without converting to an index
            index = 0
            for element in obj:
                # Check that the element is valid, obj is not too long
                if (element not in self._elts_to_idxs or
                        index >= self._length):
                    return False
                index += 1
            # Length must match
            return index == self._length
        else:
            return False

    def state_of(self, index):
        # Check index type
        if not isinstance(index, int):
            if isinstance(index, slice):
                raise NotImplementedError('Slices not implemented.')
            raise TypeError(
                'Index must be an integer, not: {}'.format(index))
        # Check for bounds
        if not (0 <= index < self.size()):
            raise IndexError(
                'Index out of bounds [0, {}): {}'
                .format(self.size(), index))
        # The state
        state = [None] * self._length
        # Build the state by repeatedly dividing the given index by the
        # base and finding the corresponding element
        radix = len(self._elements)
        base = radix ** (self._length - 1) if self._length > 0 else 1
        for idx in range(self._length):
            state[idx] = self._elements[index // base]
            index %= base
            base //= radix
        return state

    __getitem__ = state_of

    def index_of(self, state):
        index = 0
        radix = len(self._elements)
        base = radix ** (self._length - 1) if self._length > 0 else 1
        elt_count = 0
        for element in state:
            try:
                element_idx = self._elts_to_idxs[element]
            except KeyError:
                raise StateSpaceError(
                    'Element not in product space: {}'
                    .format(element))
            index += element_idx * base
            base //= radix
            elt_count += 1
        if elt_count != self._length:
            raise StateSpaceError(
                'Length out of bounds [0, {}): {}'
                .format(self._length, elt_count))
        return index

    def __repr__(self):
        return 'ProductSpace({}, {})'.format(
            self._elements, self._length)

    @property
    def elements(self):
        return self._elements

    @property
    def state_min_length(self):
        return self._length

    @property
    def state_max_length(self):
        return self._length


class CompositeSpace(object):

    def __init__(self, *spaces):
        # Check if spaces contains a single iterable or a list of spaces
        if len(spaces) == 1 and hasattr(spaces[0], '__iter__'):
            self._spaces = tuple(spaces[0])
        else:
            self._spaces = tuple(spaces)
        # Calculate the boundaries of the index partitions
        self._partitions = [0] * (len(self._spaces) + 1)
        for idx, space in enumerate(self._spaces):
            self._partitions[idx + 1] = self._partitions[idx] + len(space)
        # Set fields typically managed by subclasses if not already set
        if not hasattr(self, '_elements'):
            self._elements = tuple(general.firsts(
                itools.chain.from_iterable(
                    space.elements for space in self._spaces)))
        if not hasattr(self, '_min_length'):
            self._min_length = 0
            if spaces:
                self._min_length = min(
                    space.state_min_length for space in spaces)
        if not hasattr(self, '_max_length'):
            self._max_length = 0
            if spaces:
                self._max_length = max(
                    space.state_max_length for space in spaces)

    def size(self):
        return self._partitions[-1]

    __len__ = size

    def __contains__(self, obj):
        if isinstance(obj, int):
            return 0 <= obj < self.size()
        else:
            state = tuple(obj)
            return any(state in space for space in self._spaces)

    def state_of(self, index):
        # Check for bounds
        if not (0 <= index < self.size()):
            raise IndexError(
                'Index out of bounds [0, {}): {}'
                .format(self.size(), index))
        # Find which subspace this index belongs to
        idx = bisect.bisect(self._partitions, index) - 1
        # Return the appropriate state of the subspace
        return self._spaces[idx].state_of(index - self._partitions[idx])

    __getitem__ = state_of

    def index_of(self, state):
        state = tuple(state)
        for idx, space in enumerate(self._spaces):
            if state in space:
                return self._partitions[idx] + space.index_of(state)
        raise StateSpaceError('State not in space: {}'.format(state))

    def __repr__(self):
        return 'CompositeSpace({}, {})'.format(len(self._spaces),
                                               len(self))

    @property
    def elements(self):
        return self._elements

    @property
    def state_min_length(self):
        return self._min_length

    @property
    def state_max_length(self):
        return self._max_length


def _handle_length_arguments(length1, length2, default_max, default_min=0):
    if length2 is not None and length1 is not None:
        min_length = length1
        max_length = length2
    elif length1 is not None:
        min_length = default_min
        max_length = length1
    else:
        min_length = default_min
        max_length = default_max
    if not (0 <= min_length <= max_length <= default_max):
        raise ValueError(
            'Bad length range: [{}, {}] <= {}'
            .format(min_length, max_length, default_max))
    return min_length, max_length


class MultiLengthPermutationSpace(CompositeSpace):

    def __init__(self, elements, length1=None, length2=None):
        self._elements = tuple(elements)
        self._min_length, self._max_length = _handle_length_arguments(
            length1, length2, len(self._elements))
        super().__init__(
            PermutationSpace(self._elements, length)
            for length in range(self._min_length, self._max_length + 1))

    @staticmethod
    def space_size(number_elements, length1=None, length2=None):
        min_length, max_length = _handle_length_arguments(
            length1, length2, number_elements)
        return sum(PermutationSpace.space_size(number_elements, length)
                   for length in range(min_length, max_length + 1))

    def __repr__(self):
        return 'MultiLengthPermutationSpace({}, {}, {})'.format(
            self._elements, self._min_length, self._max_length)


class MultiLengthProductSpace(CompositeSpace):

    def __init__(self, elements, length1=None, length2=None):
        self._elements = tuple(elements)
        self._min_length, self._max_length = _handle_length_arguments(
            length1, length2, len(self._elements))
        super().__init__(
            ProductSpace(self._elements, length)
            for length in range(self._min_length, self._max_length + 1))

    @staticmethod
    def space_size(number_elements, length1=None, length2=None):
        min_length, max_length = _handle_length_arguments(
                length1, length2, number_elements)
        return sum(ProductSpace.space_size(number_elements, length)
                   for length in range(min_length, max_length + 1))

    def __repr__(self):
        return 'MultiLengthProductSpace({}, {}, {})'.format(
            self._elements, self._min_length, self._max_length)
