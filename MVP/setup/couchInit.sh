#!/bin/sh

# CouchDB setup
# Semi-generic script to get and install github archive
# Author: Howard Webb
# Date: 09/16/2018
# Final setup of CouchDB
# Build databases
# Load indexes and views

#######################################

# If this file is re-run, it will fail gracefully

TARGET=/home/pi/MVP
PYTHON=$TARTET/python

# Declarations
RED='\033[31;47m'
NC='\033[0m'

###### Error handler function #######
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

###### Customize #######

# Build user, etc
curl -X PUT http://localhost:5984/_users
curl -X PUT http://localhost:5984/_replicator
curl -X PUT http://localhost:5984/_global_changes

# Build sensor database
curl -X PUT http://localhost:5984/mvp_data

# Add views and indexes to support queries
curl -X PUT http://localhost:5984/mvp_data/_design/FullIdx --upload-file /home/pi/MVP/setup/FullIdx.json

curl -X PUT http://localhost:5984/mvp_data/_design/TimestampIdx --upload-file /home/pi/MVP/setup/TimestampIdx.json

curl -X PUT http://localhost:5984/mvp_data/_design/trial_view --upload-file /home/pi/MVP/setup/trial_view.json

echo $(date +"%D %T") "Finished building CouchDB - now running"

