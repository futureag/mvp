# MVP II

NOTE: 7/20/2017 - This respository is is the process of being built.  Do not use at this time.

MVP II is the next upgrade of the Minimal Viable Product.  There are no significant functional changes, but a cleaning up of the directory structures and some file name changes.  This version merges the 'brain' and the UI portions of the MVP, and prepares the way for future enhancements.

## Background 

Code and instructions for building the 'brain' of the controled environment hydroponics unit.
It is mostly a collection of python code that runs on a Raspberry Pi (or similar device).  See the OpenAg [forums](http://forum.openag.media.mit.edu/) for discussion and issues:

The MVP (Minimal Viable Product) is a simplified version of the MIT OpenAg Food Computer.

##Changes

  - Persistent variables are now in CouchDB.  Shelf has gone away.

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

Data storage is in a csv formatted (without header) flat file (/home/pi/Documents/OpenAg-MVP/data.txt) - this will likely be deprected in the future.

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

- Download the zip file of code from [Github](https://github.com/webbhm/OpenAg-MVP-II).  Open a file browser and go to Downloads.  You should find the zip file (OpenAg-MVP-II_master.zip) here.
    - Right click on the file OpenAg-MVP-II-master.zip and select 'Extract Here', this will create a directory 'OpenAg-MVP-II-master that contains the files.
    - Click on the new directory (OpenAg-MVP-master) to open it
    - Drag the sub-directory 'MVP to /home/pi

### Full Build (upgrade steps are documented below)

NOTE:
Different builds/downloads of NOOBS seem to have different versions of Python set up as default, though both are likely installed, and the IDE for 2 and 3 are in the programming menu.  This code will work with 2 or 3, but you cannot switch back and forth.  Check which version is the default for your system and stick with it.  To find which version you default to, open a terminal window and type:

```python```

This will display the version number on the first line.  It will also put you into a Python command line - press CTL-D to exit it.

Open this file in your Raspberry Pi so you can cut and paste command line instructions and cron commands.  Highlight the line you want and use Ctl-C to copy it.  On the Terminal window click on "Edit" and select "Paste" (terminal windows don't use the standard Ctl-V to paste). 

It is recomented that you enter the following commands in a terminal window, as this helps you to get to know the system.  As a short-cut, you can run two build scripts to do the same work:

  - This first script will take you to the point where you need to edit CouchDB and reboot
> sudo bash /home/pi/MVP/setup/build-1.sh

- Individual setps follow:

#### Create empty directories for data output

  - Run the following from a terminal screen

> cd /home/pi/MVP
> mkdir data
> mkdir pictures
> mkdir logs

#### Add additional python libraries

- Update the software:

> sudo apt-get update

- Upgrade the software, this should default you to running Python 3

> sudo apt-get upgrade

- Install fswebcam
> sudo apt-get install fswebcam


- Make webcam.sh executable
    - from the file manager, go to the /home/pi/Documents/OpenAg-MVP directory
    - right click on webcam.sh and select Properties from the menu
    - select the Permissions tab, and on the Execute drop-down select 'Anyone' and hit 'OK'

  - Install charting software  

  - Install pygal
  
  > sudo pip install pygal

    
#### CouchDB Install

- build couchdb

> sudo apt-get install couchdb -y

The -y will accept all the questions with yes

Modify the default.ini initialization file to allow outside access

> sudo leafpad /etc/couchdb/default.ini

  - Click the "Search" then "Find" menu and type HTTPD, and click the "Find" button.
  - Under the HTTPD line,change binding address to: binding_address = 0.0.0.0
  - Click "File" and "Save", then exit the editor.
  - Reboot so this takes effect (From the Main menu, click "Shutdown" and on the sub-menu click "Reboot"

  - Add a database to hold the sensor output

> curl -X PUT http://localhost:5984/mvp_sensor_data

  - To pull data from the database you need a view.  This is a specially named document in the data database.  Run the following command from the command line:

> curl -X PUT http://localhost:5984/mvp_sensor_data/_design/doc --upload-file /home/pi/MVP/setup/view.txt

  - Put persistent variables in the database:

> curl -X PUT http://localhost:5984/variable
> curl -X PUT http://localhost:5984/variable/priorFanOn "{'id': 'priorFanOn', 'value': true}"
> curl -X PUT http://localhost:5984/variable/priorFanOn "{'id': 'targetTemp', 'value': 26}"

  - the above commands are in the second build script (MVP/setup/build-2.sh)

#### Configure the server:

This version runs the server in 'background' and will restart automatically every time the Raspberry is rebooted.  To do this you need to edit the file /etc/rc.local and add a line to start the server.  This needs to be done from the command line so that sudo is the 'owner' of the file.
  
  - Open a terminal window
  - Type:
    
  ```cd /etc```
    
  ```sudo leafpad rc.local```
  
     
  - scroll to just above the line that says "exit 0" (this should be the last line) and type:
    
  ```bash /home/pi/MVP/scripts/startServer.sh```
  
  - You now need to start the server.  Reboot your Raspberry Pi.
 
  - See the [instructions here](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md) for adding this shell script to the /etc/rc.local filehttps://www.maketecheasier.com/run-bash-commands-background-linux/), and [here](https://www.maketecheasier.com/run-bash-commands-background-linux/) for running background.

  - logs & errors will go to: ~/MVP_UI/server.log
  - To test the server, open a browser and type:
  
  ```localhost:8000```
  
  - To make this accessible over the web, and from a remote computer requires configuring your router to port forward to this machine on port 8000.  This is a longer topic and not covered here.

#### Crontab

- Open a terminal window and type:

> crontab -e

- Select the second editor option
- Scroll to the bottom of the file and cut and paste the following:

> */1 * * * * python /home/pi/MVP/python/adjustThermostat.py
> 0 6 * * * python /home/pi/MVP/python/setLightOn.py
> 30 22 * * * python /home/pi/MVP/python/setLightOff.py
> */20 * * * * python /home/pi/MVP/python/logSensors.py
> 3 6-22 * * * /home/pi/MVP/scripts/webcam.sh
> 1 * * * * /home/pi/MVP/scripts/render.sh

  - adjustThermostat checks the temperature and adjusts the fan every minute
  - setLightOn turns lights on at 6AM (change for your needs)
  - setLightOff turns lights off at 10:30PM (change for your needs)
  - logSensors logs the temperature and humidity every 20 minutes
  - webcam.sh takes an image every hour between 6am and 10pm; avoiding pictures when the lights are out.
  - render.sh moves the latest picture to the website and creates the charts

### Upgrade

  - NOTE: Before upgrading, make a back-up copy of your SD card.  Insert a card reader with an SD card into one of the Raspberry's USB ports.  From the main Raspberry menu select 'Accessories' then 'SD Card Copier'.  Click on the second drop-down ("Copy to Device") and select the SD card reader, then click 'Start'.  Accept the erasing of all data on the card.  This will take a while, but in case of any problems, you can simply put this backup card into the Raspberry and resume your old MVP software from where it left off.

  - The following steps (from the full build above) need to be performed.

  - Create empty directories for data output
  - Put persistent variables in CouchDB
  - Copy data files from old location

  - The following new steps need to be done to copy old data to new locations

> cd /home/pi/MVP/pictures
> cp /home/pi/Documents/MVP_Brain/pictures/*.jpg *.jpg
> cd /home/pi/MVP/data
> cp /home/pi/Documents/MVP_Brain/data.txt data.txt

  - The above upgrade steps can be done via the following script file:

> bash /home/pi/MVP/setup/upgrade.sh

  - Finally:

  - Edit crontab to change the directory locations (same as full install instructions)
  - Edit local.rc to change the directory location (same as full install instructions)

#### Final Clean-up

  - When you are comfortable with the running of the new setup, you can delete the old directories:

> sudo rm /home/pi/Documents/MVP_Brain
> sudo rm /home/pi/MVP_UI

  - Keep the /home/pi/python directory for working on your python code, but you are free to delete any code you do now want.	

## Test The New System

  - All should be up and running, but run the test script to make sure:
  - In your brower, enter the following:

  ```localhost:8000```

  = This should display the web page with the chart and picture.

The following will attempt to move the latest picture to the web directory and build the charts.  You should get some messages of what is done, but no errors.  Record and report any errors.

```/home/pi/MVP_UI/scripts/render.sh```

  - Double clicking on /home/pi/MVP_UI/web/index.html should bring it up in a browers.

Individual files can be loaded into Python (double click on the file) and the functions called from the command line.  Follow the basic Python code testing processes.
testScript.py will go through the main functions and run them.  There should be no exceptions, though you will see errors if the si7021 sensor is not correctly wired.

The commands in the crontab file can be run from a command line window:

> python /home/pi/python/adjustThermostat.py
> python /home/pi/python/setLightOn.py
> python /home/pi/python/setLightOff.py
> python /home/pi/python/logSensors.py
> /home/pi/Documents/OpenAg-MVP/webcam.sh

## Bill of Materials:
- Raspberry Pi
- 32G SD card
- SI7021 temperature/humidity sensor
- Wire or jumpers
- Relay

## To Do:
1. Add exception handling to the Python code
2. Add a watchdog to the Raspberry
3. Fix the cron email notifications
4. Automate the build process
    - file movement (clone process?)
    - crontab loading

## Future Development (in no priority):
- GUI interface for setting persistent variables (could be local)
- Add a paristolic pump for when have to be away for a while and need to refill the reservoir (Could be a separate board using Particle).
- Light control for controlable LEDs