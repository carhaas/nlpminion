#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta
import sys

class AbstractSparseVector:
    '''
    A abstract class for a sparse vector using a dictionary.
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        '''
        Initialises the dictionary that is used as a sparse vector
        '''
        self.dict = {}

    def from_string(self, string, item_sep, key_val_sep):
        '''
        Takes a string, the specification of which is to be implemented in inheriting classes
        and adds it to the dictionary.

        :param string: string to be parsed
        :param item_sep: the symbol that separates different entries
        :param key_val_sep: the symbol that separates key and value
        '''
        raise NotImplementedError()

    def from_function(self, key, val):
        '''
        Receives a key and a value pair that can directly be inserted into the dictionary
        :param key: key
        :param val: value
        '''
        raise NotImplementedError()

    def from_file(self, in_file, sep):
        '''
        Read key-value pairs from a file. Assumes one entry per line.

        :param in_file: input file to be parsed
        :param sep: the symbol that separates key and value
        '''
        raise NotImplementedError()

    def from_gz_file(self, in_file, sep):
        '''
        Read key-value pairs from a .gz file. Assumes one entry per line.

        :param in_file: input file to be parsed
        :param sep: the symbol that separates key and value
        '''
        raise NotImplementedError()

    def to_file(self, out_file, sep):
        '''
        Writes the dictionar's key-value pairs to a file.

        :param out_file: file to be written to
        :param sep: the symbol that separates key and value
        '''
        raise NotImplementedError()

    def to_gz_file(self, out_file, sep):
        '''
        Writes the dictionar's key-value pairs to a .gz file.

        :param out_file: file to be written to
        :param sep: the symbol that separates key and value
        '''
        raise NotImplementedError()

    def pop(self, key):
        '''
        Deletes a given key from the dictionary.

        :param key: Key to be deleted.
        '''
        self.dict.pop(key)

    def clear(self):
        '''
        Empties the whole dictionary.
        '''
        self.dict.clear()

    def __iter__(self):
        '''
        Provides an iterator over the dictionaries keys
        '''
        for key in self.dict:
            yield (key, self.dict[key])

    def _compare(self, other, method):
        '''
        Given a comparison operator and two objects, checks if the comparison evaluates to true or false.

        :param other: Another object to compare to
        :param method: The kind of comparison to be performed.
        :return: If implemented it returns True or False.
        '''
        try:
            return method(self._cmpkey(), other._cmpkey())
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other".
            return NotImplemented

    def __lt__(self, other):
        '''
        Sends "less than" method to _compare and returns _compare's return value.
         '''
        return self._compare(other, lambda s,o: s < o)

    def __le__(self, other):
        '''
        Sends "less than or equal" method to _compare and returns _compare's return value.
         '''
        return self._compare(other, lambda s,o: s <= o)

    def __eq__(self, other):
        '''
        Sends "equal" method to _compare and returns _compare's return value.
         '''
        return self._compare(other, lambda s,o: s == o)
        #return self.dict == other.dict

    def __ge__(self, other):
        '''
        Sends "greater than or equal" method to _compare and returns _compare's return value.
         '''
        return self._compare(other, lambda s,o: s >= o)

    def __gt__(self, other):
        '''
        Sends "greater than" method to _compare and returns _compare's return value.
         '''
        return self._compare(other, lambda s,o: s > o)

    def __ne__(self, other):
        '''
        Sends "not equal" method to _compare and returns _compare's return value.
         '''
        return self._compare(other, lambda s,o: s != o)
        #return self.dict != other.dict

    def _cmpkey(self):
        '''
        Returns the dictionary object for comparison
        '''
        return self.dict

