#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Adadelta as described in (Zeiler, 2013) extended with

'''

class Adadelta:
    def __init__(self, rho=0.95, epsilon=1.0e-6):
        self.rho = rho
        self.epsilon = epsilon

        self.accum_grad = 0
        self.accum_update = 0


    def update(self):
        pass
        # compute gradient

        # accumulate gradient

        # compute update

        # accumulate update

        # apply update