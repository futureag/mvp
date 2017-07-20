# Create empty directories

cd /home/pi/MVP
mkdir data
mkdir logs
mkdir pictures

sudo apt-get update
sudo apt-get upgrade

# Components needed for 'brain'

sudo apt-get updatesudo apt-get install fswebcam

# Install CouchDB

sudo apt-get install couchdb -y

# Used for charting

sudo pip install pygal


echo "Edit /etc/couchdb/default.ini, then reboot"
