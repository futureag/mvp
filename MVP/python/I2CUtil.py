"""
 Wrapper of commonly used I2C message functions from periphery

 Author : Howard Webb
 Date   : 06/20/2018
 
"""

from periphery import I2C as pI2C

class I2C(object):

   def __init__(self, addr):
      self._path = "/dev/i2c-1"
      self._addr = addr
      self._i2c = pI2C(self._path)

   def __exit__(self, exc_type, exc_value, traceback):
      self._i2c.close()

   def get_msg(self, cmds, size):
       """Send and receive multiple messages
           Should return the welcome message

           Args:
               path: location of device file
               addr: address of the I2C Device
               cmds: array of commands to send
               size: size of byte array to return data in
           Returns:
               msgs: array of messages
           Raises:
               None
       """
   #    print "Get Msg1"
   #    for cmd in cmds:
   #        print "Cmd: ", hex(cmd)
   #    print "Buffer:", size        
       msgs = [self._i2c.Message(cmds), self._i2c.Message(bytearray([0x00 for x in range(size)]), read=True)]
       try:
           self._i2c.transfer(self._addr, msgs)
           ret = msgs[1].data
   #        for data in ret:
   #            print "Data:", hex(data)
           return msgs
       except Exception as e:
           print e
           return None


   def msg_write(self, cmds):
       """Write to sensor
           Args:
               cmds: commands to send
           Returns:
               msb: data from sent message
           Raises:
               None
      """
   #    print "Msg Write"
   #    for cmd in cmds:
   #        print hex(cmd)
       msgs = [self._i2c.Message(cmds)]
       try:
           self._i2c.transfer(self._addr, msgs)
   #        msb = msgs[0].data[0]
   #        print "MSB", hex(msb)
           return msgs

       except Exception as e:
           print e
           return None

   def msg_read(self, size):
       """Read existing data
           Args:
               path: location of device file
               addr: address of the I2C Device
               size: size of byte array for receiving data
           Returns:
               msgs: should be only one message returned
           Raises:
               None
      """
           
   #    print "Msg Read", size
       msgs = [self._i2c.Message(bytearray([0x00 for x in range(size)]), read=True)]
       try:
           self._i2c.transfer(self._addr, msgs)
           msb = msgs[0].data[0]
           lsb = msgs[0].data[1]
           checksum = msgs[0].data[2]
   #        print "MSB", msb, "LSB:", lsb, "Checksum:", checksum
           return msgs 

       except Exception as e:
           print e
           return None    

def bytesToWord(high, low):
   """Convert two byte buffers into a single word value
       shift the first byte into the work high position
       then add the low byte
        Args:
            high: byte to move to high position of word
            low: byte to place in low position of word
        Returns:
            word: the final value
        Raises:
            None
   """   
   word = (high << 8) + low
   return word


