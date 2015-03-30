#!/usr/bin/python

import os
import gzip

import cPickle as pickle

from load_data import load_data
#from load_data_bagofwords import load_data

from sklearn.ensemble import RandomForestClassifier

from sklearn.cross_validation import train_test_split

import numpy as np
import pandas as pd

def score_model(model, xtrain, ytrain):
    randint = reduce(lambda x,y: x|y, [ord(x)<<(n*8) for (n,x) in
                                       enumerate(os.urandom(4))])
    xTrain, xTest, yTrain, yTest = train_test_split(xtrain, ytrain,
                                                    test_size=0.4,
                                                    random_state=randint)
    model.fit(xTrain, yTrain)
    print model
    print model.score(xTest, yTest)
    return

def prepare_submission(model, xtrain, ytrain, xtest, ytest):

    model.fit(xtrain, ytrain)
    ytest_pred = model.predict(xtest)

    output = pd.DataFrame(data={'id': ytest, 'sentiment': ytest_pred})
    output.to_csv('submission.csv', index=False, quoting=3)

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data()

    model = RandomForestClassifier(n_estimators=400, n_jobs=-1)

    score_model(model, xtrain, ytrain)
    prepare_submission(model, xtrain, ytrain, xtest, ytest)
