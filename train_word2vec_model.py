#!/usr/bin/python

import os
import csv
import gzip
import multiprocessing
from collections import defaultdict

import pandas as pd
import numpy as np

import nltk
from gensim.models import Word2Vec

from sklearn.feature_extraction.text import CountVectorizer

from KaggleWord2VecUtility import review_to_wordlist, review_to_sentences

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_review(review):
    list_of_sentences = review_to_sentences(review, tokenizer, remove_stopwords=False)
    return list_of_sentences

def train_word2vec_model(do_plots=False):
    traindf = pd.read_csv('labeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    unlabeled_traindf = pd.read_csv('unlabeledTrainData.tsv.gz', compression='gzip', delimiter='\t', header=0, quoting=3)
    
    review_list = traindf['review'].tolist() + unlabeled_traindf['review'].tolist()
    sentences = []

    pool = multiprocessing.Pool(4)
    for rsent in pool.imap_unordered(clean_review, review_list):
        sentences += rsent
    
    #traincleanreview = traindf['review'].apply(clean_review).tolist()
    #unlabeledcleanreview = unlabeled_traindf['review'].apply(clean_review).tolist()    
    #sentences = traincleanreview + unlabeledcleanreview    
    #print type(sentences[0])
    
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
    
    # It can be helpful to create a meaningful model name and
    # save the model for later use. You can load it later using Word2Vec.load()
    model_name = "300features_40minwords_10context"
    model.save(model_name)


if __name__ == '__main__':
    train_word2vec_model(do_plots=True)
