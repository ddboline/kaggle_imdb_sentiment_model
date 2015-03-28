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

biased_word_list = {}

def clean_review(review):
    list_of_words = review_to_wordlist(review, remove_stopwords=False)
    return ' '.join(list_of_words)
    #word_array = np.zeros(len(biased_word_list), dtype=np.int64)
    #for word in list_of_words:
        #if word in biased_word_list:
            #word_array[biased_word_list[word]] += 1
    #return word_array

def word_counting(inp):
    print inp
    exit(0)

def process_row(inp):
    return inp[0], inp[1]['sentiment'], review_to_wordlist(inp[1]['review'])

def generate_biased_word_list():
    ''' count words in training sample '''
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)

    word_count = defaultdict(int)
    good_words = defaultdict(int)
    bad_words = defaultdict(int)
    
    pool = multiprocessing.Pool(2)
    idx = 0
    for idx, sentiment, list_of_words in pool.imap_unordered(process_row, traindf.iterrows()):
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
    global biased_word_list
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    testdf = pd.read_csv('testData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    #unlabeled_traindf = pd.read_csv('unlabeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    word_count_df = pd.read_csv('word_count.csv.gz', compression='gzip')
    
    cond0 = word_count_df['count']>500
    cond1 = word_count_df['frac']>0.1
    biased_word_list = {w: n for n, w in enumerate(list(word_count_df[cond0 & cond1]['word']))}
    
    traincleanreview = traindf['review'].apply(clean_review)
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

if __name__ == '__main__':
    #generate_biased_word_list()
    xtrain, ytrain, xtest, ytest = load_data(do_plots=True)

    print xtrain.shape, ytrain.shape, xtest.shape, ytest.shape
