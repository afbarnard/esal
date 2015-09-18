# Discrete state spaces useful for sequences
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import bisect
import itertools as itools


class StateSpaceError(Exception):
    pass


class PermutationSpace(object):

    def __init__(self, elements, length=None):
        self.elements = tuple(elements)
        self.length = (int(length) if length is not None
                       else len(self.elements))
        if not (0 <= self.length <= len(self.elements)):
            raise StateSpaceError(
                'Length out of bounds [0, {}]: {}'
                .format(len(self.elements), length))
        self.elts_to_idxs = dict(zip(self.elements, itools.count()))
        if len(self.elements) != len(self.elts_to_idxs):
            raise StateSpaceError(
                'Elements are not unique: {}'
                .format(self.elements))
        self.bases = PermutationSpace._permutation_index_bases(
            len(self.elements), self.length)

    @staticmethod
    def _permutation_index_bases(number_elements, permutation_length):
        if permutation_length == 0:
            return ()
        bases = [None] * permutation_length
        bases[-1] = 1
        for idx in range(permutation_length - 1, 0, -1):
            bases[idx - 1] = bases[idx] * (number_elements - idx)
        return bases

    @staticmethod
    def space_size(number_elements, permutation_length):
        product = 1
        for n in range(
                number_elements - permutation_length + 1,
                number_elements + 1):
            product *= n
        return product

    def size(self):
        if len(self.bases) == 0:
            return 1
        else:
            return self.bases[0] * len(self.elements)

    __len__ = size

    def __contains__(self, obj):
        if isinstance(obj, int):
            return 0 <= obj < self.size()
        elif hasattr(obj, '__iter__'):
            # Do membership check without converting to an index
            perm = tuple(obj)
            # Length must match
            if len(perm) != self.length:
                return False
            # Check each element is valid and used at most once
            in_use = [False] * len(self.elements)
            for element in perm:
                if element not in self.elts_to_idxs:
                    return False
                idx = self.elts_to_idxs[element]
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
        free_elements = list(self.elements)
        # The permutation
        perm = [None] * self.length
        # Build the permutation by repeatedly dividing the given index
        # by the bases and finding the corresponding unused element
        for idx in range(self.length):
            # Which free element to use
            free_idx = index // self.bases[idx]
            perm[idx] = free_elements[free_idx]
            del free_elements[free_idx]
            # Update the index
            index %= self.bases[idx]
        return perm

    __getitem__ = state_of

    def index_of(self, perm):
        index = 0
        used = set()
        idx = 0
        for element in perm:
            # Check for repeated elements
            if element in used:
                raise StateSpaceError(
                    'Element already used earlier in permutation: {}'
                    .format(element))
            # Count how many elements with lower indices are used
            try:
                element_idx = self.elts_to_idxs[element]
            except KeyError:
                raise StateSpaceError(
                    'Element not in permutation space: {}'
                    .format(element))
            num_lower_used = 0
            for elt in used:
                if self.elts_to_idxs[elt] < element_idx:
                    num_lower_used += 1
            # Add the contribution of this element to the index
            index += (element_idx - num_lower_used) * self.bases[idx]
            used.add(element)
            idx += 1
        if idx != self.length:
            raise StateSpaceError(
                'Length out of bounds [0, {}): {}'
                .format(self.length, idx))
        return index

    def __repr__(self):
        return 'PermutationSpace({}, {})'.format(
            self.elements, self.length)


