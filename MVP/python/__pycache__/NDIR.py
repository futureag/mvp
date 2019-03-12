# CO2 Sensor
# Author: Howard Webb
# Date: 8/10/2017
# Code taken and modified from
# https://github.com/SandboxElectronics/NDIR/tree/master/NDIR_RasPi_Python
# MH-Z16 CO2 sensor with an I2C/UART interface (IC SC16I5705)
# Note: the timing between the Raspberry clock and the interface clock occasionally throws an error
#  This is somewhat mitigated by adding some sleep in the register read code.

import smbus
import time

class Sensor():
    cmd_measure = [0xFF,0x01,0x9C,0x00,0x00,0x00,0x00,0x00,0x63]
    ppm         = 0
    
    IOCONTROL   = 0X0E << 3
    FCR         = 0X02 << 3
    LCR         = 0X03 << 3
    DLL         = 0x00 << 3
    DLH         = 0X01 << 3
    THR         = 0X00 << 3
    RHR         = 0x00 << 3
    TXLVL       = 0X08 << 3
    RXLVL       = 0X09 << 3
        
    def __init__(self, i2c_addr=0x4D):
        '''Initialize sensor - set up I2C bus
           Args:
               self:
               i2c: unique address of the sensor
           Returns:
               None:
           Raises:
               None
        '''  
        
        self.i2c_addr = i2c_addr
        self.i2c      = smbus.SMBus(1)
    
    def begin(self, test=False):
        '''Turn on the sensor
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''  
        
        try:
            self.write_register(self.IOCONTROL, 0x08)
        except IOError:
            pass
            
        self.write_register(self.FCR, 0x07)
        self.write_register(self.LCR, 0x83)
        self.write_register(self.DLL, 0x60)
        self.write_register(self.DLH, 0x00)
        self.write_register(self.LCR, 0x03)

    def getCO2(self, test=False):
        '''Get the sensor reading
           Args:
               self:
               test:
           Returns:
               co2:
           Raises:
               None
        '''  
        
        self.write_register(self.FCR, 0x07)
        self.send(self.cmd_measure)
        return(self.parse(self.receive()))

    def parse(self, response):
        '''Parse the raw data, validate check-sum
           Args:
               self:
               response: reading from register
           Returns:
               ppm: cleaned up reading
           Raises:
               None
        '''  
        
        checksum = 0

        if len(response) < 9:
            return

        for i in range (0, 9):
            checksum += response[i]

        if response[0] == 0xFF:
            if response[1] == 0x9C:
                if checksum % 256 == 0xFF:
                    self.ppm = (response[2]<<24) + (response[3]<<16) + (response[4]<<8) + response[5]
                    return(self.ppm)

    def read_register(self, reg_addr):
        '''Reading of a register address
           Args:
               self:
               reg_addr: memory address to read
           Returns:
               reading: raw data
           Raises:
               None
        '''  
        
        time.sleep(0.001)
        return self.i2c.read_byte_data(self.i2c_addr, reg_addr)
        
    def write_register(self, reg_addr, val):
        '''Write data to a register
           Args:
               self:
               reg_addr: register address of where to write
               val: value to write
           Returns:
               None:
           Raises:
               None
        '''  
        
        time.sleep(0.001)
        self.i2c.write_byte_data(self.i2c_addr, reg_addr, val)
        
    def send(self, command):
        '''Conditional write of command data
           Args:
               self:
               command: command value to write
           Returns:
               None:
           Raises:
               None
        '''  
        
        if self.read_register(self.TXLVL) >= len(command):
            self.i2c.write_i2c_block_data(self.i2c_addr, self.THR, command)

    def receive(self):
        '''Read buffer, with timing control
           Args:
               self:
           Returns:
               None:
           Raises:
               None
        '''  
        
        n     = 9
        buf   = []
        start = time.clock()
        
        while n > 0:
            time.sleep(0.001)  # Added to slow down and avoid IO error
            rx_level = self.read_register(self.RXLVL)
            
            if rx_level > n:
                rx_level = n

            buf.extend(self.i2c.read_i2c_block_data(self.i2c_addr, self.RHR, rx_level))
            n = n - rx_level

            if time.clock() - start > 0.2:
                break

        return buf

    def test(self):
        print("*** CO2 Sensor Test ***\n")
        print("Begin")
        self.begin()

        for x in range(0,50):
            print("CO2 Concentration: " + str(self.getCO2()) + " ppm")
            time.sleep(1)
        print("Done")    


if __name__=="__main__":
    s=Sensor()
    s.test()
