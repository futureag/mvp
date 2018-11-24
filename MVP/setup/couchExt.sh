#!/bin/sh

# Install CouchDB from binary packaged with the MVP code
# Author: Howard Webb
# Date: 11/16/2017

# This script assumes you are running on your Raspberry Pi with (Stretch) Raspbian installed.
# Internet is connected
# You have configured the local environment (keyboard, timezone)
# You have adjusted the Pi Preferences (Configuration)
#   Enable the camera interface
#   Enable I2C
#   Enable VNC
#   Set screen resolution to Mode 16
#   Optionally (suggested) enable SSH, VCN and 1-Wire

# Get the release from Github
# Extract it to the proper directory
# Make the build script executable
# Run the release specific build script

###### Declarations #######################


RED='\033[31;47m'   # Define red text
NC='\033[0m'        # Define default text

EXTRACT=/home/pi/unpack    # Working directory for download and unzipping
TARGET=/home/pi/MVP       # Location for MVP
RELEASE=mvp             # Package (repository) to download 
VERSION=3.1.6
GITHUB=https://github.com/futureag/$RELEASE/archive/master.zip    # Address of Github archive

echo $EXTRACT
echo $TARGET
echo $RELEASE
echo $GITHUB

###### Error handling function ###################

PROGNAME=$(basename $0)

error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	tput sgr0
	exit 1
}

####### Start Build ######################

#add couchdb user and home
sudo useradd -d /home/couchdb couchdb

cd $EXTRACT/$RELEASE-$VERSION || error_exit "Failure moving to "$EXTRACT/$RELEASE-$VERSION""

# Move to proper directory
tar -xvzf couchdb.tar.gz
sudo mv couchdb /home
echo $(date +"%D %T") "CouchDB moved"

sudo chown -R couchdb:couchdb /home/couchdb
echo $(date +"%D %T") "Changed ownership of /home/couchdb"



