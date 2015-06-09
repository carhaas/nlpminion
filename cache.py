#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gzip
from ast import literal_eval as make_tuple
from abstract_sparse_vector import AbstractSparseVector

class Cache(AbstractSparseVector):
    '''
    A sparse vector holding the information of previously parsed sentences, i.e.
    the sentence as key and the following tuple as value: boolean indicator
    whether it was true or not, the mrl and the answer
    '''

    def from_string(self, string, item_sep="\n", key_val_sep=" ||| "):
        '''
        Takes a string and adds it to the dictionary.

        :param string: string to be parsed
        :param item_sep: the symbol that separates different entries
        :param key_val_sep: the symbol that separates key and value
        '''
        for feature in string.split(item_sep):
            (key, val) = tuple(feature.strip().split(key_val_sep, 1))
            val = make_tuple(val)
            if val[0] == "True":
                val[0] = True
            elif val[0] == "False":
                val[0] = False
            self.dict[key] = val

    def from_function(self, key, val):
        '''
        Receives a key and a value pair that can directly be inserted into the dictionary
        
        :param key: key
        :param val: value
        '''
        self.dict[key] = val

    def from_file(self, in_file, sep=" |||  ", value_is_tuple=False):
        '''
        Read key-value pairs from a file. Assumes one entry per line.

        :param in_file: input file to be parsed
        :param sep: the symbol that separates key and value
        '''
        f = open(in_file, "r")
        for line in f:
            (key, val) = tuple(line.strip().split(sep, 1))
            if value_is_tuple is True:
                val = make_tuple(val)
            if val[0] == "True":
                val[0] = True
            elif val[0] == "False":
                val[0] = False
            self.dict[key] = val
        f.close()

    def from_gz_file(self, in_file, sep=" ||| ", value_is_tuple=False):
        '''
        Read key-value pairs from a .gz file. Assumes one entry per line.

        :param in_file: input file to be parsed
        :param sep: the symbol that separates key and value
        '''
        f = gzip.open(in_file, "rb")
        for line in f:
            if line.startswith(" ||| "):  # then there was no translation for this sentence, need for backward compability
                continue
            (key, val) = tuple(line.strip().split(sep, 1))
            if value_is_tuple is True:
                val_0, val_1, val_2 = tuple(val.strip()[1:-1].split(", ", 2))
                if val_0 == "True":
                    val_0 = True
                elif val_0 == "False":
                    val_0 = False
                val = (val_0, val_1[1:-1], val_2[1:-1])  # strip gets rid of surrounding " here
            self.dict[key] = val
        f.close()

    def to_file(self, out_file, sep=" ||| "):
        '''
        Writes the dictionar's key-value pairs to a file.

        :param out_file: file to be written to
        :param sep: the symbol that separates key and value
        '''
        f = open(out_file, "w")
        for key in self.dict:
            f.write("%s%s%s\n" % (key, sep, self.dict[key]))
        f.close()

    def to_gz_file(self, out_file, sep=" ||| "):
        '''
        Writes the dictionar's key-value pairs to a .gz file.

        :param out_file: file to be written to
        :param sep: the symbol that separates key and value
        '''
        f = gzip.open(out_file, "wb")
        for key in self.dict:
            t1, t2, t3 = self.dict[key]
            f.write("%s%s(%s, \"%s\", \"%s\")\n" % (key, sep, t1, t2, t3))
        f.close()

    # need to explicitly iterate over dictionary and tuple to get the correct encoding..
    def __repr__(self):
        '''
        Returns a representation of this class
        '''
        print_dict = "{"
        for key in self.dict:
            t1, t2, t3 = self.dict[key]
            print_dict += "'%s': (%s, \"%s\", \"%s\"), " % (key, t1, t2, t3)
        print_dict = print_dict[:-2]
        print_dict += "}"
        return print_dict