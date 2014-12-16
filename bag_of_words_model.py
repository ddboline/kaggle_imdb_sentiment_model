#!/usr/bin/python

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
import nltk.data

def clean_review_function(review):
    list_of_words = KaggleWord2VecUtility.review_to_wordlist(review, remove_stopwords=False)
    return ' '.join(list_of_words)

from memory_profiler import profile

@profile
def bag_of_words_model():
    labeledtrain_data = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
    #unlabeledtrain_data = pd.read_csv('unlabeledTrainData.tsv', header=0, delimiter='\t', quoting=3)

    clean_labeledtrain_reviews = map(clean_review_function, labeledtrain_data['review'])


    vectorizer = CountVectorizer(analyzer = 'word', tokenizer = None,  preprocessor = None, stop_words = None, max_features = 1000)


    train_review_subset_x = clean_labeledtrain_reviews[::2]
    train_review_subset_y = labeledtrain_data['sentiment'][::2]
    test_review_subset_x = clean_labeledtrain_reviews[1::2]
    test_review_subset_y = labeledtrain_data['sentiment'][1::2]

    train_data_features = vectorizer.fit_transform(train_review_subset_x).toarray()


    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit(train_data_features, train_review_subset_y)

    test_data_features = vectorizer.transform(test_review_subset_x).toarray()


    print forest.score(test_data_features, test_review_subset_y)

    del train_review_subset_x, train_review_subset_y, test_review_subset_x, test_review_subset_y, test_data_features, train_data_features


    train_data_features = vectorizer.fit_transform(clean_labeledtrain_reviews).toarray()


    forest = forest.fit(train_data_features, labeledtrain_data['sentiment'])


    test_data = pd.read_csv('testData.tsv', header=0, delimiter='\t', quoting=3)


    clean_test_reviews = map(clean_review_function, test_data['review'])


    test_data_features = vectorizer.transform(clean_test_reviews).toarray()


    result = forest.predict(test_data_features)

    output = pd.DataFrame(data={'id': test_data['id'], 'sentiment': result})
    output.to_csv('bag_of_words_model.csv', index=False, quoting=3)

if __name__ == '__main__':
    bag_of_words_model()
