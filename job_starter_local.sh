#!/usr/bin/env bash

mkdir -p ./data/graph-data-local/

if [[ $1 = "etl_neptune_vertices" ]]; then
    $SPARK_HOME/bin/spark-submit \
        --master local[*] \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --files configs/etl_config.json jobs/neptune/etl_vertices.py

    # hadoop fs -getmerge /neptune/vertices/ ./data/vertices-intermediate.csv
    # cat ./data/vertices_header.csv ./data/vertices-intermediate.csv > ./data/graph-data-local/vertices.csv
    # rm ./data/vertices-intermediate.csv

elif [[ $1 = "etl_create_transactions" ]]; then
    $SPARK_HOME/bin/spark-submit \
        --master local[*] \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --files configs/etl_config.json jobs/janus/etl_create_transactions.py

elif [[ $1 = "etl_create_supplier_of" ]]; then
    $SPARK_HOME/bin/spark-submit \
        --master local[*] \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --files configs/etl_config.json jobs/janus/etl_create_supplier_of.py

elif [[ $1 = "etl_janus_create_edge_located_in_hq" ]]; then
    $SPARK_HOME/bin/spark-submit \
        --master local[*] \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --files configs/etl_config.json jobs/janus/etl_create_edge_located_in_hq.py

elif [[ $1 = "etl_neptune_edges" ]]; then
    $SPARK_HOME/bin/spark-submit \
        --master local[*] \
        --packages 'org.apache.hadoop:hadoop-aws:2.7.2' \
        --py-files packages.zip \
        --files configs/etl_config.json jobs/neptune/etl_edges.py

   hadoop fs -getmerge /neptune/edges/ ./data/edges-intermediate.csv
   cat ./data/edges_header.csv ./data/edges-intermediate.csv > ./data/graph-data-local/edges.csv
   rm ./data/edges-intermediate.csv

elif [[ $1 = "etl_janus_orgs" ]]; then
    # aws-cluster configured with 6 m3.2xlarge instances plus one master
    #        --num-executors 10 \ this option is ignored below
     $SPARK_HOME/bin/spark-submit \
        --master local[8] \
        --py-files packages.zip \
        --files configs/etl_config.json jobs/janus/etl_create_orgs.py

elif [[ $1 = "etl_bls" ]]; then
    # aws-cluster configured with 6 m3.2xlarge instances plus one master
    #        --num-executors 10 \ this option is ignored below
     $SPARK_HOME/bin/spark-submit \
        --master local[*] \
        --py-files packages.zip \
        --files configs/etl_config.json jobs/hf/operations/v1/etl_bureau_of_labor_statistics.py

fi

find ./data/ -maxdepth 1 -type f -name '.*' -delete


