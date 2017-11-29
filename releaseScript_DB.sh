#!/bin/sh

# CouchDB setup
# Semi-generic script to get and install github archive
# Author: Howard Webb
# Date: 11/16/2017
# Create directories
# Install libraries, including CouchDB and OpenCV
# Set up variables
# Test the System
# Load cron to automate

#######################################

TARGET=/home/pi/MVP
PYTHON=$TARTET/python

# Run the release specific build script

# Declarations
RED='\033[31;47m'
NC='\033[0m'

###### Error handler function #######
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

###### Release Modules #######

echo "##### Installing CouchDB #####"
# Uncomment to compile
#COUCH=couchBld.sh
# Uncomment to download
COUCH=couchDwn.sh 

#add couchdb user and home
sudo useradd -d /home/couchdb couchdb

# Install Database
chmod +x $TARGET/setup/$COUCH || error_exit "Failure setting permissions "$COUCH
echo $(date +"%D %T") "Run permissions set"
bash $TARGET/setup/$COUCH || error_exit "Failure building CouchDB"
echo $(date +"%D %T") "CouchDB Install"

# Create log directory
cd $TARGET
mkdir -p logs

# start database
chmod +x $TARGET/scripts/startCouchDB.sh
$TARGET/scripts/startCouchDB.sh

sleep 10   # wait for start before build databases

########### Database built, customize for MVP #############
 
# Build sensor database and view script
curl -X PUT http://localhost:5984/mvp_sensor_data

# To pull data from the database you need a view.  This is a specially named document in the data database.

curl -X PUT http://localhost:5984/mvp_sensor_data/_design/doc --upload-file /home/pi/MVP/setup/view.txt

echo  $(date +"%D %T") "Finished building CouchDB - now running"

exit 0