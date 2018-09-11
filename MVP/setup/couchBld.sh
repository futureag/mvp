# Code substantially taken from: http://andyfelong.com/2017/09/couchdb-2-1-on-raspberry-pi-raspbian-stretch/
# update packages & OS
cd
sudo apt-get update
sudo apt-get upgrade
 
# You can check the OS version
cat /etc/os-release 
 
# add Erlang Solutions repository and public key
wget http://packages.erlang-solutions.com/debian/erlang_solutions.asc
sudo apt-key add erlang_solutions.asc
sudo apt-get update
 
# install all build dependencies - note mutiple lines
sudo apt-get --no-install-recommends -y install \
build-essential pkg-config erlang libicu-dev \
libmozjs185-dev libcurl4-openssl-dev
 
#add couchdb user and home
sudo useradd -d /home/couchdb couchdb
sudo mkdir /home/couchdb
sudo chown couchdb:couchdb /home/couchdb
 
# Get source - need URL for mirror (see blog instructions)
wget http://www-eu.apache.org/dist/couchdb/source/2.2.0/apache-couchdb-2.2.0.tar.gz
 
# extract source and enter source directory
tar zxvf apache-couchdb-2.2.0.tar.gz 
cd apache-couchdb-2.2.0/
 
# configure build and make executable(s)
./configure
make release
 
#copy built release to couchdb user home directory
cd ./rel/couchdb/
sudo cp -Rp * /home/couchdb
sudo chown -R couchdb:couchdb /home/couchdb
#cd /home/couchdb/etc

# Clean up
sudo rm /home/pi/erlang_solutions.asc
sudo rm /home/pi/apache-couchdb-2.2.0.tar.gz
