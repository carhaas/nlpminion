#!/usr/bin/env python
# -*- coding: utf-8 -*-
from feature_vector import FeatureVector


class Translation:
    '''
    A object that stores a translation as returned by cdec.
    '''

    def __init__(self, kbest_entry):
        '''
        Expects an k-best list output entry from the cdec decoder. The string is split into its relevant parts

        :param kbest_entry: one line of cdec output in k-best format (the format cdec returns when the -k option is used)
        '''
        self.bleu_score = None
        self.decoder_rank = None
        self.bleu_rank = None
        self.decoder_ori = None
        self.features = FeatureVector()
        (self.idval, self.string, features_raw, self.decoder_score) = tuple(kbest_entry.strip().split(" ||| "))
        self.decoder_score = float(self.decoder_score)
        self.features.from_string(features_raw)

    def __repr__(self):
        '''
        :return: A Translation objects representation
        '''
        return "<%s:%s:%s:%s:%s>" % (
            self.string, self.decoder_score, self.bleu_score, self.decoder_rank, self.bleu_rank)