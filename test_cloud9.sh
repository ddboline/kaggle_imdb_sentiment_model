#!/bin/bash

DATE=`date +%Y%m%d%H%M%S`
if [ -z $1 ]; then
    N=1000
else
    N=$1
fi

time python my_model.py $N > temp.out 2> temp.err

ssh ddboline@ddbolineathome.mooo.com "~/bin/send_to_gtalk imdb_sentiment_model_DONE"
