#!/bin/sh

# CouchDB Initialization
# Semi-generic script to get and install github archive
# Author: Howard Webb
# Date: 11/16/2017
# Build databases and views

# If this file is re-run, these functions will fail (gracefully) since the database is already there
#######################################

TARGET=/home/pi/MVP
PYTHON=$TARTET/python
########### Database built, customize for MVP #############
 
# Build user, etc
curl -X PUT http://localhost:5984/_users
curl -X PUT http://localhost:5984/_replicator
curl -X PUT http://localhost:5984/_global_changes

# Build sensor database and view script
curl -X PUT http://localhost:5984/mvp_sensor_data

# To pull data from the database you need a view.  This is a specially named document in the data database.

curl -X PUT http://localhost:5984/mvp_sensor_data/_design/doc --upload-file /home/pi/MVP/setup/view.txt

echo  $(date +"%D %T") "Finished building CouchDB - now running"