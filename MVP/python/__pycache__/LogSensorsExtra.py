"""
Record non-standard sensors to the database and logging

 Author : Howard Webb
 Date   : 03/12/2019
 
"""
from oneWireTemp import *
from TSL2561 import TSL2561
#from VL53L0X import *
from EC import EC
from CCS811 import CCS811, SLAVE
from CouchUtil import saveList
from LogUtil import get_logger
from scd30 import SCD30

class LogSensorExtra(object):

    def __init__(self):
        '''Set up logging and main variables
           Args:
               self:
           Returns:
               None:
           Raises:
               None
        '''               
        
        self._logger = get_logger('LogSensorExtra')
        self._activity_type = "Environment_Observation"

    def getAirAmbientTempObsv(self, test=False):
        '''One-Wire thermometer assigned to ambient reading
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               

        try:
            temp = getTempC(ambientTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'DS18B20_1', status_qualifier,''])
            self._logger.debug("{}, {}, {:10.1f}".format("Ambient Temp", status_qualifier, temp))            
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', '', 'Centigrade', 'DS18B20_1', status_qualifier, str(e)])            
            self._logger.error("{}, {}".format("Ambient Temp", e))            
        
    def getAirBoxTempObsv(self, test=False):
        '''One-Wire thermometer assigned to inside the box reading
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               

        try:
            temp = getTempC(boxTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'DS18B20_2', status_qualifier,''])            
            self._logger.debug("{}, {}, {:10.1f}".format("Box Air Temp", status_qualifier, temp))            

        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', '', 'Centigrade', 'DS18B20_2', status_qualifier, str(e)])                        
            self._logger.error("{}, {}".format("Box Air Temp", e))                                           
        
    def getAirTopTempObsv(self, test=False):
        '''One-Wire thermometer assigned to top of box
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               

        try:
            temp = getTempC(topTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Top', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'DS18B20_3', status_qualifier,''])            
            self._logger.debug("{}, {}, {:10.1f}".format("Top Air Temp", status_qualifier, temp))
                               
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Top', 'Air', 'Temperature', '', 'Centigrade', 'DS18B20_3', status_qualifier, str(e)])                                              
            self._logger.error("{}, {}".format("Top Air Temp", e))            
        
    def getNutrientReservoirTempObsv(self, test=False):
        '''One-Wire thermometer assigned to reservoir
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               
        try:
            temp = getTempC(reservoirTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'DS18B20_4', status_qualifier,''])            
            self._logger.debug("{}, {}, {:10.1f}".format("Reservoir Temp", status_qualifier, temp))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Air', 'Temperature', '', 'Centigrade', 'DS18B20_4', status_qualifier, str(e)])                                                          
            self._logger.error("{}, {}".format("Reservoir Temp", e))
                               
    def getLightCanopyLUXObsv(self, test=False):
        '''LUX light reading from the canopy
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               

        lx = TSL2561()
        try:
            lux = lx.getLux()
            
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', "{:3.1f}".format(lux), 'lux', 'TSL2561', status_qualifier,''])                        
            self._logger.debug("{}, {}, {:10.1f}".format("Canopy LUX", status_qualifier, lux))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', '', 'lux', 'TSL2561', status_qualifier,str(e)])                                    
            self._logger.error("{}, {}".format("Canopy LUX", e))                                           
     

    def getNutrientReservoirECObsv(self, test=False):
        '''Electrical conductivity of the reservoir
            Often used to control the filler system
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               

        try:
            s = EC()
            ec = s.getEC()
            
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', "{:3.1f}".format(ec), 'EC', 'EC', status_qualifier,''])                                    
            self._logger.debug("{}, {}, {:10.1f}".format("Reservoir EC", status_qualifier, ec))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', '', 'EC', 'EC', status_qualifier,str(e)])                                                
            self._logger.error("{}, {}".format("Reservoir Depth", e))                                           

    def getAirCanopyCO2Obsv(self, test=False):
        '''CO2 from the canopy (SCD30 Sensiron sensor)
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               
        
        status_qualifier = 'Success'
        co2 = 0
        temp = 0
        rh = 0
        try:
            sensor = SCD30()
            sensor.start_periodic_measurement(test)   
            co2, temp, rh = sensor.get_data(test)

            if test:
                status_qualifier = 'Test'
            
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'SCD30', status_qualifier,''])                                                
            self._logger.debug("{}, {}, {:10.1f}".format("Canopy CO2", status_qualifier, co2))            
            
            saveList([self._activity_type, '', 'Canopy', 'Air', 'Temperature', "{:3.1f}".format(temp), 'ppm', 'SCD30', status_qualifier,''])                                                
            self._logger.debug("{}, {}, {:10.1f}".format("Canopy Temperature", status_qualifier, temp))            
                               
            saveList([self._activity_type, '', 'Canopy', 'Air', 'Humidity', "{:3.1f}".format(rh), 'ppm', 'SCD30', status_qualifier,''])                                                
            self._logger.debug("{}, {}, {:10.1f}".format("Canopy Humidity", status_qualifier, rh))            
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', '', 'ppm', 'SCD30', status_qualifier,str(e)])                                                            
            self._logger.error("{}, {}".format("Canopy CO2", e))                                           

            saveList([self._activity_type, '', 'Canopy', 'Air', 'Temperature', '', 'c', 'SCD30', status_qualifier,str(e)])                                                            
            self._logger.error("{}, {}".format("Canopy CO2", e))                                           

            saveList([self._activity_type, '', 'Canopy', 'Air', 'Humidity', '', 'percent', 'SCD30', status_qualifier,str(e)])                                                            
            self._logger.error("{}, {}".format("Canopy Humidity", e))
            
    def getSecondCO2(self, test=False):
        '''CO2 from the canopy (CCS811 sensor)
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               
        try:
            sensor = CCS811(SLAVE)
            co2 = sensor.get_co2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'CCS811', status_qualifier,''])                                                            
            self._logger.debug("{}, {}, {:10.1f}".format("Alt CO2", status_qualifier, co2))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2','', 'ppm', 'CCS811', status_qualifier,str(e)])                                                                        
            self._logger.error("{}, {}".format("Alt CO2", e) )                                          

    def getNDIRCO2Obsv(self, test=False):
        '''CO2 from the canopy (NDIR sensor)
           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               
        
        status_qualifier = 'Success'
        co2 = 0
        temp = 0
        rh = 0
        try:
            from NDIR import Sensor
            sensor = Sensor()
            sensor.begin(test)   
            co2 = sensor.getCO2(test)

            if test:
                status_qualifier = 'Test'
            
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'NDIR', status_qualifier,''])                                                
            self._logger.debug("{}, {}, {:10.1f}".format("NDIR Canopy CO2", status_qualifier, co2))            
            
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', '', 'ppm', 'NDIR', status_qualifier,str(e)])                                                            
            self._logger.error("{}, {}".format("NDIR Canopy CO2", e))                                           


    def makeEnvObsv(self, test=False):
        '''Log extra sensors
           Uncomment code to activate sensor recording

           Args:
               self:
               test:
           Returns:
               None:
           Raises:
               None
        '''               
        
        #self._logger.debug("{}".format("Ambient Air Temp"))            
        #lg.getAirAmbientTempObsv(test)

        #self._logger.debug("{}".format("Box Air Temp"))            
        #lg.getAirBoxTempObsv(test)

        #self._logger.debug("{}".format("Top Air Temp"))            
        #lg.getAirTopTempObsv(test)

        #self._logger.debug("{}".format("Reservoir Temp"))
        #lg.getNutrientReservoirTempObsv(test)

        self._logger.debug("{}".format("Canopy LUX"))            
        lg.getLightCanopyLUXObsv(test)

        self._logger.debug("{}".format("Reservoir EC"))            
        lg.getNutrientReservoirECObsv(test)

        self._logger.debug("{}".format("Canopy CO2"))            
        lg.getAirCanopyCO2Obsv(test)

        self._logger.debug("{}".format("Alt CO2"))            
        lg.getSecondCO2(test)
        
        self._logger.debug("{}".format("NDIR CO2"))                    
        lg.getNDIRCO2Obsv(test)

        self._logger.debug("{}".format("EC"))            
        lg.getNutrientReservoirECObsv(test)

def test():
    lg = LogSensorExtra()                           
    lg.getNutrientReservoirECObsv()

if __name__=="__main__":
    '''Setup for calling from script'''
    lg = LogSensorExtra()                           
    lg.makeEnvObsv()
#    test()

    

       
