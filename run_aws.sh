#!/bin/bash

DATE=`date +%Y%m%d%H%M%S`
N=1000
git pull
python my_model.py $N > temp.out 2> temp.err
tar zcvf temp_output_${N}_${DATE}.tar.gz temp.out temp.err *.csv
python save_to_s3.py temp_output_${N}_${DATE}.tar.gz
