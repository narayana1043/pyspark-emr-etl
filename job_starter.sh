#!/usr/bin/env bash

mkdir -p ./data/graph-data

if [ $1 = "etl_neptune_vertices" ]; then
    # aws-cluster configured with 6 m3.2xlarge instances plus one master
    #        --num-executors 10 \ this option is ignored below
    spark-submit \
        --deploy-mode cluster \
        --master yarn \
        --driver-memory 12g \
        --executor-cores 3\
        --executor-memory 2g \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --conf "spark.dynamicAllocation.enabled=true" \
        --conf "spark.dynamicAllocation.executorIdleTimeout=60s" \
        --files configs/etl_config.json jobs/neptune/etl_vertices.py

    hadoop fs -getmerge /neptune/vertices/ ./data/vertices-intermediate.csv
    cat ./data/vertices_header.csv ./data/vertices-intermediate.csv > ./data/graph-data/vertices.csv
    rm ./data/vertices-intermediate.csv

elif [ $1 = "etl_neptune_edges" ]; then
    spark-submit \
        --deploy-mode cluster \
        --master yarn \
        --driver-memory 12g \
        --executor-cores 3 \
        --executor-memory 2g \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --conf "spark.dynamicAllocation.enabled=true" \
        --conf "spark.dynamicAllocation.executorIdleTimeout=60s" \
        --files configs/etl_config.json jobs/neptune/etl_edges.py

   hadoop fs -getmerge /neptune/edges/ ./data/edges-intermediate.csv
   cat ./data/edges_header.csv ./data/edges-intermediate.csv > ./data/graph-data/edges.csv
   rm ./data/edges-intermediate.csv

elif [ $1 = "pyspark" ]; then
    $SPARK_HOME/bin/pyspark \
        --master local[*] \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --files configs/etl_config.json
fi

find ./data/ -maxdepth 1 -type f -name '.*' -delete


