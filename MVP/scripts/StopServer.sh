#!/bin/bash

#find the process that is running the server
echo 'Find the server process'
ps aux | grep 'server_8000.py'|grep -v 'grep' 
echo 'Process number to kill'
ps aux | grep 'server_8000.py'|grep -v 'grep' | awk '{print $2}'


#kill the process
kill $(ps aux | grep 'server_8000.py'|grep -v 'grep' | awk '{print $2}')
echo 'Process killed'
#fuser -k 8000/tcp
