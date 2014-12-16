#!/usr/bin/python

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
import itertools

from memory_profiler import profile

def clean_review_function(review):
    list_of_words = KaggleWord2VecUtility.review_to_wordlist(review, remove_stopwords=False)
    return ' '.join(list_of_words)

@profile
def average_vectors():
    labeledtrain_data = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    unlabeledtrain_data = pd.read_csv('unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    test_data = pd.read_csv('testData.tsv', header=0, delimiter='\t', quoting=3)

    print [ x['review'].size for x in [ labeledtrain_data , unlabeledtrain_data, test_data] ]


if __name__ == '__main__':
    average_vectors()
