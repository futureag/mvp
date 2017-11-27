# MVP II

NOTE: 11/27/2017 - The build is going through beta testing, but almost ready for release.  The goal is to have a single script that will extract and build the entire environment on a 'stretch' release of Raspbian.

## Background 

Code and instructions for building the 'brain' of the controled environment hydroponics unit.
It is mostly a collection of python code that runs on a Raspberry Pi (or similar device).  See the OpenAg [forums](http://forum.openag.media.mit.edu/) for discussion and issues:

The MVP (Minimal Viable Product) is a simplified version of the MIT OpenAg Food Computer.

##Changes

  - Persistent variables are now in Python files (env.py and variable.py).  Shelf has gone away.
  - Cron is loaded from a file, no longer needing to be edited.

## Architecture:
The MVP brain is mostly python scripts involed using cron as the scheduler.  
Python and cron are built into the Raspbian OS, and the Raspberry library to manipulate GPIO pins is already loaded.

The Python is modular so additions and changes can easily be made without affecting the whole system.

- Scheduling Control (cron)
  - Image capture (webcam.sh)
  - Log Sensors (logSensors.py)
  - Turn lights On (setLightOn.py)
  - Tirm lights Off (setLightOff.py)
  - Check Temperature (adjustThermostat.py)
  - Refresh charts and picture for the UI (render.sh)

Data storage is in a csv formatted (without header) flat file (/home/pi/MVP/data/data.txt) - this will likely be deprected in the future.

For more information on Cron [see:](https://docs.oracle.com/cd/E23824_01/html/821-1451/sysrescron-24589.html)

## Hardware Build:

**Fan:**
There are two fans, one for circulation and one for exhausting excess heat  These can run off the Raspberry's 5V or from a external 12V transformer

**Temperature/Humidity Sensor**
A si7021 sensor on an I2C bus is used for temperature and humidity.  See the following for (instructions)[https://learn.adafruit.com/adafruit-si7021-temperature-plus-humidity-sensor/overview] on use and wiring.

**Webcam**
A standard USB camera is used for imaging (though the Raspberry Pi camera is an option).  See [here](https://www.raspberrypi.org/documentation/usage/webcams/) for instructions

**Relay**
A set of relays controled by GPIO pins is used to turn lights on and off (120V), and the exhaust fan (12V)

# Pin Assignment:
Refer to the following [diagram](https://docs.particle.io/datasheets/raspberrypi-datasheet/#pin-out-diagram) for the Raspberry's pin names:

Code follows the board number convention.

- '3 - SDA to si7021'
- '5 - SCL to si7021'
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
2. 32G SD card to hold data
3. Sensors and relay are wired to the Pi.  If you try to run the code without sensors, some of it will error out (I/O Error, I noticed in the getTempC() function).  This will ripple up to error out the cron job for logSensorData.py.
>
### Software Build

The build scripts are the documentation.  If you want to build things yourself, follow the scripts (MVP/setup).
The initial script is not in Github, as the script extracts the files from Github and changes the permissions on /home/pi/MVP/setup/releaseScript.sh.  If you do not have the script, you can run the following:

sudo apt-get update
mkdir -p /home/pi/MVP
mkdir -p /home/pi/unpack
wget https://github.com/webbhm/OpenAg-MVP-II/archive/master.zip -O mvp.zip
cd /home/pi/unpack
unzip -uo /home/pi/unpack/mvp.zip
cd /home/pi/unpack/OpenAg-MVP-II-master/MVP
mv * /home/pi/MVP
rm -r /home/pi/unpack
chmod +x /home/pi/MVP/setup/releaseScript.sh
/home/pi/MVP/setup/releaseScript.sh

releaseScript.sh calls the following scripts:
releaseScript_DB.sh - installs the CouchDB code
releaseScript_Local.sh - builds libraries, starts the database and initializes things
releaseScript_Test.sh - calls Validate.sh to test the system
releaseScript_Final.sh - configures start-up and loads cron

## To Do:
1. Add a watchdog to the Raspberry
2. Fix the cron email notifications

## Future Development (in no priority):
- GUI interface for setting persistent variables (could be local)
- Add a pump for when have to be away for a while and need to refill the reservoir.
- Light control for controlable LEDs
