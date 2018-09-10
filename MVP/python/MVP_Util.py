'''
A collection of miscellanious utilities convenient for the MVP
Author: Howard M. Webb
Date: 2018-09-08
'''

from datetime import datetime
import time

def UTCtoLocal(utc_datetime):
    '''
    Convert a UTC datetime object to local time datatime object
    Args:
        utc_datetime: datetime object in Grenich time
    Return:
        datetime object in Local time
    Raises:
        None
    '''
    now_timestamp = time.time()
    fts = datetime.fromtimestamp(now_timestamp)
    uts = datetime.utcfromtimestamp(now_timestamp)
    offset = fts - uts
    return utc_datetime + offset

def UTCStrToLocal(timestamp):
    '''
    Convert a UTC ISO formaatted timestamp local time string
    Args:
        timestamp: UTC timestamp
    Return:
        datetime object in Local time
    Raises:
        None
    '''
    # Cut to size in case there are micro-seconds
    tts =datetime.strptime(timestamp[:19], '%Y-%m-%dT%H:%M:%S')
    lt = UTCtoLocal(tts)
    return lt.isoformat()[:19]

def UTCStrToLDT(timestamp):
    '''
    Convert a UTC ISO formatted timestamp local datetime object
    Convenient for converting UTC dates to local for reporting
    Args:
        timestamp: UTC timestamp
    Return:
        datetime object in Local time
    Raises:
        None
    '''        
    tts =datetime.strptime(timestamp[:19], '%Y-%m-%dT%H:%M:%S')
    return UTCtoLocal(tts)

def test():
    utc = datetime.utcnow()
    print 'UTC', utc
    print UTCtoLocal(utc)
    ts = utc.isoformat()
    print "Timestamp", ts
    print UTCStrToLocal(ts)
    print UTCStrToLDT(ts)


if __name__=="__main__":
    test()
