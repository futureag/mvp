'''
Create demo data for testing
'''

from couchdb import Server
from datetime import datetime
from datetime import timedelta
from env import env
from LogUtil import get_logger

NBR_PLANTS = 6
TS = 0
FIELD = 1
ACTIVITY = 2
TRIAL = 3
PLOT = 4
SUBJECT = 5
ATTRIBUTE = 6
VALUE = 7
UNITS = 8
PARTICIPANT = 9
STATUS = 10
COMMENT = 11

url = 'http://webbhm:admin@localhost:5984'
db_name = 'mvp_data'

usr = 'webbhm'
pwd = 'admin'
server = Server()
#server.resource.credentials = (usr, pwd)
db = server[db_name]

logger = get_logger('CouchUtil')



def processEnv(row):
    '''
    Environment specific processing
    Args:
        doc: list of attributes, should be of format:
             [timestamp, field, activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
             participant may be a device string, or a list: ['person':'hmw']
    Returns:
        rec: json formatted record ready for the database
    Throws:
        None

    '''
    
    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}, 'location': row[PLOT]}
    rec['location'] = {'field':row[FIELD]}    
    return rec

def processState(row):
    '''
    State specific processing
    Args:
        doc: list of attributes, should be of format:
             [timestamp, field, activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
             participant may be a device string, or a list: ['person':'hmw']
    Returns:
        rec: json formatted record ready for the database
    Throws:
        None

    '''
    
    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}, 'location': row[PLOT]}
    rec['participant']= {'type':'device', 'name':row[PARTICIPANT]}    
    rec['location'] = {'field':row[FIELD]}    
    return rec
    
def processAgro(row):
    '''
    Agronomic specific processing
    Args:
        doc: list of attributes, should be of format:
             [timestamp, field, activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
             participant may be a device string, or a list: ['person':'hmw']
    Returns:
        rec: json formatted record ready for the database
    Throws:
        None

    '''

    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['sub-activity'] = row[PLOT]
    if len(row[SUBJECT]) > 0:
        rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}}
    rec['location'] = {'field':row[FIELD], 'trial':row[TRIAL]}
    return rec

def processPheno(row):
    '''
    Phenotype specific processing
    Args:
        doc: list of attributes, should be of format:
             [timestamp, field, activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
             participant may be a device string, or a list: ['person':'hmw']
    Returns:
        rec: json formatted record ready for the database
    Throws:
        None

    '''
    
    rec = buildCore(row)
    rec['activity_type'] = row[ACTIVITY]
    rec['subject'] = {'name':row[SUBJECT],'attribute':{'name':row[ATTRIBUTE], 'units':row[UNITS], 'value': row[VALUE]}}
    rec['location'] = {'field':row[FIELD], 'trial':row[TRIAL], 'plot':row[PLOT]}    
    return rec

def buildCore(row):
    '''
    Build the core of the json structure, common elements
    Args:
        row: list of activity 
             [timestamp, field, activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
             participant may be a device string, or a list: ['person':'hmw']
    Returns:
        rec: json formatted record ready for the database
    Throws:
        None

    '''

    rec = {}
    rec['start_date'] = {'timestamp':row[TS]}
    if isinstance(row[PARTICIPANT], list):
        rec['participant']= {'type':row[PARTICIPANT][0], 'name':row[PARTICIPANT][1]}
    else:
        rec['participant']= {'type':'device', 'name':row[PARTICIPANT]}
    if len(row[COMMENT]) == 0:
        rec['status'] = {'status':'Complete', 'status_qualifier': row[STATUS]}
    else:        
        rec['status'] = {'status':'Complete', 'status_qualifier': row[STATUS], 'comment':row[COMMENT]}
    return rec

def saveList(doc):
    '''
    Convert activity list to json structure and save to database
    This is the entry point for all other functions
    Args:
        doc: list of attributes, should be of format:
             [activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
             participant may be a device string, or a list: ['person':'hmw']
    Returns:
        rec: json formatted record ready for the database
    Throws:
        None

    '''
    # dictionary of activity types and specific processing functions
    proc = {'Environment_Observation':processEnv, 'State_Change':processState, 'Agronomic_Activity':processAgro, 'Phenotype_Observation':processPheno}    
    # add timestamp and field_id
    timestamp = datetime.utcnow().isoformat()[:19]
    doc.insert(0, env['field']['field_id'])
    doc.insert(0, timestamp)
    # Use activity type to route processing
    rec = proc[doc[2]](doc)
    saveRec(rec)
        
def saveRec(rec):
    '''
    Persist json structure to a database
    Args:
        rec: json structure
    Returns:
        id: document id
        rev: revision number of document
    Throws:
        None

    '''
    
#    print rec
    global db
    id, rev = db.save(rec)
    msg = "{} {}".format("Saved:", rec)
    logger.info(msg)

#    print id, rev

def test():
    print "Env Rec"
    rec = ['Environment_Observation','', 'Left_Side', 'Air', 'Temperature', 27.5, 'fairenheight', 'SI7021', 'Success', '']
    saveList(rec)
    print "Env Rec - Person"
    rec = ['Environment_Observation','', 'Reservoir', 'Nutrient', 'pH', 5.6, 'pH',['person','hmw'], 'Success', 'from bucket']
    saveList(rec)
    print "Agro Rec"
    rec = ['Agronomic_Activity', 'd3ca243b-2740-4557-87f9-c07be9d929ad', 'Planted', '', '', '', '', ['person','hmw'], 'Success', '']
    saveList(rec)
    print "Pheno Rec"
    rec = ['Phenotype_Observation', 'd3ca243b-2740-4557-87f9-c07be9d929ad', 1,'Plant','Weight', 125, 'g', ['person','hmw'], 'Success', '']
    saveList(rec)
    print "State Rec"
    rec = ['State_Change', '','Top', 'Light', 'state', 'ON', 'state', 'Light', 'Success', '']
    saveList(rec)

    
if __name__=="__main__":
    test()
