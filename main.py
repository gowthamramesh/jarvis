#!/usr/bin/python
#
#	JARVIS
#	Author	:	Gowtham Ramesh
#	Org		:	G Inc. 
#	Date	:	July 20 2017
#	Desc	: 	Jarvis is my personal assistant. Just like Ironman's
#



#	Imports
from __future__ import print_function
import sys,os
os.chdir(os.path.dirname(sys.argv[0]))
import logging.config
import logging
from Queler.QueryHandler import QueryHandler

logging.config.fileConfig('logging.conf')
logging.basicConfig(filename='example.log', filemode='w')
# create logger
logger = logging.getLogger('InputProcessor')

queler = QueryHandler();

######################### User defined functions #########################

#	Main
#	Description
#		Main function. Set things up for Jarvis
#	Paramters
#		None
#	Returns
#		None
def main () :
	print ("How may I help you?")
	UserInput	=	""
	UserInput = sys.stdin.readline()
	UserInput = UserInput.rstrip('\n')
	logger.info ("User entered : %s", UserInput)
	logger.info ("Processing User input")
	queler.ProcessQuery(UserInput)

######################### End of User defined functions ######################

# Welcome the User
print ("Hello, I am Gowtham\'s Assistant, Jarvis")

# 	Call the main function
if __name__ == '__main__':
	main()