class ProductSpace(object):

    def __init__(self, elements, length=None):
        self.elements = tuple(elements)
        self.length = (int(length) if length is not None
                       else len(self.elements))
        if not (0 <= self.length <= len(self.elements)):
            raise StateSpaceError(
                'Length out of bounds [0, {}]: {}'
                .format(len(self.elements), length))
        self.elts_to_idxs = dict(zip(self.elements, itools.count()))
        if len(self.elements) != len(self.elts_to_idxs):
            raise StateSpaceError(
                'Elements are not unique: {}'
                .format(self.elements))

    @staticmethod
    def space_size(number_elements, length):
        return number_elements ** length

    def size(self):
        return len(self.elements) ** self.length

    __len__ = size

    def __contains__(self, obj):
        if isinstance(obj, int):
            return 0 <= obj < self.size()
        elif hasattr(obj, '__iter__'):
            # Do membership check without converting to an index
            index = 0
            for element in obj:
                # Check that the element is valid, obj is not too long
                if (element not in self.elts_to_idxs or
                        index >= self.length):
                    return False
                index += 1
            # Length must match
            return index == self.length
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
        state = [None] * self.length
        # Build the state by repeatedly dividing the given index by the
        # base and finding the corresponding element
        radix = len(self.elements)
        base = radix ** (self.length - 1) if self.length > 0 else 1
        for idx in range(self.length):
            state[idx] = self.elements[index // base]
            index %= base
            base //= radix
        return state

    __getitem__ = state_of

    def index_of(self, state):
        index = 0
        radix = len(self.elements)
        base = radix ** (self.length - 1) if self.length > 0 else 1
        elt_count = 0
        for element in state:
            try:
                element_idx = self.elts_to_idxs[element]
            except KeyError:
                raise StateSpaceError(
                    'Element not in product space: {}'
                    .format(element))
            index += element_idx * base
            base //= radix
            elt_count += 1
        if elt_count != self.length:
            raise StateSpaceError(
                'Length out of bounds [0, {}): {}'
                .format(self.length, elt_count))
        return index

    def __repr__(self):
        return 'ProductSpace({}, {})'.format(self.elements, self.length)


class CompositeSpace(object):

    def __init__(self, *spaces):
        # Check if spaces contains a single iterable or a list of spaces
        if len(spaces) == 1 and hasattr(spaces[0], '__iter__'):
            self.spaces = tuple(spaces[0])
        else:
            self.spaces = tuple(spaces)
        # Calculate the boundaries of the index partitions
        self.partitions = [0] * (len(self.spaces) + 1)
        for idx, space in enumerate(self.spaces):
            self.partitions[idx + 1] = self.partitions[idx] + len(space)

    def size(self):
        return self.partitions[-1]

    __len__ = size

    def __contains__(self, obj):
        if isinstance(obj, int):
            return 0 <= obj < self.size()
        else:
            state = tuple(obj)
            return any(state in space for space in self.spaces)

    def state_of(self, index):
        # Check for bounds
        if not (0 <= index < self.size()):
            raise IndexError(
                'Index out of bounds [0, {}): {}'
                .format(self.size(), index))
        # Find which subspace this index belongs to
        idx = bisect.bisect(self.partitions, index) - 1
        # Return the appropriate state of the subspace
        return self.spaces[idx].state_of(index - self.partitions[idx])

    __getitem__ = state_of

    def index_of(self, state):
        state = tuple(state)
        for idx, space in enumerate(self.spaces):
            if state in space:
                return self.partitions[idx] + space.index_of(state)
        raise StateSpaceError('State not in space: {}'.format(state))

    def __repr__(self):
        return 'CompositeSpace({}, {})'.format(len(self.spaces),
                                               len(self))


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
        self.elements = tuple(elements)
        self.min_length, self.max_length = _handle_length_arguments(
            length1, length2, len(self.elements))
        super().__init__(
            PermutationSpace(self.elements, length)
            for length in range(self.min_length, self.max_length + 1))

    @staticmethod
    def space_size(number_elements, length1=None, length2=None):
        min_length, max_length = _handle_length_arguments(
            length1, length2, number_elements)
        return sum(PermutationSpace.space_size(number_elements, length)
                   for length in range(min_length, max_length + 1))

    def __repr__(self):
        return 'MultiLengthPermutationSpace({}, {}, {})'.format(
            self.elements, self.min_length, self.max_length)


class MultiLengthProductSpace(CompositeSpace):

    def __init__(self, elements, length1=None, length2=None):
        self.elements = tuple(elements)
        self.min_length, self.max_length = _handle_length_arguments(
            length1, length2, len(self.elements))
        super().__init__(
            ProductSpace(self.elements, length)
            for length in range(self.min_length, self.max_length + 1))

    @staticmethod
    def space_size(number_elements, length1=None, length2=None):
        min_length, max_length = _handle_length_arguments(
                length1, length2, number_elements)
        return sum(ProductSpace.space_size(number_elements, length)
                   for length in range(min_length, max_length + 1))

    def __repr__(self):
        return 'MultiLengthProductSpace({}, {}, {})'.format(
            self.elements, self.min_length, self.max_length)
