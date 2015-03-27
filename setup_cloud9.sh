#!/bin/bash

sudo apt-get update
sudo apt-get install -y python-boto python-sklearn python-pandas 

sudo bash -c "echo deb ssh://ddboline@ddbolineathome.mooo.com/var/www/html/deb/trusty ./ > /etc/apt/sources.list.d/py2deb2.list"
sudo apt-get update

sudo apt-get install -y --force-yes python-nltk python-gensim

scp ddboline@ddbolineathome.mooo.com:~/nltk_data_full.tar.gz .
tar zxvf nltk_data_full.tar.gz
rm nltk_data_full.tar.gz

# if [[ $- != *i* ]]; then
#     # Shell is non-interactive.  Be done now
#     return
# fi

# python -m nltk -c "nltk.download()"
# python -c "import nltk; nltk.download()"
