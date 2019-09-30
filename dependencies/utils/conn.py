from elasticsearch import Elasticsearch
import pymysql
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from dependencies.utils import config


curr_config = config.get_config()


def get_es_conn():
    """

    :return:
    """
    if curr_config['status'] == 'prod':
        es = Elasticsearch(curr_config['ES_HOST'], timeout=60, max_retries=3, retry_on_timeout=True, sniff_on_start=True,
                           sniff_on_connection_fail=True,)
    else:
        es = Elasticsearch(curr_config['ES_HOST'])
    return es


def get_db_conn():
    """

    :return:
    """

    db = curr_config['DB_NAME']
    conn = pymysql.connect(host=db['DB_HOST'], user=db['DB_USER'], passwd=db['DB_PASSWD'],
                           db=db['DB'], port=3306)
    return conn


def get_janus_traversal():
    """

    :return:
    """
    graph = Graph()
    conn_str = 'ws://' + curr_config['JANUS_HOST'] + ':8182/gremlin'
    connection = DriverRemoteConnection(conn_str, 'g')
    g = graph.traversal().withRemote(connection)
    return g


def get_status():
    return config.get_config()['STATUS']
