from dependencies.spark import start_spark
from dependencies.janus import create_vertices
import json


def main():
    """Main ETL script definition.

    :return: None
    """
    # start Spark application and get Spark session, logger and config
    spark, log, config = start_spark(
        app_name='janus-create-orgs',
        files=['configs/etl_config.json'])
    # get the spark context
    sc = spark.sparkContext

    # log that main ETL job is starting
    log.warn('etl_job for vertices is up-and-running')

    # execute ETL pipeline: the orgs.txt file should be placed in path in hadoop
    data_rdd = sc.textFile('path/to/the/file', minPartitions=120)
    data_rdd.map(create_vertices).count()

    # log the success and terminate Spark application
    log.warn('test_etl_job is finished')
    spark.stop()
    return None


# entry point for PySpark ETL application
if __name__ == '__main__':
    main()
