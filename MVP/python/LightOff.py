#!/usr/bin/python

#Light Control
#Thin wrapper over Light object so can easily call from bash script
# Author: Howard Webb
# Date: 3/29/2018

from Light import Light

if __name__=="__main__":
    l=Light()
    l.set_off()
