#!/usr/bin/python

import os
import csv
import gzip
import multiprocessing
from collections import defaultdict

import pandas as pd

from KaggleWord2VecUtility import review_to_wordlist, review_to_sentences

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

if __name__ == '__main__':
    generate_biased_word_list()
