# Author: Howard Webb
# Date: 3/2/2018
# Simple manager for sending data to the CouchDB instance

import requests
import json

def logEnvObsvJSON(jsn):
    headers = {'content-type': 'application/json'}
    r = requests.post('http://localhost:5984/mvp_test', data = json.dumps(jsn), headers=headers)
#    r = requests.post('http://python_user:TopFarmDog!!@openagcloud.media.mit.edu:5984/webbhm_env_obsv', data = json.dumps(jsn), headers=headers)
    return getStatus(r)

def getStatus(msg):
    print msg
    return True

    
def test():
    jsn={'foo':'bar'}
    res=logEnvObsvJSON(jsn)
    print res

if __name__=="__main__":
    test()    
