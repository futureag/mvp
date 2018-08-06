"""
# Get location information for the IP
Note: This is dependent upon two external services:
  ipstack.com (using my access_key)
  ipify.org - get host (router) ip
# Author: Howard Webb
# Data: 11/02/2017
"""

from requests import get
import json

def get_location():
  return {}
    """Call a service that gets geo info for the router location
        Args: None
        Returns: None
        Raises:
            None
    """        
    ip = get_host()

    send_url='http://api.ipstack.com/' + ip + '?access_key=dc5d110a00711bdeec659db986d3033a'
#    print send_url
    r=get(send_url)
#    print r
    j=json.loads(r.text)
# return location object
    return j

def get_host():
    ip = get('https://api.ipify.org').text
#    print 'My public IP address is:', ip
    return ip    

def test():
    """Call a service that gets geo info for the router location
        Args: None
        Returns: None
        Raises:
            None
    """        
    ip = get_host()
    print ip
    loc=get_location(ip)
    print(loc)

if __name__=="__main__":
    test()
