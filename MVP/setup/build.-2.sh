curl -X PUT http://localhost:5984/mvp_sensor_data

# To pull data from the database you need a view.  This is a specially named document in the data database.

curl -X PUT http://localhost:5984/mvp_sensor_data/_design/doc --upload-file /home/pi/MVP/setup/view.txt

#Put persistent variables in CouchDB, build the databse:

curl -X PUT http://localhost:5984/variable

# Add the variables

curl -X PUT http://localhost:5984/variable/priorFanOn "{'id': 'priorFanOn', 'value': true}"

curl -X PUT http://localhost:5984/variable/priorFanOn "{'id': 'targetTemp', 'value': 26}"

# Finish up the web server controls

echo "Edit rc.local, then reboot"