#!/bin/sh

# Test Portion
# Version for building CouchDB
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
PYTHON=$TARGET/python

# Run the release specific build script

# Declarations
RED='\033[31;47m'
NC='\033[0m'

##### Error handling rouotine#####
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

########### Test the system ###################

echo "##### Start Testing #####"
# Build some data
python $PYTHON/LogSensors.py || error_exit "Failure testing sensors"

# Test the system and build some data
chmod +x $TARGET/setup/Validate.sh
$TARGET/setup/Validate.sh || error_exit "Validation test failure"
echo $(date +"%D %T") "System PASSED"

# Run startup to set lights
python $PYTHON/StartUp.py || error_exit "Failure setting lights"
echo $(date +"%D %T") "StartUp PASSED"


