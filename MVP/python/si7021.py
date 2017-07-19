# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7021
# This code is designed to work with the SI7021_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SI7021_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus


def getTempC():
# SI7021 address, 0x40(64)
#		0xF3(243)	Select temperature NO HOLD master mode
    bus = smbus.SMBus(1)
    bus.write_byte(0x40, 0xF3)

    time.sleep(0.3)

# SI7021 address, 0x40(64)
# Read data back, 2 bytes, Temperature MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

# Convert the data
    cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    #fTemp = cTemp * 1.8 + 32
    print ("Temperature in Celsius is : %.2f C" %cTemp)
    #print ("Temperature in Fahrenheit is : %.2f F" %fTemp)
    return cTemp

def getHumidity():
    bus = smbus.SMBus(1)
    bus.write_byte(0x40, 0xF5)

    time.sleep(0.3)

# SI7021 address, 0x40(64)
# Read data back, 2 bytes, Humidity MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

# Convert the data
    humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
    print ("Relative Humidity is : %.2f %%" %humidity)
    return humidity

