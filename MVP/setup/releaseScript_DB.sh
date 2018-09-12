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
COUCH=couchBld.sh
# Uncomment to download
#COUCH=couchDwn.sh 

#add couchdb user and home
sudo useradd -d /home/couchdb couchdb

# Install Database
chmod +x $TARGET/setup/$COUCH || error_exit "Failure setting permissions "$COUCH
echo $(date +"%D %T") "Run permissions set"
$TARGET/setup/$COUCH || error_exit "Failure building CouchDB"
echo $(date +"%D %T") "CouchDB Install"

# Create log directory
cd $TARGET
mkdir -p /home/pi/MVP/logs

# start database
sudo chmod +x $TARGET/scripts/StartCouchDB.sh
$TARGET/scripts/StartCouchDB.sh

echo "##### Give CouchDB some time to start before proceeding #####"
sleep 45

echo "##### Finish Initianization of CouchDB #####"
sudo chmod +x $TARGET/setup/couchInit.sh || error_exit "Failure setting permissions "$COUCH
$TARGET/setup/couchInit.sh




exit 0
