#!/bin/bash

sudo apt-get update
sudo apt-get install -y python-sklearn python-pandas
sudo pip install nltk memory_profiler gensim
python -m nltk
python -c "import nltk; nltk.download()"
