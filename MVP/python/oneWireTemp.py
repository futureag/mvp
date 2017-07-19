# Code modified from: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20
# This code requires modifying /boot/config.txt
# This code requires using modprobe (see above website)
# This is set up for multiple probes being read (the x in the functions)

import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

#for documentation, this is the sensor placement
boxTemp = 0
topTemp = 1
reservoirTemp = 2
ambientTemp = 3



def read_temp_raw(x):
    device_folder = glob.glob(base_dir + '28*')[x]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def getTempC(x):
    lines = read_temp_raw(x)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
#        temp_f = temp_c * 9.0 / 5.0 + 32.0
#        return temp_c, temp_f
        return temp_c
	
#tempC = getTempC()
#print ("Temp: %.2f C" %tempC)

#for x in range(0, 4):
#    tempC = getTempC(x)
#    print ("Temp: %.2f C" %tempC)



