#!/usr/bin/python

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
import itertools
import nltk.data
from gensim.models import Word2Vec

from memory_profiler import profile


# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_review_function(review):
    list_of_sentences = KaggleWord2VecUtility.review_to_sentences(review, tokenizer, remove_stopwords=False)
    return list_of_sentences

@profile
def average_vectors():
    labeledtrain_data = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    unlabeledtrain_data = pd.read_csv('unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    test_data = pd.read_csv('testData.tsv', header=0, delimiter='\t', quoting=3)

    print [x['review'].size for x in [labeledtrain_data, unlabeledtrain_data, test_data]]

    sentences = map(clean_review_function, itertools.chain(labeledtrain_data['review'], unlabeledtrain_data['review']))
    print len(sentences)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)

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

    model.doesnt_match("man woman child kitchen".split())
    model.doesnt_match("france england germany berlin".split())
    model.doesnt_match("paris berlin london austria".split())
    model.most_similar("man")
    model.most_similar("queen")
    model.most_similar("awful")



if __name__ == '__main__':
    average_vectors()
