# Author: Howard Webb
# Data: 7/25/2017

# NOTE: this chart bins data into timestamp groups and uses multiple lines of data
# This is a test of combining temp, humidity and dewpoint

import pygal
from couchdb import Server
import json
from DewPoint import getDewPoint
import pandas as pd
import math
from datetime import datetime
from MVP_Util import UTCStrToLDT

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getResults():
#    header={"Content-Type":"application/json"}
    ts = datetime.utcnow().isoformat()[:19]
    payload={"selector":{"start_date.timestamp":{"$lt":ts},"status.status_qualifier":{"$eq": "Success"}, "activity_type":{"$eq":"Environment_Observation"}, "subject.name":{"$eq": "Air"}, "$or":[{"subject.attribute.name":"Humidity"}, {"subject.attribute.name":"Temperature"}]}, "fields":["start_date.timestamp", "subject.attribute.name", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}        
    server = Server()
    db_name = 'mvp_data'
    db = server[db_name]
    return db.find(payload)

def cleanData(data, test=False):
    '''Flatten structure to three columns'''
    out=[]
    for row in data:
#        print row
        hold={}
        # bin the timestamp into 20 minute groups
        # get only the first 19 characters of the timestamp
        d=UTCStrToLDT(row["start_date"]["timestamp"])
        d=d.replace(second=0, minute=int(math.floor(d.minute/20)))
        hold['timestamp']=str(d)
        hold["name"]=row["subject"]["attribute"]["name"]
        hold["value"]=row["subject"]["attribute"]["value"]
        out.append(hold)
    return out        

def buildChart(data, test=False):

    # Build dataframe from array
    df = pd.DataFrame.from_dict(data)
    df.set_index(['timestamp', 'name'])

    # Check for duplicates
    df = df.drop_duplicates(subset=['timestamp', 'name'])

    # Pivot the data by timestamp-bin with name groupings for columns
    df=df.pivot(index='timestamp', columns='name', values='value')
    if test:
        print df
#    print df

# Fill missing data with dummy value
    df=df.fillna(11.1)

    #put in descending order
    d1=df.iloc[::-1]

#pull off only 120 rows
#    d1 = d1[:][:120]

# Reorder again
    d1=d1.iloc[::-1]

    # Make numeric (except for dates) - this does not seem to be working
    d1.apply(pd.to_numeric, errors='ignore')

#    print d1

# Calculate dew point
    dp=[]
    for idx, row in d1.iterrows():
#        print row
        dp.append(getDewPoint(float(row['Temperature']), float(row['Humidity'])))
    d1['Dewpoint']=dp

# Clear index so all are columns
    d3=d1.reset_index()
    if test:
        print d3

#build chart
    line_chart = pygal.Line(range=(0, 40))
    line_chart.title = 'Temperature,Humidity and Dew Point'
    line_chart.y_title="Degrees C"
    line_chart.x_title="Timestamp (hover over to display date)"
    line_chart.x_labels = d3['timestamp']
    line_chart.add('Humidity', [float(row) for row in d3['Humidity']], secondary=True)
    line_chart.add('Temperature',[float(row) for row in d3['Temperature']])
    line_chart.add('Dewpoint', d3['Dewpoint'])
    line_chart.render_to_file('/home/pi/MVP/web/humidity_chart.svg')    

def getDewPointChart(test=False):
    data=getResults()
    r_cnt = len(data)
    if r_cnt>0:
        print "Records: ", r_cnt
        data=cleanData(data, test)
        buildChart(data, test)
    else:
        print "No Data"

def test():
    data=getResults()
    r_cnt = len(data)
    if r_cnt>0:
        print "Records: ", r_cnt
        data=cleanData(data, test)
        buildChart(data, test)
    else:
        print "No Data"

if __name__=="__main__":
    getDewPointChart()
