from datetime import tzinfo, datetime
import requests
import json


#Output to file
def logData(name, status, attribute, value, comment):
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())
    logDB(timestamp, name, status, attribute, value, comment)
    
def logDB(timestamp, name, status, attribute, value, comment):
    log_record = {'timestamp' : timestamp,
            'name' : name,
            'status' : status,
            'attribute' : attribute,
            'value' : value,
            'comment' : comment}
    json_data = json.dumps(log_record)
    print(json.dumps(log_record, indent=4, sort_keys=True))
    headers = {'content-type': 'application/json'}
    r = requests.post('http://localhost:5984/mvp_sensor_data', data = json_data, headers=headers)
    print(r.json())

#Uncomment to test this function
#logData(_si7021, _Success, _temperature, '27', '')    
