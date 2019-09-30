#!/bin/bash

sudo yum install -y git

# Copy ssh key from s3
aws s3 cp s3://interos-etl/scripts/s3_rsa ~/.ssh/
# chmod it
chmod 400 ~/.ssh/s3_rsa
# clone
GIT_SSH_COMMAND='ssh -i ~/.ssh/s3_rsa -o "StrictHostKeyChecking no"' git clone git@bitbucket.org:interos/pyspark-etl.git ~/pyspark-etl/

sudo easy_install-3.6 pip
sudo /usr/local/bin/pip3 install pipenv
sudo /usr/local/bin/pip3 install requests
sudo /usr/local/bin/pip3 install boto3
sudo /usr/local/bin/pip3 install pmdarima
sudo /usr/local/bin/pip3 install pandas