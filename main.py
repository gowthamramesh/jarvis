#!/usr/bin/python
#
#    JARVIS
#    Author    :    Gowtham Ramesh
#    Org        :    G Inc. 
#    Date    :    July 20 2017
#    Desc    :     Jarvis is my personal assistant. Just like Ironman's
#



#    Imports
from __future__ import print_function
import sys,os
os.chdir(os.path.dirname(sys.argv[0]))

import logging.config
import logging
from Queler.QueryHandler import QueryHandler
from ConfigParser import SafeConfigParser


#    Setup
logging.config.fileConfig('logging.conf')
logging.basicConfig(filename='example.log', filemode='w')
#     create logger
logger = logging.getLogger('InputProcessor')

queler = QueryHandler();

#    Config Parser
parser = SafeConfigParser()
parser.read('config.ini')

#    Members
PLUGIN_FOLDER = "plugins"
MODNAME = "ModuleName"
CLSNAME = "ClassName"
intents = {}
intentModules = {}

######################### User defined functions #########################

def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def loadModules () :
    intents = parser.sections();
    for intent in intents:
		modname = parser.get(intent, MODNAME)
		classname = parser.get(intent,CLSNAME)
		importmod = PLUGIN_FOLDER + "." + modname + "." + classname
		module = __import__(importmod, globals={}, locals={}, fromlist = ["*"])
		mod = getattr(module, classname)
		obj = mod()
		intentModules[intent] = obj

#    Main
#    Description
#        Main function. Set things up for Jarvis
#    Paramters
#        None
#    Returns
#        None
def main () :
    loadModules()
    while 1:
        print ("How may I help you?")
        UserInput    =    ""
        UserInput = sys.stdin.readline()
        UserInput = UserInput.rstrip('\n')
        logger.info ("User entered : %s", UserInput)
        logger.info ("Processing User input")
        queler.ProcessQuery(UserInput, intentModules)

######################### End of User defined functions ######################

# Welcome the User
print ("Hello, I am Gowtham\'s Assistant, Jarvis")

#     Call the main function
if __name__ == '__main__':
    main()
