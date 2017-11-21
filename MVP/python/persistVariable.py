import couchdb

# Initialize the CouchDB with databases and populate the variables
#Author: Howard Webb
#Date: 7/6/2017

variable_db = 'variable'


def getVariable(variable):
    couch = couchdb.Server()
    db = couch[variable_db]
    doc = db[variable]
    return doc['value']
    
def setVariable(variable, value):
    couch = couchdb.Server()
    db = couch[variable_db]
    doc = db[variable]
    doc['value'] = value
    db.save(doc)

# Test code, uncomment to run
#putVariable('targetTemp', 26)
#putVariable('priorFanOn', False)
#print(str(getVariable('targetTemp')))
#print(str(getVariable('priorFanOn')))
