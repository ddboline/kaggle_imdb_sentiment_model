#!/usr/bin/python

import os
import pandas as pd
from KaggleWord2VecUtility import KaggleWord2VecUtility
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import itertools
import nltk.data

# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_review_function(review):
    list_of_sentences = KaggleWord2VecUtility.review_to_sentences( review , tokenizer , remove_stopwords=False )
    return list_of_sentences


def my_model(nfeatures=100, run_test_data=False):
    print 'nfeatures', nfeatures
    
    labeledtrain_data = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    unlabeledtrain_data = pd.read_csv('unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    test_data = pd.read_csv('testData.tsv', header=0, delimiter='\t', quoting=3)

    print 'labeledtrain_data.shape', labeledtrain_data.shape
    print 'unlabeledtrain_data.shape', unlabeledtrain_data.shape
    print 'test_data.shape', test_data.shape

    sentences = (pd.concat([labeledtrain_data['review'], unlabeledtrain_data['review']])).apply(clean_review_function)
    
    print len(sentences)

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

if __name__ == '__main__':
    nfeatures = 100
    for arg in os.sys.argv:
        try:
            nfeatures = int(arg)
        except ValueError:
            pass
    my_model(nfeatures, run_test_data=True)
