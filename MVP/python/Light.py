#Light Control
# Author: Howard Webb
# Date: 7/25/2017
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

from Relay import *
from LogUtil import get_logger
from CouchUtil import saveList

class Light(object):

    def __init__(self):
        self.r=Relay()
        self.logger = get_logger('Light')

    def set_on(self, test=False):
        "Check state and turn on if needed"
        if self.get_state()==0:
            self.r.set_on(lightPin, test)
            self.log_state("On", test)
            self.logger.debug('Light turned ON')            
        else:
            self.logger.debug('Light already ON - no change')
            
        
    def set_off(self, test=False):
        '''Check state and turn off if needed'''
        if self.get_state()==1:
            self.r.set_off(lightPin, test)
            self.log_state("Off", test)
            self.logger.debug('Light turned OFf')                        
        else:
            self.logger.debug('Light already OFF - no change')

    def get_state(self, test=False):
        '''Check the GPIO
    '''
        return self.r.get_state(lightPin)
        

    def log_state(self, value, test=False):
        """
        Create Environment Observation
    """
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        saveList(['State_Change','','Top', 'Lights', 'State', value, 'Lights', 'state', status_qualifier, ''])            

def test():
    """
    System test of the light object
    """
    lght=Light()
    
    print "Test Light"
    print "Light State: ", lght.get_state(True)
    print "Turn Light On"
    lght.set_on(True)
    print "Light State: ", lght.get_state(True)
    print "Turn Light Off"        
    lght.set_off(True)
    print "Light State: ", lght.get_state(True)
    print "Turn Light On"        
    lght.set_on(True)
    print "Light State: ", lght.get_state(True)
    print "Done"

if __name__=="__main__":
    test()    
                
    

