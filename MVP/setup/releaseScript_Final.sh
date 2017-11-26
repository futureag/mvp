#!/bin/sh

# Libraries and Local
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

# Declarations
RED='\033[31;47m'
NC='\033[0m'

# Exit on error
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}


########### Final configuration changes ######################

echo "##### Start Final Configuration Changes #####"
# Change CouchDB for access on network
# modify /home/couchdb/etc/local.ini
COUCH=/home/couchdb/etc/local.ini
COUCH2=/home/pi/scripts/test2.txt
if grep -q "bind_address = 0.0.0.0" $COUCH;
then
	echo $COUCH" already has bind address"
else
	sed -e 's/;bind_address = 127.0.0.1/bind_address = 0.0.0.0/' $COUCH > $COUCH2
	mv -f $COUCH2 $COUCH
	echo "bind address added to "$COUCH
fi

# Set startup script
# Modify /etc/rc.local
RC_LOCAL=/etc/rc.local
RC_LOCAL2=/etc/rc.local2
if grep -q "startup.sh" $RC_LOCAL;
then
	echo $RC_LOCAL" already has startup command"
else
	sed -e 's/exit 0/\/home\/pi\/MVP\/scripts\/startup.sh'\\n\\'nexit 0/' $RC_LOCAL > $RC_LOCAL2
	mv -f $RC_LOCAL2 $RC_LOCAL
	echo "startup.sh added to "$RC_LOCAL
fi

# Load Cron
crontab /home/pi/scripts/MVP_cron.txt

echo $(date +"%D %T") "Final Config Complete"

