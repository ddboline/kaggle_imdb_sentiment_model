#!/usr/bin/python

import os
import csv
import gzip
import multiprocessing
from collections import defaultdict

import pandas as pd
import numpy as np

import nltk

from sklearn.feature_extraction.text import CountVectorizer

from KaggleWord2VecUtility import review_to_wordlist, review_to_sentences

from gensim.models import Word2Vec

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_review(review):
    list_of_words = review_to_wordlist(review, remove_stopwords=False)
    return ' '.join(list_of_words)

def load_data(do_plots=False):
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    testdf = pd.read_csv('testData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)

    traincleanreview = traindf['review'].apply(clean_review).tolist()
    testcleanreview = testdf['review'].apply(clean_review).tolist()
    unlabeledcleanreview = unlabeled_traindf['review'].apply(clean_review).tolist()

    model_name = "300features_40minwords_10context"
    model = Word2Vec.load(model_name)

    # Set values for various parameters
    num_features = 300    # Word vector dimensionality
    min_word_count = 40   # Minimum word count
    num_workers = 4       # Number of threads to run in parallel
    context = 10          # Context window size
    downsampling = 1e-3   # Downsample setting for frequent words

    # Initialize and train the model (this will take some time)
    print "Training Word2Vec model..."
    model = Word2Vec(sentences, workers=num_workers, \
                size=num_features, min_count = min_word_count, \
                window = context, sample = downsampling, seed=1)

    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

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
