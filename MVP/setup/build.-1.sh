# Create empty directories

cd /home/pi/Hold/MVP
mkdir data
mkdir logs
mkdir pictures

# Components needed for 'brain'

sudo apt-get updatesudo apt-get install fswebcam

# Install CouchDB

sudo apt-get install couchdb -y

# Used for charting

sudo pip install pygal


echo "Edit /etc/couchdb/default.ini, then reboot"


 #Build 2

echo "Edit rc.local, then reboot"