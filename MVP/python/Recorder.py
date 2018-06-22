"""
# Recorder - create JSON structure and route to one or more destinations
# Author: Howard Webb
# Date 6/18/2018

    To modify where data is stored (ie MQTT, CouchDB, SQL)
      Import a new recorder
      Add the recorder's function to the array in the record function
"""

from CouchDB import log_env_obsv_json
from JsonUtil import make_env_json

def record_env(activity_type, subject, subject_location, attribute, value, participant, status_qualifier, timestamp=None, status='Complete', status_qualifier_reason='', comment='', validate=False):
    """Create Environmental Observation JSON record and route to storage
           Args:
               activity_type: type of record
               subject: what being observed
               subject_location: where in the MVP the subject is located=
               attribute: what is being measured
               value: measurment amount
               participant: who or what made the observation
               status_qualifier: condition of action
               timestamp: when the action took place
               status_qualifier_reason: if failed, the failure code
               comment: anything want to say
               validate: flag to run validation test
           Returns:
               None
           Raises:
               None
    """

    jsn = make_env_json(activity_type, subject, subject_location, attribute, value, participant, status_qualifier)
    record_env_router(jsn)

def  mqtt_recorder(msg):
    """Dummy stand in for mqtt messaging
           Args:
               msg: what to send
           Returns:
               None
           Raises:
               None
    """
    print msg

def display_recorder(msg):
    """Dummy stand in for routing to screen
           Args:
               msg: what to send
           Returns:
               None
           Raises:
               None
    """
    print msg

def record_env_router(msg):
    """ Record Environmental Observation Router
        Uses a list to route records to various recorders
           Args:
               msg: what to send
           Returns:
               None
           Raises:
               None
    """
    recorders = [mqtt_recorder, display_recorder, log_env_obsv_json]
    for recorder in recorders:
        recorder(msg)

def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    record_env('State_Change', 'Lights', 'Top', 'State', 0, 'Lights', 'Test')

if __name__ == "__main__":
    test()
