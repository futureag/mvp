#!/bin/sh

# Download a pre-build of CouchDB
# Get the release from Github
# Extract it to the proper directory

########################################

# Declarations
RED='\033[31;47m'   # Define red text
NC='\033[0m'        # Define default text

EXTRACT=/home/pi/unpack    # Working directory for download and unzipping
TARGET=/home       # Location for MVP
RELEASE=CouchDB-2-1             # Package (repository) to download 
GITHUB=https://github.com/webbhm/$RELEASE/archive/master.zip    # Address of Github archive

echo $EXTRACT
echo $TARGET
echo $RELEASE
echo $GITHUB


#####################################
# Error handling function

PROGNAME=$(basename $0)

error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	tput sgr0
	exit 1
}

######################################

# Build target directory
#sudo mkdir -p $TARGET || error_exit "Failure to build target directory"
#echo $(date +"%D %T") $TARGET" built"


# Download CouchDB from GitHub
# Build extraction directory
sudo mkdir -p $EXTRACT || error_exit "Failure to build working directory"
echo $(date +"%D %T") "Directory built"
cd $EXTRACT|| error_exit "Failure moving to "$EXTRACT

# Download from Github
sudo wget $GITHUB -O $EXTRACT/couch2.zip || error_exit "Failure to download zip file"
echo $(date +"%D %T") " Github downloaded"

# Unzip the files, overwrite older existing files without prompting
sudo unzip -uo $EXTRACT/couch2.zip || error_exit "Failure unzipping file"
echo $(date +"%D %T") "Couch Github unzipped"

cd $EXTRACT

# Extract second layer zip file containing the tar file || error_exit "Failure unzipping inner couchdb.zip file"
sudo unzip -uo /home/pi/unpack/CouchDB-2-1-master/couch.zip || error_exit "Failure unzipping inner couchdb.zip file"

# UnTar the inner files, overwrite older existing files without prompting
sudo tar -xpf $EXTRACT/couchdb.tar --directory $TARGET || error_exit "Failure un-Tarring couchdb.tar"
echo $(date +"%D %T") "CouchDB files unpacked"

# change ownership (if not already done by tar)
sudo chown -R couchdb:couchdb /home/couchdb

# Clean up temporary extraction directory
sudo rm -r $EXTRACT
echo $(date +"%D %T") $EXTRACT" removed"

