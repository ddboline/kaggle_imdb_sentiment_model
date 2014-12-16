#!/usr/bin/python

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
import itertools
import nltk.data

from memory_profiler import profile


# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_review_function(review):
    print review
    list_of_sentences = KaggleWord2VecUtility.review_to_sentences( review , tokenizer , remove_stopwords=False )
    
    def clean_review_sentence(revsent):
        print revsent
        list_of_words = KaggleWord2VecUtility.review_to_wordlist(revsent, remove_stopwords=False)
        return ' '.join(list_of_words)
    
    return map( clean_review_sentence , list_of_sentences )

@profile
def average_vectors():
    labeledtrain_data = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    unlabeledtrain_data = pd.read_csv('unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    test_data = pd.read_csv('testData.tsv', header=0, delimiter='\t', quoting=3)

    print [ x['review'].size for x in [ labeledtrain_data , unlabeledtrain_data, test_data] ]

    sentences = map( clean_review_function , itertools.chain( labeledtrain_data['review'], unlabeledtrain_data['review'] ) )
    print len(sentences)

if __name__ == '__main__':
    average_vectors()
