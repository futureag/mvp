# Get location information for the IP
# Author: Howard Webb
# Data: 11/02/2017

import requests
import json

def getLocation():
    send_url='http://freegeoip.net/json'
    r=requests.get(send_url)
    j=json.loads(r.text)
# return location object
    return j

def test():
    loc=getLocation()
    print(loc)

if __name__=="__main__":
    test()
