"""
# Author: Howard Webb
# Date: 3/2/2018
# Simple manager for sending data to the CouchDB instance
"""

import json
import requests
from LogUtil import get_logger

def log_env_obsv_json(jsn):
    """Self test
           Args:
               jsn: json message to persist to the database
           Returns:
               status
           Raises:
               None
    """
    headers = {'content-type': 'application/json'}
    database = 'http://localhost:5984/mvp_test'
    req = requests.post(database, data=json.dumps(jsn), headers=headers)
    return get_status(req)

def get_status(msg):
    """Self test
       Need to add testing around the return message
           Args:
               jsn: json message to persist to the database
           Returns:
               status
           Raises:
               None
    """
    logger = get_logger("CouchDB")
    logger.info(msg)
    return True


def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    jsn = {'foo':'bar'}
    res = log_env_obsv_json(jsn)
    print res

if __name__ == "__main__":
    test()
