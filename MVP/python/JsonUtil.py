"""
# Author: Howard Webb
# Date: 3/5/2018
# Create JSON structure for saving data and push to CouchDB, and other recorders

"""

from datetime import datetime
import json
from LogUtil import get_logger
from env import env
from reference import ref

def make_env_json(activity_type, subject, subject_location, attribute, value, participant, status_qualifier, timestamp=None, status='Complete', status_qualifier_reason='', comment='', validate=False):
    """Environmental Observation and State_Change records
           Args:
               activity_type: type of record
               subject: what being observed
               subject_location: where in the MVP the subject is located=
               attribute: what is being measured
               value: measurment amount
               participant: who or what made the observation
               status_qualifier: condition of action
               timestamp: when the action took place
               reason: if failed, the failure code
               comment: anything want to say
           Returns:
               jsn: JSON formatted record
           Raises:
               None
    """

    if validate:
        valid, reason = validate_environ_obsv(activity_type, subject, subject_location, attribute, value, participant, status, status_qualifier)
        if not valid:
            logger = get_logger("JsonUtil")
            msg = "{} {}".format("Failure Validating", reason)
            logger.Warning(msg)

    if timestamp is None:
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())
    jsn = {}
    jsn['activity_type'] = activity_type
    jsn['start_date'] = {'timestamp': timestamp}
    jsn['field'] = {'uuid': env['field']['uuid']}
    loc = {'name':subject_location}
    subj = {'name':subject, 'location':loc}
    attrib = {'name': attribute, 'value':value, 'units':get_env_units(attribute)}
    participant_type = get_participant_type(participant)
    part = {'name': participant, 'type':participant_type}
    jsn['participant'] = part
    status = {'status':'Complete', 'status_qualifier':status_qualifier, 'status_qualifier_reason': status_qualifier_reason, 'comment': comment}
    subj['attribute'] = attrib
    jsn['subject'] = subj
    jsn['status'] = status
    return jsn

def make_pheno_json(activity_type, plot_id, subject, attribute, value, participant, status_qualifier, timestamp=None, status='Complete', status_qualifier_reason='', comment='', validate=False):
    """Phenotype Observation and State_Change records
           Args:
               activity_type: type of record
               pot_id: location (pot/plant location) being observed
               subject: what being observed
               subject_location: where in the MVP the subject is located
               attribute: what is being measured
               value: measurment amount
               participant: who or what made the observation
               status_qualifier: condition of action
               timestamp: when the action took place
               reason: if failed, the failure code
               comment: anything want to say
           Returns:
               jsn: JSON formatted record
           Raises:
               None
    """

    if validate:
        valid,reason = validate_pheno_obsv(activity_type, plot_id, subject, attribute, value, participant, status, status_qualifier)
        if not valid:
            logger = get_logger("JsonUtil")
            msg = "{} {}".format("Failure Validating", reason)
            logger.Warning(msg)

    if timestamp is None:
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())
    jsn = {}
    jsn['activity_type'] = activity_type
    jsn['start_date'] = {'timestamp': timestamp}
    loc = {'field': env['field']['uuid'], 'plot_id':plot_id, 'use':env['field']['plots'][plot_id]['use']}
    subj = {'name':subject, 'location':loc}
    attrib = {'name': attribute, 'value':value, 'units':get_pheno_units(attribute)}
    participant_type = get_participant_type(participant)
    part = {'name': participant, 'type':participant_type}
    jsn['participant'] = part
    status = {'status':'Complete', 'status_qualifier':status_qualifier, 'status_qualifier_reason': status_qualifier_reason, 'comment': comment}
    subj['attribute'] = attrib
    jsn['subject'] = subj
    jsn['status'] = status
    return jsn

def validate_environ_obsv(activity_type, subject, subject_location, attribute, value, participant, status, status_qualifier):
    """Optional validation routine for checking Environmental Obsservations
           Args:
               activity_type: type of record
               subject: what being observed
               subject_location: where in the MVP the subject is located
               attribute: what is being measured
               value: measurment amount
               participant: who or what made the observation
               status_qualifier: condition of action
           Returns:
               valid: boolean flag of validation
               reason: reason for failure
           Raises:
               None
    """
    valid = True
    reason = ''
    if not subject in ref['Environment_Subject']:
        valid = False
        reason += (' Subject not found: '+subject)
    if not subject_location in ref['Field_Location']:
        valid = False
        reason += (' Field Loc not found: '+subject_location)
    if not attribute in ref['Environment_Attribute']:
        valid = False
        reason += (' Attribute not found: '+attribute)
    if not participant in ref['Participant']:
        valid = False
        reason += (' Participant not found: '+participant)
    if not status in ref['Status']:
        valid = False
        reason += (' Status not found: '+status)
    if not status_qualifier in ref['Status_Qualifier']:
        valid = False
        reason += (' Status_Qualifier not found: '+status_qualifier)
    return valid, reason

def validate_pheno_obsv(activity_type, plot_id, subject, attribute, value, participant, status, status_qualifier):
    """Optional validation routine for checking EPhenotype Obsservations
           Args:
               activity_type: type of record
               pot_id: location (pot/plant location) being observed
               subject: what being observed
               attribute: what is being measured
               value: measurment amount
               participant: who or what made the observation
               status_qualifier: condition of action
           Returns:
               valid: boolean of validation
               reason: reason for failure
           Raises:
               None
    """
    valid = True
    reason = ''
    if not subject in {'Plant', 'Leaf'}:
        valid = False
        reason += (' Subject not found: '+subject)
    if not plot_id in env['field']['plots']:
        valid = False
        reason += (' Plot_Id not found: '+plot_id)
    if not attribute in ref['Phenotype_Attribute']:
        valid = False
        reason += (' Attribute not found: '+attribute)
    if not status in ref['Status']:
        valid = False
        reason += (' Status not found: '+status)
    if not status_qualifier in ref['Status_Qualifier']:
        valid = False
        reason += (' Status_Qualifier not found: ' + status_qualifier)
    return valid, reason

def get_participant_type(participant):
    """lookup paraticipant type
           Args:
               participant: person or device
           Returns:
               participant_type
           Raises:
               None
    """
    if participant in ref['Participant']:
        return ref['Participant'][participant]['participant']['type']
    else:
        return 'Person'

def get_env_units(attribute):
    """lookup attribute value units
           Args:
               attribute: what measured
           Returns:
               units
           Raises:
               None
    """

    return ref['Environment_Attribute'][attribute]['units']

def get_pheno_units(attribute):
    """lookup attribute value units
           Args:
               attribute: what measured
           Returns:
               units
           Raises:
               None
    """
    return ref['Phenotype_Attribute'][attribute]['units']

def pretty_print(txt):
    """Dump json in nice format
           Args:
               txt: json string
           Returns:
               None
           Raises:
               None
    """
    print json.dumps(txt, indent=4, sort_keys=True)

def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    print "Test"
    print "Make Environment Observation"
    jsn = make_env_json('Environment_Observation', 'Air', 'Top', 'Temperature', 23.7, 'SI7021', 'Test', status='Complete', comment='self test', validate=True)
    pretty_print(jsn)
    print "Make Phenotype Observation"
    jsn = make_pheno_json('Phenotype_Observation', 1, 'Leaf', 'Area', 345.6, '13245', 'Test', status='Complete', comment='self test', validate=True)
    pretty_print(jsn)


if __name__ == "__main__":
    test()
