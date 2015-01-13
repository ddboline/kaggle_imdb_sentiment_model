#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import the SDK
import boto
import uuid
import os
import time

# read aws credentials from file, then stick into global variables...
def read_keys():
    with open('%s/.aws/credentials' % os.getenv('HOME'), 'r') as f:
        for line in f:
            if 'aws_access_key_id' in line:
                aws_access_key_id = line.split('=')[-1].strip()
            if 'aws_secret_access_key' in line:
                aws_secret_access_key = line.split('=')[-1].strip()
    return aws_access_key_id, aws_secret_access_key

AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = read_keys()

AMIIDS = ['ami-98aa1cf0', 'ami-344e3c5c']

def save_to_s3(bname, kname, fname):
    s3 = boto.connect_s3(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    with open(fname, 'r') as infile:
        bucket = s3.get_bucket(bname)
        k = boto.s3.key.Key(bucket)
        k.key = kname
        k.set_contents_from_file(infile)

# def help_ec2_instance():
#     #ec2 = boto.connect_ec2(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
#     ec2 = boto.ec2.connect_to_region('us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
#     #print '\n'.join(x for x in dir(ec2) if 'instance' in x)
#     print help(ec2.run_instances)

if __name__ == '__main__':
    save_to_s3('kaggle_imdb_sentiment_model_ddboline', 'temp_output_20150113202234.tar.gz', 'temp_output_20150113202234.tar.gz')
