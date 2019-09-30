import json
import requests
from dependencies.utils import conn
from dependencies.utils import utils

# module level connections
es = conn.get_es_conn()
countries = utils.get_countries()


def get_sample():
    return None
