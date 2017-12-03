# Create global variables as a dictionary, used when logging sensors that give the unique id of the system (MAC address) and the experiment started.
# A python file is generated that is 'read' by the logging program.
import os

env_file = '/home/pi/MVP/python/env.py'
var_file = '/home/pi/MVP/python/variable.py'

def saveDict(name, file_name, dict):
    #print(values)
    f = open(file_name, 'w+')
    tmp=name+'='+str(dict)
    f.write(tmp)
    f.close()

def saveEnv(dict):
    saveDict('env', env_file, dict)

def setEnv(name, value):
    import env
    env.env[name]=value
    saveEnv(env.env)

def delEnv(name):
    import env
    del env.env[name]
    saveEnv(env.env)

def saveVars(dict):
    saveDict('env', var_file, dict)

def setVariable(name, value):
    import variable as var
    var.env[name]=value
    saveVars(var.env)
    
def delVariable(name):
    import variable as var
    del var.env[name]
    saveVars(var.env)    
    
if __name__=="__main__":
    test1='test1'
    test2='test2'
    setEnv(test1, 'one')
    setVariable(test2, 'two')
    print(env.env)
    print(var.env)
    delEnv(test1)
    delVariable(test2)
    
