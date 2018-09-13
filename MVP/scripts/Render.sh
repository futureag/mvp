#!/bin/bash

#This script renders the web data files
#Invoke this via cron on a regular (hourly?) basis to refresh the data
#Author: Howard Webb
#Date: 7/5/2017

echo "Move latest webcam image"

#Modify this path if you move the webcam image directory
pic_dir="/home/pi/MVP/pictures/"
web_dir="/home/pi/MVP/web/"
python_dir="/home/pi/MVP/python/"

#Pipe ls of the webcam directory from most recent to latest
# Then clip off only the last line
# Finally trim the string to just the name and store in the variable (File Name)
FN=$(ls -ltr "$pic_dir" | tail -1 | awk '{print $NF}')

#Check that got what expected
echo "$pic_dir$FN"

#Finally copy this file to the output web directory
#Since will be overwriting, need to confirm with "yes"
yes | cp "$pic_dir$FN" "$web_dir"image.jpg


#create the temperature graph
echo "Build temperature graph"
python "$python_dir"TempChart.py

echo "Build humidity graph"
#create the humidity graph
python "$python_dir"HumidityChart.py
