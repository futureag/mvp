"""
# Check status on boot
# Check lights correctly set
# Make sure Solenoid is closed
"""

from Light import *
from env import env
from datetime import datetime
from datetime import timedelta
from LogUtil import get_logger

logger = get_logger()

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
    # Get times from env and split into components
    s=env['lights']['On']
    e=env['lights']['Off']
    state = determineState(s, e)
    l=Light()
    if state:
        l.set_on(test)
        pass
    else:
        l.set_off(test)
        pass
        
def determineState(start, end):
    ''' Determine if lights should be on or off'''
    global logger
    s=start.split(':')
    e=end.split(':')    
    # Munge date into times
    t=datetime.now()
    st=t.replace(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
    et=t.replace(hour=int(e[0]), minute=int(e[1]), second=int(e[2]))

    if st > et:
        # Night Light - roll to next day when lights go off
        et += timedelta(days=1)

    msg = "{} {} {} {}".format("Start Time: ", st, "End Time: ", et)
    logger.debug(msg)
    
    if (st < datetime.now()) and (et > datetime.now()):
        msg="Lights should be On"
        logger.debug(msg)            
        return True
    else:
        msg="Lights should be Off"
        logger.debug(msg)        
        return False


def test():
    determineState('06:30:00', '22:00:00')
    determineState('15:30:00', '08:30:00')    

if __name__=="__main__":
#    test()
    check()
     
