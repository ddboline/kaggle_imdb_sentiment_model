#!/usr/bin/python

import os
import csv
import gzip
import multiprocessing
from collections import defaultdict

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer

from KaggleWord2VecUtility import review_to_wordlist, review_to_sentences

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_review(review):
    list_of_sentences = review_to_sentences(review, tokenizer, remove_stopwords=False)
    return list_of_sentences

def load_data_bagofwords(do_plots=False):
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    testdf = pd.read_csv('testData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    unlabeled_traindf = pd.read_csv('unlabeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    
    traincleanreview = traindf['review'].apply(clean_review)
    print type(traincleanreview)
    exit(0)
    testcleanreview = testdf['review'].apply(clean_review)
    vectorizer = CountVectorizer(analyzer='word', vocabulary=biased_word_list)
    trainwvector = vectorizer.transform(traincleanreview).toarray()
    testwvector = vectorizer.transform(testcleanreview).toarray()

    #traindf['wvector'] = traindf['review'].apply(clean_review)
    #testdf['wvector'] = testdf['review'].apply(clean_review)
    
    traindf = traindf.drop(labels=['review'], axis=1)
    testdf = testdf.drop(labels=['review'], axis=1)

    print traindf.shape, testdf.shape
    print traindf.columns
    print testdf.columns

    xtrain = trainwvector
    ytrain = traindf['sentiment'].values
    xtest = testwvector
    ytest = testdf['id'].values
    
    return xtrain, ytrain, xtest, ytest

def load_data(do_plots=False):
    return load_data_bagofwords(do_plots)

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data(do_plots=True)

    print xtrain.shape, ytrain.shape, xtest.shape, ytest.shape
