"""
# Acuator for the exhaust fan
# Author: Howard Webb
# Date: 2/15/2017
"""

from env import env
from Relay import *
import time
from LogUtil import get_logger
from CouchUtil import saveList

class Fan(object):
    """Code associated with the exhaust fan"""

    relay = None
    target_temp = 0

    def __init__(self):
        self.logger = get_logger("Fan")
        self.logger.debug("initialize Fan object")
        self.relay = Relay()
        self.fan_relay = fanPin

    def set_fan_on(self):
        """Turn the fan on
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_fan_on")
        self.relay.set_state(self.fan_relay, ON)

    def set_fan_off(self):
        """Turn the fan off
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_fan_off")
        self.relay.set_state(self.fan_relay, OFF)

    def adjust(self, temp, test=False):
        """Determine if the fan should change state
            Args:
                temp: current temperature
                test: flag for testing
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In adjust")
        fan_state = self.relay.get_state(self.fan_relay)
        target_temp = env['thermostat']['setPoint']
        msg = "{} {} {} {} {} {}".format("Temp:", temp, " Target Temp:", target_temp, " Fan State:", fan_state)
        self.logger.info(msg)
        if temp > target_temp and not fan_state:
            self.set_fan_on()
            self.log_state("On", test)
            self.logger.debug("Turning fan on")

        elif temp <= target_temp and fan_state:
            self.set_fan_off()
            self.log_state("Off", test)
            self.logger.debug("Turning fan on")
        else:
            self.logger.debug("No change to fan")

    def log_state(self, value, test=False):
        """Send state change to database
           Args:
               value: state change
               test: flag for testing
           Returns:
               None
           Raises:
               None
        """
        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(['State_Change', '', 'Side', 'Fan', 'State', value, 'state', 'Fan', status_qualifier, ''])

def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    fan = Fan()
    print "Test"
    print "State: ", fan.relay.get_state(fan.fan_relay)
    print "Turn Fan On"
    fan.set_fan_on()
    print "State: ", fan.relay.get_state(fan.fan_relay)
    time.sleep(2)

    print "Turn Fan Off"
    fan.set_fan_off()
    print "State: ", fan.relay.get_state(fan.fan_relay)
    time.sleep(2)

    print "Adj 45"
    fan.adjust(45, True)
    print "State: ", fan.relay.get_state(fan.fan_relay)

    print "Adj 45"
    fan.adjust(45, True)
    print "State: ", fan.relay.get_state(fan.fan_relay)

    print "Adj 10"
    fan.adjust(10, True)
    print "State: ", fan.relay.get_state(fan.fan_relay)

    print "Adj 45"
    fan.adjust(45, True)
    print "State: ", fan.relay.get_state(fan.fan_relay)
    print "Done"

if __name__ == "__main__":
    test()


