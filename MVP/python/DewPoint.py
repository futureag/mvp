'''
Aproximate calculator for dewpoint based on temperature and relative humidity
For the purposes of the MVP, the extremes should not be an issue
Author: Howard Webb
Date: 10/12/2017
for details, see:

'''

import numpy as np
 
# approximation valid for
# 0 degC < T < 60 degC
# 1% < RH < 100%
# 0 degC < Td < 50 degC 
 
# constants
a = 17.271
b = 237.7 # degC
 

def getDewPoint(T,RH):
#    print('T', T, type(T))
#    print('RH', RH, type(RH))
    Td = (b * gamma(T,RH)) / (a - gamma(T,RH))
    return float(Td)
 
def gamma(T,RH):
    g = (a * T / (b + T)) + np.log(RH/100.0)
    return g

def getDewPointAprox(t, rh):
    return t-((100-rh)/5)
 
#dp=getDewPoint(12.7724626215, 45)
#print(dp)
#print(type(dp))
