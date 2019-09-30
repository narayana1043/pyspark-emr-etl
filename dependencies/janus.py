from dependencies.utils import conn
from gremlin_python.process.graph_traversal import __
import json

g = conn.get_janus_traversal()


def create_vertices(org_txt):
    """

    :param:
    :return:
    """
    variable_x = json.loads(org_txt)
    g.addV('variable_x').property('my_id', variable_x['my_id']) \
        .property('property1', variable_x['property1']) \
        .property('property2', variable_x['property2']).next()
    return None
