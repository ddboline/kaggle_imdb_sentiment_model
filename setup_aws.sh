#!/bin/bash

###
GITHUB_DIR="kaggle_imdb_sentiment_model"
GITHUB_REPO="https://github.com/ddboline/${GITHUB_DIR}.git"
SETUP_SCRIPT="setup_cloud9.sh"

# sudo -u ubuntu git clone ${GITHUB_REPO} /home/ubuntu/${GITHUB_DIR}
# cd /home/ubuntu/${GITHUB_DIR}
# sudo -u ubuntu sh ${SETUP_SCRIPT}

cd /home/ubuntu/${GITHUB_DIR}
sudo -u ubuntu git pull
sudo -u ubuntu sh run_aws.sh 2000
