# Create empty directories

cd /home/pi/Hold/MVP
mkdir data
mkdir logs
mkdir pictures

# Copy old data to new loctions

cd /home/pi/MVP/pictures
cp /home/pi/Documents/MVP_Brain/pictures/*.jpg *.jpg
cd /home/pi/MVP/data
cp /home/pi/Documents/MVP_Brain/data.txt data.txt


#Put persistent variables in CouchDB, build the databse:

curl -X PUT http://localhost:5984/variable

# Add the variables

curl -X PUT http://localhost:5984/variable/priorFanOn "{'id': 'priorFanOn', 'value': true}"

curl -X PUT http://localhost:5984/variable/priorFanOn "{'id': 'targetTemp', 'value': 26}"