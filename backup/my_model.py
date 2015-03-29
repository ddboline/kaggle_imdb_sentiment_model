#!/usr/bin/python

import os
import pandas as pd
from KaggleWord2VecUtility import KaggleWord2VecUtility
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

#master_word_dict = {}
#number_of_rows = 0
def clean_review_function(review):
    global master_word_dict, number_of_rows
    list_of_words = KaggleWord2VecUtility.review_to_wordlist(review, remove_stopwords=False)
    return ' '.join(list_of_words)

def my_model(nfeatures=100, run_test_data=False):
    print 'nfeatures', nfeatures

    labeledtrain_data = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)

    print 'labeledtrain_data.shape', labeledtrain_data.shape

    clean_labeledtrain_reviews = labeledtrain_data['review'].apply(clean_review_function)

    print clean_labeledtrain_reviews.shape

    vectorizer = CountVectorizer(analyzer = 'word', tokenizer = None,  preprocessor = None, stop_words = None, max_features = nfeatures)

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

    if run_test_data:
        train_data_features = vectorizer.fit_transform(clean_labeledtrain_reviews).toarray()

        forest = forest.fit(train_data_features, labeledtrain_data['sentiment'])

        test_data = pd.read_csv('testData.tsv', header=0, delimiter='\t', quoting=3)

        clean_test_reviews = test_data['review'].apply(clean_review_function)

        test_data_features = vectorizer.transform(clean_test_reviews).toarray()

        result = forest.predict(test_data_features)

        output = pd.DataFrame(data={'id': test_data['id'], 'sentiment': result})
        output.to_csv('my_model.csv', index=False, quoting=3)

if __name__ == '__main__':
    nfeatures = 100
    for arg in os.sys.argv:
        try:
            nfeatures = int(arg)
        except ValueError:
            pass
    my_model(nfeatures, run_test_data=True)
