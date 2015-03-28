#!/bin/bash

sudo apt-get update
sudo apt-get install -y python-boto python-sklearn python-pandas 

sudo bash -c "echo deb ssh://ddboline@ddbolineathome.mooo.com/var/www/html/deb/trusty ./ > /etc/apt/sources.list.d/py2deb2.list"
sudo apt-get update

sudo apt-get install -y --force-yes python-nltk python-gensim

CURDIR=`pwd`
cd $HOME
scp ddboline@ddbolineathome.mooo.com:~/nltk_data_full.tar.gz .
tar zxvf nltk_data_full.tar.gz
rm nltk_data_full.tar.gz
cd $CURDIR

scp ddboline@ddbolineathome.mooo.com:~/setup_files/build/kaggle_imdb_sentiment_model/imdb_sentiment_model.tar.gz
tar zxvf imdb_sentiment_model.tar.gz
rm imdb_sentiment_model.tar.gz
