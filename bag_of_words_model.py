#!/usr/bin/python

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
from memory_profiler import profile

@profile
def bag_of_words_model():
    labeledtrain_data = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    #unlabeledtrain_data = pd.read_csv('unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    
    clean_labeledtrain_reviews = map( lambda r: ' '.join(KaggleWord2VecUtility.review_to_wordlist(r, remove_stopwords=False)) , labeledtrain_data['review'] )

    vectorizer = CountVectorizer(analyzer = 'word', tokenizer = None,  preprocessor = None, stop_words = 'english', max_features = 1000)

    train_review_subset_x = clean_labeledtrain_reviews[::2]
    train_review_subset_y = labeledtrain_data['sentiment'][::2]
    test_review_subset_x = clean_labeledtrain_reviews[1::2]
    test_review_subset_y = labeledtrain_data['sentiment'][1::2]
    
    train_data_features = vectorizer.fit_transform(train_review_subset_x).toarray()
    
    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit( train_data_features, train_review_subset_y )
    
    test_data_features = vectorizer.transform(test_review_subset_x).toarray()
    
    print forest.score( test_data_features , test_review_subset_y )
    
    #test_data = pd.read_csv('testData.tsv', header=0, delimiter='\t', quoting=3)
    #clean_labeledtrain_reviews = map( lambda r: KaggleWord2VecUtility.review_to_wordlist(r, remove_stopwords=False) , test_data['review'] )

if __name__ == '__main__':
    bag_of_words_model()
