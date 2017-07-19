import pygal
import requests
import json

def getHumidityChart():
        #Query the database for data
        #Order descending so the last rows are first
        #These modifiers get humidity and return only 60 rows
        r = requests.get('http://127.0.0.1:5984/mvp_sensor_data/_design/doc/_view/attribute_value?startkey=["humidity",{}]&endkey=["humidity"]&descending=true&limit=60')

        #Iterate over the rows and xtract the values and timestamp into Python lists
        v_lst = [float(x['value']['value']) for x in r.json()['rows']]
        ts_lst = [x['value']['timestamp'] for x in r.json()['rows']]

        #Build the chart from the lists
        line_chart = pygal.Line()
        line_chart.title = 'Humidity'
        line_chart.y_title="Percent"
        line_chart.x_title="Timestamp (hover over to display)"
        # reverse order for proper time sequence
        ts_lst.reverse()
        line_chart.x_labels = ts_lst

        #revrese order for proper time sequence
        v_lst.reverse()
        line_chart.add('Humidity', v_lst)

        #Save the chart as SVG to the web directory
        line_chart.render_to_file('/home/pi/MVP/web/humidity_chart.svg')

getHumidityChart()

