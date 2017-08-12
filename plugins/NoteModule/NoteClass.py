#!/usr/bin/python
#
#    JARVIS
#    Author    :    Gowtham Ramesh
#    Org        :    G Inc. 
#    Date    :    Aug 12 2017
#    Desc    :     Jarvis is my personal assistant. Just like Ironman's
#

class NoteClass:
    def __init__(self):
        self.intent = "AddToNote"

    def GetMyIntent(self):
        return "AddToNote"

    def ProcessIntent(self, userIntent):
    	print ("Processing AddtoNote intent")
    	print(userIntent)







