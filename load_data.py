#!/usr/bin/python

import os
import csv
import gzip

import pandas as pd
import numpy as np

from KaggleWord2VecUtility import review_to_wordlist, review_to_sentences

from collections import defaultdict

word_count = defaultdict(int)

def clean_review(review):
    list_of_words = review_to_wordlist(review, remove_stopwords=False)
    for word in list_of_words:
        word_count[word] += 1
    return ' '.join(list_of_words)

good_words = defaultdict(int)
bad_words = defaultdict(int)

def word_counting(inp):
    print inp
    exit(0)

def print_word_count():
    with gzip.open('word_count.csv.gz', 'wb') as wcfile:
        wcfile.write('word,count\n')
        for w, c in sorted(word_count.items(), key=lambda x: x[1]):
            #wcfile.write('%s,%s\n' % (w, c))
            wcfile.write('%s,%d,%d,%d\n' % (c, word_count[word], good_words[word], bad_words[word]))

def load_data(do_plots=False):
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    testdf = pd.read_csv('testData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    unlabeled_traindf = pd.read_csv('unlabeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    
    for idx, row in traindf.iterrows():
        if idx % 1000 == 0:
            print 'finished %d' % idx
        list_of_words = review_to_wordlist(row['review'], remove_stopwords=False)
        for word in list_of_words:
            word_count[word] += 1
            if row['sentiment'] == 0:
                bad_words[word] += 1
            elif row['sentiment'] == 1:
                good_words[word] += 1
    
    exit(0)
    traindf['clean_review'] = traindf['review'].apply(clean_review)

    traindf[['sentiment', 'clean_review']].apply(word_counting)

    print_word_count()

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
