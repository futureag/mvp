# Author: Howard Webb
# Data: 7/25/2017

# NOTE: this chart bins data into timestamp groups and uses multiple lines of data
# This is a test of combining temp, humidity and dewpoint

import pygal
import requests
import json
from DewPoint import getDewPoint
import pandas as pd
import math
from datetime import datetime

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getResults():
    header={"Content-Type":"application/json"}
    ts = str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow()))
#    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":{"$eq": "Success"}, "activity_type":{"$eq":"Environmental_Observation"}, "subject.name":{"$eq": "Air"},"subject.location.name": {"$eq": "Top"}, "$or":[{"subject.attribute.name": "Temperature"},{"subject.attribute.name": "Humidity"}], "fields":["start_date.timestamp", "subject.attribute.name", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":{"$eq": "Success"}, "activity_type":{"$eq":"Environmental_Observation"}, "subject.name":{"$eq": "Air"},"subject.location.name": {"$eq": "Top"}, "$or":[{"subject.attribute.name":"Humidity"}, {"subject.attribute.name":"Temperature"}]}, "fields":["start_date.timestamp", "subject.attribute.name", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}        
    url='http://localhost:5984/mvp_test/_find'
    return requests.post(url, json=payload, headers=header)

def cleanData(data):
    '''Flatten structure to three columns'''
    out=[]
    for row in data.json()["docs"]:
#        print row
        hold={}
        # bin the timestamp into 20 minute groups
        d=datetime.strptime(row["start_date"]["timestamp"], '%Y-%m-%d %H:%M:%S')
        d=d.replace(second=0, minute=int(math.floor(d.minute/20)))
        hold['timestamp']=str(d)
        hold["name"]=row["subject"]["attribute"]["name"]
        hold["value"]=row["subject"]["attribute"]["value"]
        out.append(hold)
    return out        

def getDewPointChart():
    data=getResults()
    buildChart(data)    


def buildChart(data):

    # Build dataframe from array
    df = pd.DataFrame.from_dict(data)
#    print df
    # label the columns
#    df.columns=['name', 'timestamp', 'value']
    # set the index
    df.set_index(['timestamp', 'name'])
#    print df.columns
    # Check for duplicates
    df = df.drop_duplicates(subset=['timestamp', 'name'])

    # Pivot the data by timestamp-bin with name groupings for columns
    df=df.pivot(index='timestamp', columns='name', values='value')
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

def test():
    data=getResults()
    if data.status_code == 200:
        print "Records: ", len(data.json()["docs"])
        data=cleanData(data)
  #      print data
        buildChart(data)
    else:
        print "No Data - Reason: ", data.reason

if __name__=="__main__":
    test()
