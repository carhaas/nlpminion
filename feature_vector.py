#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gzip
from abstract_sparse_vector import AbstractSparseVector
from decimal import Decimal

class FeatureVector(AbstractSparseVector):
    '''
    A sparse vector holding the information of features from cdec's translation system
    '''

    def from_string(self, string, item_sep=" ", key_val_sep="="):
        '''
        Takes a string and adds it to the dictionary.

        :param string: string to be parsed
        :param item_sep: the symbol that separates different entries
        :param key_val_sep: the symbol that separates key and value
        '''
        for feature in string.split(item_sep):
            (key, val) = feature.split(key_val_sep)
            self.dict[key] = float(val)

    def from_function(self, key, val):
        '''
        Receives a key and a value pair that can directly be inserted into the dictionary
        
        :param key: key
        :param val: value
        '''
        self.dict[key] = val

    def from_file(self, in_file, sep=" "):
        '''
        Read key-value pairs from a file. Assumes one entry per line.

        :param in_file: input file to be parsed
        :param sep: the symbol that separates key and value
        '''
        f = open(in_file, "r")
        for line in f:
            (key, val) = tuple(line.strip().split(sep, 1))
            self.dict[key] = float(val)
        f.close()

    def from_gz_file(self, in_file, sep=" "):
        '''
        Read key-value pairs from a .gz file. Assumes one entry per line.

        :param in_file: input file to be parsed
        :param sep: the symbol that separates key and value
        '''
        f = gzip.open(in_file, "rb")
        for line in f:
            (key, val) = tuple(line.strip().split(sep, 1))
            self.dict[key] = float(val)
        f.close()

    def to_file(self, out_file, sep=" "):
        '''
        Writes the dictionar's key-value pairs to a file.

        :param out_file: file to be written to
        :param sep: the symbol that separates key and value
        '''
        f = open(out_file, "w")
        for key in sorted(self.dict):
            format = ("%.16f" % self.dict[key]).rstrip("0")
            if format.endswith("."):
                format = format+"0"
            print >> f, "%s%s%s" % (key, sep, format)
            #print >> f, "%s%s%s" % (key, sep, self.dict[key])
            #print >> f, "%s%s%s" % (key, sep, Decimal(self.dict[key]))
        f.close()

    def to_gz_file(self, out_file, sep=" "):
        '''
        Writes the dictionar's key-value pairs to a .gz file.

        :param out_file: file to be written to
        :param sep: the symbol that separates key and value
        '''
        f = gzip.open(out_file, "wb")
        for key in self.dict:
            format = ("%.16f" % self.dict[key]).rstrip("0") #16f
            if format.endswith("."): #16f ensure .0
                format = format+"0"
            print >> f, "%s%s%s" % (key, sep, format)
            #f.write("%s%s%s\n" % (key, sep, self.dict[key])) #ori
            #f.write("%s%s%s\n" % (key, sep, Decimal(self.dict[key]))) #decimal
        f.close()

    def __add__(self, x):
        '''
        Performs an in place element wise summation given a second FeatureVector

        :param x: the second FeatureVector
        '''
        for key in x.dict:
            if key in self.dict:
                self.dict[key] = self.dict[key] + x.dict[key]
            else:
                self.dict[key] = x.dict[key]
        return self

    def __sub__(self, x):
        '''
        Performs an in place element wise substraction given a second FeatureVector

        :param x: the second FeatureVector
        '''
        for key in x.dict:
            if key in self.dict:
                self.dict[key] = self.dict[key] - x.dict[key]
            else:
                self.dict[key] = 0 - x.dict[key]
        return self

    def __mul__(self, x):
        '''
        Performs an in place element wise multiplication given a scalar

        :param x: the second FeatureVector
        '''
        for key in self.dict:
            self.dict[key] = self.dict[key] * x
        return self

    def __repr__(self):
        '''
        Returns a representation of this class
        '''
        print_dict = "{"
        for key in self.dict:
            print_dict += "'%s': %s, " % (key, str(self.dict[key]))
        print_dict = print_dict[:-2]
        print_dict += "}"
        return print_dict