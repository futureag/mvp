#!/bin/sh

# CouchDB Reset
# Delete mvp_data and rebuild it
# Author: Howard Webb
# Date: 10/02/2018

#######################################

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
# Delete database
curl -X DELETE http://localhost:5984/mvp_data

# Build sensor database
curl -X PUT http://localhost:5984/mvp_data

# Add views and indexes to support queries
curl -X PUT http://localhost:5984/mvp_data/_design/FullIdx --upload-file /home/pi/MVP/setup/FullIdx.json

curl -X PUT http://localhost:5984/mvp_data/_design/TimestampIdx --upload-file /home/pi/MVP/setup/TimestampIdx.json

curl -X PUT http://localhost:5984/mvp_data/_design/trial_view --upload-file /home/pi/MVP/setup/trial_view.json

echo $(date +"%D %T") "Finished rebuilding mvp_data"

