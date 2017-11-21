#!/bin/sh

# Part 2
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

# Exit on error
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

# Update what have
sudo apt-get update

# Build directories
mkdir -p $TARGET || error_exit "Failure to build MVP directory"
cd $TARGET
mkdir -p data
mkdir -p logs
mkdir -p pictures
echo $(date -u) "directories created"

# Install CouchDB

sudo chmod +x $TARGET/setup/couch.sh
$TARGET/setup/couch.sh || error_exit "Failure to install CouchDB"

################# Install Libraries ######################

# FS Webcam
sudo apt-get install fswebcam -y || error_exit "Failure to install fswebcam (USB Camera support)"
echo  $(date +"%D %T") "fswebcam intalled (supports USB camera"

# Used for charting
sudo pip install pygal|| error_exit "Failure to install pygal (needed for charting)"
echo  $(date +"%D %T") "pygal installed (used for charting)"

# Used for charting
sudo pip install pandas|| error_exit "Failure to install pandas (needed for charting)"
echo  $(date +"%D %T") "pandas installed (used for charting)"

# CouchDB python library
# http://pythonhosted.org/CouchDB

pip install  couchdb || error_exit "Failure to install CouchDB Python library"
echo  $(date +"%D %T") "CouchDB Python Library intalled"

# OpenCV library
# https://www.raspberrypi.org/forums/viewtopic.php?t=142700
# numpy dependency

sudo apt-get install python-numpy -y || error_exit "Failure to install numpy math library"
echo  $(date +"%D %T") "numpy Library intalled"

sudo apt-get install python-scipy -y || error_exit "Failure to install scipy science library"
echo  $(date +"%D %T") "scipy Library intalled"

sudo apt-get install ipython -y || error_exit "Failure to install ipython library"
echo  $(date +"%D %T") "ipython Library intalled"

# Not needed at this time
#sudo apt-get install libopencv-dev python-opencv -y || error_exit "Failure to install opencv (computer vision) library"
#echo  $(date +"%D %T") "opencv Library intalled"

##################################################
# Local stuff

# Make scripts executable
chmod +x $TARGET/scripts/render.sh
chmod +x $TARGET/scripts/webcam.sh
chmod +x $TARGET/scripts/startServer.sh
chmod +x $TARGET/scripts/stopServer.sh
chmod +x $TARGET/scripts/startCouchDB.sh

#Create variables
# Build the environment information

python $PYTHON/buildEnv.py || error_exit "Failure to build environment variables"
echo  $(date +"%D %T") "Environment variables built"

python $PYTHON/buildVariables.py || error_exit "Failure to build state variables"
echo  $(date +"%D %T") "State variables built"

echo  $(date +"%D %T") "Finished building CouchDB - try running"

nohup sudo -i -u couchdb /home/couchdb/bin/couchdb > /home/pi/MVP/logs/couchdb.log &

sleep 10   # wait for start before build databases

curl -X PUT http://localhost:5984/_users
curl -X PUT http://localhost:5984/_replicator
curl -X PUT http://localhost:5984/_global_changes

########### Database built, customize for MVP #############
 
# Build sensor database and view script
curl -X PUT http://localhost:5984/mvp_sensor_data

# To pull data from the database you need a view.  This is a specially named document in the data database.

curl -X PUT http://localhost:5984/mvp_sensor_data/_design/doc --upload-file /home/pi/MVP/setup/view.txt

########### Test the system ###################

# Build some data
python $PYTHON/logSensors.py || error_exit "Failure testing sensors"

# Test the system and build some data
python $PYTHON/testScript.py || error_exit "Failure of test script"

sudo bash /home/pi/MVP/scripts/render.sh
echo $(date +"%D %T") "System PASSED"

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

echo $(date +"%D %T") "Your MVP is now running - you should reboot the system"
#reboot
