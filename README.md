# MVP III

Latest Release: 3.1.8

Chanage Log: 2018/11/24
 - Fix CouchDB binary download to modify ownership to couchdb
 - Chanage ownership of log files to fix write problem
 - Add java script to index.html to give charts a unique name (Chrome caching problem fix)

Change Log: 2018/10/2
 - Added binary CouchDB to get around build problems
 - NOTE: Fuxton is not included in this binary

Change Log: 2018/09/24
 - add chmod to Startup.sh so logs always have the correct write permission

Change Log: 2018/09/21
  - Correct typo in Startup.sh

Change Log: 2018/07/05
  - Major change to the data JSON structure, this should be the final version
  - Removed SI7021 dependency on smbus, replaced with python-periphery
  - Added StartUp.py to check state of lights when reboot
  - Added HeartBeat.py to check CouchDB is up and running, or else will reboot automatically to reset the system
  - Removed web access to CouchDB
  - File and method name changes for consistency with the python code standard
  - Add standard Python logging
  - Removed retreival of geo information due to API deprecation

## Background 

Code and instructions for building the 'brain' of the controled environment hydroponics unit.
It is mostly a collection of python code that runs on a Raspberry Pi (or similar device).  See the OpenAg [forums](http://forum.openag.media.mit.edu/) for discussion and issues:

The MVP (Minimal Viable Product) is a simplified version of the MIT OpenAg Food Computer.

## Assumptions

 - Follows the instructions for building a Raspbian (Noobs) system.
 - Configure the environment (see below).  Turn VNC on, this is the easiest way to view multiple Raspberry Pis without needing separate keyboards and monitors for each.  You can view all the Raspberries on your local network through one Raspberry, or download VNC to a PC and access them through a PC.
 
 ## Building multiple MVPs
  - Once you have configured one SD card, from the main menu, use the Accessories/SD Card Copier to replicate the system for the other MVPs.  Just be sure to run the following so that a unique ID will be created for each MVP
  
  > python /home/pi/MVP/python/Environment.py

## Architecture:
The MVP brain is mostly python scripts involed using cron as the scheduler.  
Python and cron are built into the Raspbian OS, and the Raspberry library to manipulate GPIO pins is already loaded.

The Python is modular so additions and changes can easily be made without affecting the whole system.

- Scheduling Control (cron)
  - Image capture (Webcam.sh)
  - Log Sensors (LogSensors.py)
  - Turn lights On (LightOn.py)
  - Tirm lights Off (LightOff.py)
  - Check Temperature (Thermostat.py)
  - Refresh charts and picture for the UI (Render.sh)

CouchDB is the main data storage system, and will provide easy replication to the cloud in the future.

For more information on Cron [see:](https://docs.oracle.com/cd/E23824_01/html/821-1451/sysrescron-24589.html)

## Hardware Build:

**Fan:**
There are two fans, one for circulation and one for exhausting excess heat  These can run off the Raspberry's 5V or from a external 12V transformer

**Temperature/Humidity Sensor**
A SI7021 sensor on an I2C bus is used for temperature and humidity.  See the following for (instructions)[https://learn.adafruit.com/adafruit-si7021-temperature-plus-humidity-sensor/overview] on use and wiring.

**Webcam**
A standard USB camera is used for imaging (though the Raspberry Pi camera is an option).  See [here](https://www.raspberrypi.org/documentation/usage/webcams/) for instructions

**Relay**
A set of relays controled by GPIO pins is used to turn lights on and off (120V), and the exhaust fan (12V)

# Pin Assignment:
Refer to the following [diagram](https://docs.particle.io/datasheets/raspberrypi-datasheet/#pin-out-diagram) for the Raspberry's pin names:

Code follows the board number convention.

- '3 - SDA to SI7021'
- '5 - SCL to SI7021'
- '29 - light relay (relay #4)'
- '31 - (reserved for relay #3)'
- '33 - (reserved for relay #2)'
- '35 - GPIO13 fan control (relay #1)'


## Build Activities
### Assumptions:
1. NOOB install of Raspbian on Raspberry Pi
2. The Raspbian system has been configured 
    - for localization (time, timezone)
    - wifi is established and connected
    - I2C has been enabled
    - VNC is enabled for easy remote access
    - Screen resolution is set to Mode 16 for proper VNC viewing
    
2. 32G SD card to hold data
3. Sensors and relay are wired to the Pi.  If you try to run the code without sensors, some of it will error out (I/O Error, I noticed in the get_tempC() function).  This will ripple up to error out the cron job for LogSensor.py.
>
### Software Build

The build scripts are the documentation.  If you want to build things yourself, follow the scripts (/home/pi/MVP/setup).
The initial script is not in Github, as the script extracts the files from Github and changes the permissions on /home/pi/MVP/setup/releaseScript.sh.  From within your Raspberry Pi, cut and paste the following lines of code to to a text file and name is buildScript.sh.  Then change, the permissions to make it executable (from a File Manager, right click on the file and select "Properties".  In the "Permissions" tab, under "Execute", select "Anyone" and then click "OK").  Then open a terminal window and type in "<path to your file>/buildScript.sh.   
```
#!/bin/sh

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
VERSION=v3.1.8         # github version to work with
ZIP_DIR=3.1.8
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

########################################
echo "##### Relsease Specific Build #####"
# Complete the release specific build - this is the CouchDB extract

# Set permissions on script
chmod +x $TARGET/setup/releaseScript.sh || error_exit "Failure setting permissions on release script (check file exists in MVP/scripts)"
echo $(date +"%D %T") "Run permissions set"

# Run script in download
bash $TARGET/setup/releaseScript.sh || error_exit "Failure running release specific script"

# Clean up temporary extraction directory
rm -r $EXTRACT
echo $(date +"%D %T") $EXTRACT" removed"

echo $(date +"%D %T") "Install Complete"

```
## Manual Build
The following scripts (in /home/pi/MVP/scripts) can be run separately and in sequence if any errors are encountered.  Look within the scripts for single commands.

- releaseScript.sh calls the following scripts:
- releaseScript_DB.sh - installs the CouchDB code
- releaseScript_Local.sh - builds libraries, starts the database and initializes things
- releaseScript_Test.sh - calls Validate.sh to test the system
- releaseScript_Final.sh - configures start-up and loads cron

## To Do:
1. Add a watchdog to the Raspberry
2. Fix the cron email notifications

## Future Development (in no priority):
- GUI interface for setting persistent variables (could be local)
- Add a pump for when have to be away for a while and need to refill the reservoir.
- Light control for controlable LEDs
