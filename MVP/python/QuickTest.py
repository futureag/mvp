""" Quick Test of MVP Python Code """


def json_test():
    from JsonUtil import test as j_test
    j_test()

def couch_test():
    from CouchDB import test as c_test
    c_test()

def relay_test():
    from Relay import test as r_test
    r_test()

def light_test():
    from Light import test as l_test
    l_test()

def sens_test():
    from logSensors import test as s_test
    s_test()

def recorder_test():
    from Recorder import test as rec_test
    rec_test()

def fan_test():
    from Fan import test as fan_test

def thermostat_test():
    from Thermostat import test as therm_test

def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """    
    print "\nRecorder Test"
    recorder_test()
    print "\nTest JSON Utility"
    json_test()
    print "\nTest CouchDB"
    couch_test()
    print "\nTest Relay"
    relay_test()
    print "\nTest Lights"
    light_test()
    print "\nTest Sensor Logging"
    sens_test()
    print "\nTest Fan"
    fan_test()
    print "Test Thermostat"
    thermostat_test()


if __name__=="__main__":
    test()    
