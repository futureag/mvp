#!/bin/bash

#Script to start up the web server
#This should be placed in a startup directory so it runs every time the Pi is booted
#There are several ways to do this, but the following is one
#https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
#Author: Howard Webb
#Date: 7/15/2017

#NOTE: The server must be started from the directory from which files are to be served
sudo touch /home/pi/MVP/logs/server.log
sudo chmod a+r /home/pi/MVP/logs/server.log
sudo chmod a+w /home/pi/MVP/logs/server.log
sudo chmod a+x /home/pi/MVP/logs/server.log
cd /home/pi/MVP/web
nohup python /home/pi/MVP/python/server_8000.py &/home/pi/MVP/logs/server.log &
