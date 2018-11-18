# Part 1
# Semi-generic script to get and install github archive
# Author: Howard Webb
# Date: 10/02/2018

# This script assumes you are running on your Raspberry Pi with (Stretch) Raspbian installed.
# Internet is connected
# You have configured the local environment (keyboard, timezone)
# You have adjusted the Pi Preferences (Configuration)
#   Enable the camera interface
#   Enable I2C
#   Enable VNC
#   Set screen resolution to Mode 16
#   Optionally (suggested) enable SSH, VCN and 1-Wire

# Get the release from Github
# Extract it to the proper directory
# Make the build script executable
# Run the release specific build script

###### Declarations #######################


RED='\033[31;47m'   # Define red text
NC='\033[0m'        # Define default text

EXTRACT=/home/pi/unpack    # Working directory for download and unzipping
TARGET=/home/pi/MVP       # Location for MVP
RELEASE=mvp             # Package (repository) to download
VERSION=v3.1.6         # github version to work with
ZIP_DIR=3.1.6
GITHUB=https://github.com/futureag/$RELEASE/archive/$VERSION.zip    # Address of Github archive

echo $EXTRACT
echo $TARGET
echo $RELEASE
echo $GITHUB

###### Error handling function ###################

PROGNAME=$(basename $0)

error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	tput sgr0
	exit 1
}

####### Start Build ######################
echo "##### Update Existing System #####"
sudo apt-get update
sudo apt-get upgrade -y

echo "##### Starting to build directories #####"
# Build target directory
mkdir -p $TARGET || error_exit "Failure to build target directory"
echo $(date +"%D %T") $TARGET" built"

echo "##### Starting download of MVP from Github #####"
# Download MVP from GitHub and install
# Build extraction directory
mkdir -p $EXTRACT || error_exit "Failure to build working directory"
echo $(date +"%D %T") "Directory built"
cd $EXTRACT

# Download from Github
wget -N $GITHUB -O $VERSION.zip || error_exit "Failure to download zip file"
echo $(date +"%D %T") "MVP Github downloaded"

cd $EXTRACT

# Unzip the files, overwrite older existing files without prompting
unzip -uo $EXTRACT/$VERSION.zip || error_exit "Failure unzipping file"
echo $(date +"%D %T") "MVP unzipped"

cd $EXTRACT/$RELEASE-$ZIP_DIR/MVP || error_exit "Failure moving to "$EXTRACT/$RELEASE"-"$ZIP_DIR

# Move to proper directory
mv * $TARGET
echo $(date +"%D %T") "MVP moved"

echo "##### Release Specific Build #####"
# Complete the release specific build - this is the CouchDB extract

# Set permissions on release script
chmod +x $TARGET/setup/releaseScript.sh || error_exit "Failure setting permissions on release script (check file exists in MVP/scripts)"
echo $(date +"%D %T") "Run permissions set on release script"

# Run script in download
bash $TARGET/setup/releaseScript.sh || error_exit "Failure running release specific script" 

# Add couchdb user to pi group
sudo usermod -a -G couchdb pi || error_exit "Failure adding pi user to couchdb group"


echo "##### Running Startup Script #####"

# Set permissions on install script
chmod +x $TARGET/scripts/Startup.sh || error_exit "Failure setting permissions on startup script (check file exists in MVP/scripts)"
echo $(date +"%D %T") "Run permissions set on startup script"

# Run startup script
bash $TARGET/scripts/Startup.sh || error_exit "Failure running startup script" 
echo "##### Running Render Script #####"

# Check couchdb is running
curl --silent --show-error --fail localhost:5984 || error_exit "Can't connect to couchdb"

# Run render script
sudo bash $TARGET/scripts/Render.sh || error_exit "Failure running startup script"

# Clean up temporary extraction directory
rm -r $EXTRACT
echo $(date +"%D %T") $EXTRACT" removed"

echo $(date +"%D %T") "Install Complete"
echo $(date +"%D %T") "Dashboard running on localhost:8000"