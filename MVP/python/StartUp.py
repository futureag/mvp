"""
# Check status on boot
# Check lights correctly set
# Make sure Solenoid is closed
"""

from Light import *
from env import env
from datetime import datetime
from LogUtil import get_logger

def check(test=False):
    """Main function to run what needs to be done at restart
    Args:
        test: flag for testing system
    Returns:
        None
    Raises:
        None
    """    
    checkLight(test)

def checkLight(test=False):
    """Check if lights should be on or off
    Args:
        test: flag for testing system
    Returns:
        None
    Raises:
        None
    """

    logger = get_logger()
    # Get times from env and split into components
    s=env['lights']['On']
    s=s.split(':')
    e=env['lights']['Off']
    e=e.split(':')
    # Munge date into times
    t=datetime.now()
    st=t.replace(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
    et=t.replace(hour=int(e[0]), minute=int(e[1]), second=int(e[2]))
    msg = "{} {} {} {}".format("Start Time: ", st, "End Time: ", et)
    logger.debug(msg)
    l=Light()
    msg="Lights should be On"
    if (st < datetime.now()) and (et > datetime.now()):
        l.set_on(test)
    else:
        msg="Lights should be Off"
        l.set_off(test)
    logger.debug(msg)

def test():
    """Self check function
    Args:
        None:
    Returns:
        None
    Raises:
        None
    """    

    print 'Test'
    print 'Time: ', datetime.now()
    s=env['lights']['On']
    s=s.split(':')
    e=env['lights']['Off']
    e=e.split(':')

    t=datetime.now()
    st=t.replace(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
    et=t.replace(hour=int(e[0]), minute=int(e[1]), second=int(e[2]))
    print "Start: ", st
    print "End: ", et    
    if (st < datetime.now()) and (et > datetime.now()):
        print "Lights should be on"
    else:
        print "Lights should be off"
        
             

if __name__=="__main__":
    check()
     
