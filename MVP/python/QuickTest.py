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




def test():
    print "Recorder Test"
    recorder_test()
    print "Test JSON Utility"
    json_test()
    print "Test CouchDB"
    couch_test()
    print "Test Relay"
    relay_test()
    print "Test Lights"
    light_test()
    print "Test Sensor Logging"
    sens_test()


if __name__=="__main__":
    test()    
