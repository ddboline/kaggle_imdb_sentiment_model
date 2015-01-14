#!/bin/bash

DATE=`date +%Y%m%d%H%M%S`
if [ -z $1 ]; then
    N=1000
else
    N=$1
fi
git pull
time python my_model.py $N > temp.out 2> temp.err
tar zcvf temp_output_${N}_${DATE}.tar.gz temp.out temp.err *.csv
python save_to_s3.py temp_output_${N}_${DATE}.tar.gz
sudo poweroff
