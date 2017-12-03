#!/bin/sh

# Final configuration
# Version for building CouchDB
# Semi-generic script to get and install github archive
# Author: Howard Webb
# Date: 11/16/2017
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
COUCH2=/home/pi/test2.txt
if grep -q "bind_address = 0.0.0.0" $COUCH;
then
	echo $COUCH" already has bind address"
else
	sed -e 's/;bind_address = 127.0.0.1/bind_address = 0.0.0.0/' $COUCH > $COUCH2
	sudo mv -f $COUCH2 $COUCH
	echo "bind address added to "$COUCH
fi

echo "##### Set startup script ####"
# Modify /etc/rc.local
RC_LOCAL=/etc/rc.local
RC_LOCAL2=/home/pi/rc.local2
if grep -q "startup.sh" $RC_LOCAL;
then
	echo $RC_LOCAL" already has startup command"
else
	sed -e 's/exit 0/\/home\/pi\/MVP\/scripts\/startup.sh'\\n\\'nexit 0/' $RC_LOCAL > $RC_LOCAL2
	sudo mv -f $RC_LOCAL2 $RC_LOCAL
	echo "startup.sh added to "$RC_LOCAL
fi

echo "##### Load Cron ####"
CMD=$TARGET/scripts/cron.sh
chmod +x $CMD
$CMD

echo $(date +"%D %T") "Final Config Complete"

