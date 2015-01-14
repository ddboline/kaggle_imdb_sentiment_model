#!/bin/bash

sudo apt-get update
sudo apt-get install -y python-boto python-sklearn python-pandas python-pip
sudo pip install nltk memory_profiler gensim
if [[ $- != *i* ]]; then
    # Shell is non-interactive.  Be done now
    return
fi

# python -m nltk -c "nltk.download()"
python -c "import nltk; nltk.download()"
