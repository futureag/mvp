import pygal
import couchdb
import pandas as pd

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getMultiTempChart():

    # Create the server object, defaults to localhost:5984
    server = couchdb.Server()
    # Get data database
    db = server['mvp_sensor_data']
    # Pull view document
    doc = db['_design/doc']
    # get view (function) from document
    func = doc['views']['attrib_bin']['map']
    # Run the query, order so most recent are first
    result = db.query(func, descending=True)
    # Reduce results to only temperature records
    res = result[['temperature', {}]:['temperature']]

    # Re-build the key based on binned dates, then build an output array of key values
    data =[]
    for row in res:
        row['key'][2]= row['key'][2][0] + ' ' + str(int(float(row['key'][2][1])/20))
        data.append(row['key'])


    # Build dataframe from array
    df = pd.DataFrame.from_dict(data)
    # label the columns
    df.columns=['attribute', 'name', 'timestamp', 'value']
    # set the index
    df.set_index(['timestamp', 'name'])

    # Check for duplicates
    #print(df.duplicated(subset=['timestamp', 'name']))
    df = df.drop_duplicates(subset=['timestamp', 'name'])
    #print('After ' + str(len(df.index)))


    # Pivot the data by timestamp-bin with name groupings for columns
    df=df.pivot(index='timestamp', columns='name', values='value')
    #print(df)

    #put in descending order
    d1=df.iloc[::-1]
    #print(d1)

    d2=d1.to_records()
    #print(d2)

    # Create the chart
    # Pull the temperature values from the rows and build a list, limit the list to 60 records
    ts=[row[0] for row in d2][:60]
    ambient_temp = [float(row[1]) for row in d2][:60]
    box_temp = [float(row[2]) for row in d2][:60]
    box_top_temp=[float(row[3]) for row in d2][:60]
    reservoir_temp=[float(row[4]) for row in d2][:60]

    # put back into ascending order
    ts.reverse()
    ambient_temp.reverse()
    box_temp.reverse()
    box_top_temp.reverse()
    reservoir_temp.reverse()

    #print(ts)

    #build chart
    line_chart = pygal.Line()
    line_chart.title = 'Temperature'
    line_chart.y_title="Degrees C"
    line_chart.x_title="Timestamp (hover over to display date)"
    line_chart.x_labels = ts
    line_chart.add('Ambient', ambient_temp)
    line_chart.add('Box Temp', box_temp)
    line_chart.add('Top Temp', box_top_temp)
    line_chart.add('Reservoir Temp', reservoir_temp)
    line_chart.render_to_file('/home/pi/MVP/web/temp_chart.svg')

getMultiTempChart() 
