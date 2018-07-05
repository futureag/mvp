# Temperature chart with data from CouchDB
# Author: Howard Webb
# Date: 3/5/2018

import pygal
import requests
import json
from datetime import datetime

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getResults(test=False):
    '''Run a Mango query to get the data'''
    ts = str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow()))
    header={"Content-Type":"application/json"}
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":{"$eq": "Success"}, "activity_type":{"$eq":"Environmental_Observation"}, "subject.name":{"$eq": "Air"},"subject.location.name": {"$eq": "Top"},"subject.attribute.name": {"$eq": "Humidity"}}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}    
    url='http://localhost:5984/mvp_test/_find'
    if test:
        print payload
    return requests.post(url, json=payload, headers=header)
    
def buildChart(data):
    '''Build the chard from array data'''
    v_lst=[]
    ts_lst=[]
    for row in data.json()["docs"]:
#        print row["start_date"]["timestamp"], row["subject"]["attribute"]["value"]
        v_lst.append(float(row["subject"]["attribute"]["value"]))
        ts_lst.append(row["start_date"]["timestamp"])


    line_chart = pygal.Line()
    line_chart.title = 'Humidity'
    line_chart.y_title="Percent Humidity"
    line_chart.x_title="Timestamp (hover over to display date)"
    #need to reverse order to go from earliest to latest
    ts_lst.reverse()
    line_chart.x_labels = ts_lst
    #need to reverse order to go from earliest to latest
    v_lst.reverse()
    line_chart.add('Humidity', v_lst)
    line_chart.render_to_file('/home/pi/MVP/web/humidity_chart.svg')

def buildTempChart():
    data=getResults(True)
    if data.status_code == 200:
        r_cnt=len(data.json()["docs"])    
        if r_cnt>0:
            print "Records: ", r_cnt
            buildChart(data)
        else:
            print "No records selected"
    else:
        print "No Data, Reason: ", data.reason

def test():
    data=getResults()
    if data.status_code == 200:
        print "Records: ", len(data.json()["docs"])
        buildChart(data)
    else:
        print "No Data, Reason: ", data.reason

if __name__=="__main__":
    buildTempChart()

