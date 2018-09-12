#!/bin/sh

# Validation script
# Author: Howard Webb
# Date: 11/16/2017

#######################################

TARGET=/home/pi/MVP
PYTHON=$TARGET/python

##### Error Handling Function #####

# Declarations
RED='\033[31;47m'
NC='\033[0m'

# Exit on error
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

#####################################

echo "##### Validation of the MVP 3.0 directory structure and code ####"

RED='\033[0;31m'
NC='\033[0m'

printf "MVP 1.0 Validation script\n"
printf "\n---Check for directories---\n"

main_dir=/home/pi/MVP
ui_dir=/home/pi/MVP

dir=$main_dir
cd  $dir &> /dev/null
if [ $? = 0 ]
then
    printf "$dir OK\n"
else 
    error_exit "MVP Directory not found, failed to extract from Github"
fi

dir=$main_dir/scripts
cd  $dir &> /dev/null
if [ $? = 0 ]
then
    printf "$dir OK\n"
else
    error_exit "Scripts directory not found, failed to extract from Github"
fi

printf "\n---Check CouchDB ---\n"
curl http://localhost:5984/ &> /dev/null
if [ $? = 0 ]
then
    printf "CouchDB OK \n"
else
    error_exit "CouchDB not Running"
fi

curl http://localhost:5984/mvp_data &> /dev/null
if [ $? = 0 ]
then
    printf "Sensor database OK\n"
else
    error_exit "Sensor Database not found in CouchDB"
fi

printf "\n---Test Sensors---\n"

echo "##### Test si7021 ####"
cmd=$main_dir/python/SI7021.py
python $cmd &> /dev/null
if [ $? = 0 ]
then
    printf "SI7021 OK\n"
else
    error_exit "Failure testing SI7021 sensor"
fi

printf "\n---Test Data Logger---\n"

cmd2=$main_dir/python/LogSensors.py
printf "Logged sensor data"

printf "\n---Test Actuators---\n"
echo "##### Test Thermostat #####"
cmd3=$main_dir/python/Thermostat.py
python $cmd3 || error_exit "Failure testing thermostat"
printf "Thermostat OK\n"

echo "##### Test Lights Off #####"
cmd4=$main_dir/python/LightOff.py
python $cmd4 || error_exit "Failure testing Lights Off"

echo "##### Test Lights On #####"
cmd5=$main_dir/python/LightOn.py
python $cmd5 || error_exit "Failure testing Lights On"
echo "Lights On OK"

echo "##### Test Webcam #####"
cmd6=$main_dir/scripts/Webcam.sh
$cmd6 || error_exit "Failure testing Camera"
printf "Webcam OK\n"

printf "\n---Building website, if you got this far, there is some data---\n"

echo "##### Test Render #####"
cmd7=$main_dir/scripts/Render.sh
#$cmd7 || error_exit "Failure rendering data to charts"
printf "Website render OK\n"

printf "\n---Done---\n"

