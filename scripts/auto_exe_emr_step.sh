#!/usr/bin/env bash

export PATH=/usr/local/bin/:$PATH
cd /home/hadoop/pyspark-etl
pipenv install
./build_dependencies.sh
./job_starter_janus.sh job_name
