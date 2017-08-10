#!/usr/bin/python
#
#	JARVIS
#	Author	:	Gowtham Ramesh
#	Org		:	G Inc. 
#	Date	:	Aug 09 2017
#	Desc	: 	Jarvis is my personal assistant. Just like Ironman's
#

# Class QueryHandler
# Description:
#
# Parameters
#	
#
# ReturnVal
#	None
#
# Notes
#	None
#


class QueryHandler:
	
	#	QueryHandler::Init
	#	Description
	#		Constructor
	#	Paramters
	#		inputQuery	:	If query is set during object creation
	#	Returns
	#		None
	def __init__(self, inputQuery = None):
		self.inputQuery = inputQuery
		self.tokens = []

	#	QueryHandler::ProcessQuery
	#	Description
	#		Entry point for any query. Process the tokens and decide on action
	#	Paramters
	#		inputQuery	:	Query to be processed. If None, use the self variable
	#	Returns
	#		None
	def ProcessQuery(self, 	inputQuery):
		if inputQuery is None:
			print "Invalid Input"
		else:
			self.inputQuery = inputQuery

		# Split the tokens
		self.tokens = self.inputQuery.split()
		
		for current_word in self.tokens:
 			print(current_word)

	#	QueryHandler::PrintQuery
	#	Description
	#		Print a query on the console
	#	Paramters
	#		None
	#	Returns
	#		None
	def printQuery():
		print(self.inputQuery)