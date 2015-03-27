#!/usr/bin/python

import os
import gzip

import pandas as pd
import numpy as np

def load_data(do_plots=False):
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    testdf = pd.read_csv('testData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    unlabeled_traindf = pd.read_csv('unlabeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    
    print traindf.shape, testdf.shape, unlabeled_traindf.shape
    print traindf.columns
    print testdf.columns
    print unlabeled_traindf.columns

    xtrain = None
    ytrain = traindf['sentiment'].values
    xtest = None
    ytest = testdf['id'].values
    
    return 4*[None]

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data(do_plots=True)
