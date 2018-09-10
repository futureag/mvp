'''
sudo pip install couchdb
sudo pip install pygal
sudo pip install json

# Temperature chart with data from CouchDB
# Author: Howard Webb
# Date: 3/5/2018
'''
import pygal
from couchdb import Server
import json
from datetime import datetime
from MVP_Util import UTCStrToLDT

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getResults(test=False):
    '''Run a Mango query to get the data'''
    ts = datetime.utcnow().isoformat()[:19]
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", "subject.name":"Air","subject.attribute.name": "Temperature"}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}    
    db_name = 'mvp_data'
    if test:
        print payload
    server = Server()
    db = server[db_name]
    return db.find(payload)
    
def buildChart(data):
    '''Build the chard from array data'''
    v_lst=[]
    ts_lst=[]
    for row in data:
#        print row["start_date"]["timestamp"], row["subject"]["attribute"]["value"]
        v_lst.append(float(row["subject"]["attribute"]["value"]))
        ts_lst.append(UTCStrToLDT(row["start_date"]["timestamp"]))


    line_chart = pygal.Line()
    line_chart.title = 'Temperature'
    line_chart.y_title="Degrees C"
    line_chart.x_title="Timestamp (hover over to display date)"
    #need to reverse order to go from earliest to latest
    ts_lst.reverse()
    line_chart.x_labels = ts_lst
    #need to reverse order to go from earliest to latest
    v_lst.reverse()
    line_chart.add('Air Temp', v_lst)
    line_chart.render_to_file('/home/pi/MVP/web/temp_chart.svg')

def buildTempChart():
    data=getResults(True)
    r_cnt=len(data)    
    if r_cnt>0:
        print "Records: ", r_cnt
        buildChart(data)
    else:
        print "No records selected"

def test():
    data=getResults()
    if data.status_code == 200:
        print "Records: ", len(data.json()["docs"])
        buildChart(data)
    else:
        print "No Data, Reason: ", data.reason

if __name__=="__main__":
    buildTempChart()

