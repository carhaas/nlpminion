#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Adadelta as described in (Zeiler, 2013)

'''

from math import sqrt
from feature_vector import FeatureVector

class Adadelta:
    def __init__(self, rho=0.95, epsilon=1.0e-6):
        '''
        Initialises the accumalative gradient and update parameters, as well as
        the decay constant rho and constant epsilon that ensures non-zero
        denominator
        
        :param rho: decay constant
        :param epsilon: constant that ensures non-zero denominator
        '''
        self.rho = rho
        self.epsilon = epsilon

        self.accum_grad = FeatureVector()
        self.accum_update = FeatureVector()


    def update(self, gradient):
        '''
        given a gradient this function computes the delta to be used for
        updating, accumulates gradient and update
        
        :param gradient: the gradient of the objective function as a
        FeatureVector
        
        :return: the delta to be used for the update
        '''
        delta = FeatureVector()

        # would be nicer if we could directly do this operation on FeatureVector without the need to iterate
        for key, gradient_value in gradient:
            #print "key: %s" % key
            #print "gradient_value: %s" % gradient_value

            # if this dimension hasn't been seen, initialise with 0
            if key not in self.accum_grad.dict:
                self.accum_grad.from_function(key, 0.0)  # does this work as there is only 1 item?
            if key not in self.accum_update.dict:
                self.accum_update.from_function(key, 0.0)  # does this work as there is only 1 item?

            # accumulate gradient
            self.accum_grad.dict[key] = self.rho * self.accum_grad.dict[key] + (1-self.rho) * gradient_value ** 2
            #print "self.accum_grad.dict[key]: %s" % self.accum_grad.dict[key]

            # compute update
            delta.dict[key] = - sqrt(self.accum_update.dict[key] + self.epsilon) / sqrt(self.accum_grad.dict[key] + self.epsilon) * gradient_value
            #print "delta.dict[key]: %s" % delta.dict[key]

            # accumulate update
            self.accum_update.dict[key] = self.rho * self.accum_update.dict[key] + (1-self.rho) * delta.dict[key] ** 2
            #print "self.accum_update.dict[key]: %s" % self.accum_update.dict[key]

        return delta