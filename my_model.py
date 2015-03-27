#!/usr/bin/python

import os
import gzip

import cPickle as pickle

from load_data import load_data

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data()
