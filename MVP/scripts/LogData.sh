#!/bin/bash

timestamp="$(date +"%D %T")"
echo $(date +"%D %T") "Log Sensors"

#Log std JSON data
python /home/pi/MVP/python/LogSensors.py

