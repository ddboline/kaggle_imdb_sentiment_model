#!/usr/bin/python

import os
import csv
import gzip

import pandas as pd
import numpy as np

from KaggleWord2VecUtility import review_to_wordlist, review_to_sentences

from collections import defaultdict

import multiprocessing

from sklearn.feature_extraction.text import CountVectorizer

word_count = defaultdict(int)

def clean_review(review):
    list_of_words = review_to_wordlist(review, remove_stopwords=False)
    return ' '.join(list_of_words)

good_words = defaultdict(int)
bad_words = defaultdict(int)

def word_counting(inp):
    print inp
    exit(0)

def proc_row(inp):
    return inp[0], inp[1]['sentiment'], review_to_wordlist(inp[1]['review'])

def generate_biased_word_list():
    ''' count words in training sample '''
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    
    pool = multiprocessing.Pool(2)
    idx = 0
    for idx, sentiment, list_of_words in pool.imap_unordered(proc_row, traindf.iterrows()):
        if idx % 1000 == 0:
            print 'finished %d' % idx
        for word in list_of_words:
            word_count[word] += 1
            if sentiment == 0:
                bad_words[word] += 1
            elif sentiment == 1:
                good_words[word] += 1
    
    with gzip.open('word_count.csv.gz', 'wb') as wcfile:
        wcfile.write('word,count,good,bad,frac\n')
        for w, c in sorted(word_count.items(), key=lambda x: x[1]):
            wcfile.write('%s,%d,%d,%d,%f\n' % (w, c, good_words[w], bad_words[w], abs(good_words[w]-bad_words[w])/float(c)))

def load_data(do_plots=False):
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    testdf = pd.read_csv('testData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    #unlabeled_traindf = pd.read_csv('unlabeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    word_count_df = pd.read_csv('word_count.csv.gz', compression='gzip')
    
    cond0 = word_count_df['count']>1000
    cond1 = word_count_df['frac']>0.2
    biased_word_list = {w: n for n, w in enumerate(list(word_count_df[cond0 & cond1]['word']))}
    
    traindf['clean_review'] = traindf['review'].apply(clean_review)
    testdf['clean_review'] = testdf['review'].apply(clean_review)
    
    vectorizer = CountVectorizer(analyzer='word', vocabulary=biased_word_list)
    
    traindf['wvector'] = vectorizer.transform(traindf['clean_review'].values)
    testdf['wvector'] = vectorizer.transform(traindf['clean_review'].values)
    
    traindf = traindf.drop(labels=['review', 'clean_review'], axis=1)
    testdf = testdf.drop(labels=['review', 'clean_review'], axis=1)

    print traindf.shape, testdf.shape, unlabeled_traindf.shape
    print traindf.columns
    print testdf.columns
    print unlabeled_traindf.columns

    xtrain = traindf['wvector'].values
    ytrain = traindf['sentiment'].values
    xtest = testdf['wvector'].values
    ytest = testdf['id'].values
    
    return 4*[None]

if __name__ == '__main__':
    #generate_biased_word_list()
    xtrain, ytrain, xtest, ytest = load_data(do_plots=True)

    print xtrain.shape, ytrain.shape, xtest.shape, ytest.shape