#!/bin/bash

#Script to start up CouchDB
#Author: Howard Webb
#Date: 7/15/2017

sudo touch /home/pi/MVP/logs/couchdb.log
sudo chmod a+r /home/pi/MVP/logs/couchdb.log
sudo chmod a+w /home/pi/MVP/logs/couchdb.log
sudo chmod a+x /home/pi/MVP/logs/couchdb.log

nohup sudo -i -u couchdb /home/couchdb/bin/couchdb &> /home/pi/MVP/logs/couchdb.log &

