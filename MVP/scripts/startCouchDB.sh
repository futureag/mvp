#!/bin/bash

#Script to start up CouchDB
#Author: Howard Webb
#Date: 7/15/2017

nohup sudo -i -u couchdb /home/couchdb/bin/couchdb &>~/MVP/logs/couchdb.log &
