import smbus2, time


address = 0x40
rh_no_hold = 0xf5
previous_temp = 0xe0


class si7021(object):
    def __init__(self):
        self.bus = smbus2.SMBus(1)

    def read_word(self):
        """
        Use I2C ioctl to read Si7021 measurements because SMBus ioctl misbehaves.
        If you just call read_byte() twice, you get the same byte both times. And
        if you try to read a 2 byte buffer here, it also doesn't work right. For
        some reason, 3 bytes seems to be okay.
        """
        msg = smbus2.i2c_msg.read(0x40, 3)
        self.bus.i2c_rdwr(msg)
        msb = ord(msg.buf[0])
        lsb = ord(msg.buf[1])
        checksum = ord(msg.buf[2])
#        print "  si7021 i2c read:", msb, lsb, checksum
        return (msb*256) + lsb

    def write(self, command):
        self.bus.write_byte(address, command)
	
    def temp_and_humidity(self):
        self.write(rh_no_hold)
        time.sleep(0.03)
        percent_rh = self.read_word()
        percent_rh = 125.0/65536.0*percent_rh-6.0
        self.write(previous_temp)
        temp_c = self.read_word()
        temp_c = 175.72/65536.0*temp_c-46.85
        return temp_c, percent_rh

    def getHumidity(self):
        self.write(rh_no_hold)
        time.sleep(0.03)
        percent_rh = self.read_word()
        percent_rh = 125.0/65536.0*percent_rh-6.0
        return percent_rh

    def getTempC(self):
        self.write(previous_temp)
        temp_c = self.read_word()
        temp_c = 175.72/65536.0*temp_c-46.85
        return temp_c

    def test(self):
        'Self test of the object'
        print('\n*** Test SI7021 ***\n')
        print('Temp C: %.2f F' %self.getTempC())
        print('Humidity : %.2f %%' %self.getHumidity())

if __name__=="__main__":
    t=si7021()
    t.test()
    
