# LUX Light Sensor
# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2561
# This code is designed to work with the TSL2561_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TSL2561_I2CS#tabs-0-product_tabset-2

#from periphery import I2C
import time
from I2CUtil import I2C, bytesToWord

# Device I2C address
path = "/dev/i2c-1"
addr = 0x39 #I2C Address
ctrl = 0x00 # Control register
timing = 0x01 # Timing register
cmd = 0x80 #128 Command bit
power_on = 0x03 #3
nominal_integration = 0x02

class TSL2561(object):
    
    def __init__(self):
      self._addr = addr
      self._path = path
      self._i2c = I2C(path, addr)

    def getChannels(self):
        '''Reads two light channels and calculates visible spectrum       
           Args:
               self:
           Returns:
               ir, full: infra-red and full spectrum reading
           Raises:
               None
        '''               
        # Select control register, 0x00(00) with command register, 0x80(128)
        #		0x03(03)	Power ON mode
        cmds = [ctrl|cmd, power_on]
        self._i2c.msg_write(cmds)

        cmds = [timing|cmd, nominal_integration]
        self._i2c.msg_write(cmds)        

        # need a pause here between sending the request and getting the data
#        print("Sleep")
        time.sleep(0.05)

        # Full Spectrum
        # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
        # ch0 LSB, ch0 MSB
        cmds = [cmd|0x0C]
        size = 2
        ms2 = self._i2c.msg_read(size, cmds)
#        ms2 = self._i2c.msg_read2(cmds, size)        
#        for ms in ms2:
#            print('-')
#            for dt in ms.data:
#                print("Data " + str(dt))
        full = bytesToWord(ms2[1].data[1], ms2[1].data[0])

        # Infra-red band
        # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
        # ch1 LSB, ch1 MSB
        size = 2
#        cmds = [cmd, 0x0E]
        cmds = [cmd|0x0E]        
#        cmds = [0x0E, cmd]        
        ms3 = self._i2c.msg_read(size, cmds)
#        ms3 = self._i2c.msg_read2(cmds, size)        
#        for ms in ms3:
#            print('-')
#            for dt in ms.data:
#                print("Data " + str(dt))

        ir = bytesToWord(ms3[1].data[1], ms3[1].data[0])

        if ir == None or full == None:
           return None, None
        else:
           return ir, full

    def getLux(self):
        '''Get calculated lux value
           Args:
               self:
           Returns:
               lux: visible light spectrum
           Raises:
               None
        '''               

        ir, full = self.getChannels()
        # Visible is full minus infra-read
        return full-ir
    
def test():
    # Output data to screen
    lx = TSL2561()
    ir, full = lx.getChannels()
    if full == None:
        print("Failure")
    print("Full Spectrum(IR + Visible) :%d lux" %(full))
    print("Infrared Value :%d lux" %ir)
    print("Visible Value :%d lux" %(full-ir))
    for x in range(0,13):
        print("LUX: " + str(lx.getLux()))
        time.sleep(1)
    print("Done")        

if __name__=="__main__":
    test()            

