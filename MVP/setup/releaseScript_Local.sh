#!/bin/sh

# Libraries and Local
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

################# Install Libraries ######################
# Make sure back to home directory
cd /home/pi

echo "##### Install Libraries #####"
# FS Webcam
sudo apt-get install fswebcam -y || error_exit "Failure to install fswebcam (USB Camera support)"
echo  $(date +"%D %T") "fswebcam intalled (supports USB camera"

# Needed for I2C
sudo pip install python-periphery || error_exit "Failure to install python-periphery (needed for si7021 temp sensor)"
echo  $(date +"%D %T") "python-periphery installed (needed for si7021 temp sensor)"

# Used for charting
sudo pip install pygal|| error_exit "Failure to install pygal (needed for charting)"
echo  $(date +"%D %T") "pygal installed (used for charting)"

pip install  couchdb || error_exit "Failure to install CouchDB Python library"
echo  $(date +"%D %T") "CouchDB Python Library intalled"

# https://www.raspberrypi.org/forums/viewtopic.php?t=142700
# numpy dependency

sudo apt-get install python-numpy -y || error_exit "Failure to install numpy math library"
echo  $(date +"%D %T") "numpy Library intalled"

sudo apt-get install python-scipy -y || error_exit "Failure to install scipy science library"
echo  $(date +"%D %T") "scipy Library intalled"

sudo apt-get install ipython -y || error_exit "Failure to install ipython library"
echo  $(date +"%D %T") "ipython Library intalled"

##################################################
# Local stuff

echo "##### Build directories #####"
mkdir -p $TARGET || error_exit "Failure to build MVP directory"
cd $TARGET
mkdir -p data
mkdir -p pictures
echo $(date -u) "directories created"

echo "##### Start Local file changes #####"
# Make scripts executable
chmod +x $TARGET/scripts/*.sh

#Create variables
# Build the environment information

python $PYTHON/Environment.py || error_exit "Failure to initialize MVP"
echo  $(date +"%D %T") "MVP Initialized"

echo "##### Make Pi owner of MVP ####"
sudo chown -R pi:pi /home/pi/MVP

echo "##### Start Web Server - needed for Testing ####"
CMD=/home/pi/MVP/scripts/StartServer.sh
chmod +x $CMD
$CMD
echo $(date +"%D %T") "Web Server Started"

exit 0
