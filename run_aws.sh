#!/bin/bash

DATE=`date +%Y%m%d%H%M%S`
git pull
python my_model.py 100 > temp.out 2> temp.err
tar zcvf temp_output_${DATE}.tar.gz temp.out temp.err *.csv
scp temp_output_${DATE}.tar.gz ddboline@ddbolineathome.mooo.com:~/setup_files/build/kaggle_imdb_sentiment_model/
