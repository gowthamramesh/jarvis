#!/usr/bin/python
#
#    JARVIS
#    Author    :    Gowtham Ramesh
#    Date    :    Aug 09 2017
#    Desc    :     Jarvis is my personal assistant. Just like Ironman's
#

# Class QueryHandler
# Description:
#
# Parameters
#    
#
# ReturnVal
#    None
#
# Notes
#    None
#

from luis_sdk import LUISClient
from gtts import gTTS
import os

class QueryHandler:
    
    #    QueryHandler::Init
    #    Description
    #        Constructor
    #    Paramters
    #        inputQuery    :    If query is set during object creation
    #    Returns
    #        None
    def __init__(self, inputQuery = None):
        self.inputQuery = inputQuery
        self.tokens = []
        self.__APPID__ = "18680fc7-d5f3-41b8-95ce-1fa4743ed70d"
        self.__APPKEY__ = "e4d7710b899342e3888c798fbb02ca13"
    
    def process_res(self, res):
        '''
        A function that processes the luis_response object and prints info from it.
        :param res: A LUISResponse object containing the response data.
        :return: None
        '''
        print(u'---------------------------------------------')
        print(u'LUIS Response: ')
        print(u'Query: ' + res.get_query())
        print(u'Top Scoring Intent: ' + res.get_top_intent().get_name())
        if res.get_dialog() is not None:
            if res.get_dialog().get_prompt() is None:
                print(u'Dialog Prompt: None')
            else:
                print(u'Dialog Prompt: ' + res.get_dialog().get_prompt())
            if res.get_dialog().get_parameter_name() is None:
                print(u'Dialog Parameter: None')
            else:
                print('Dialog Parameter Name: ' + res.get_dialog().get_parameter_name())
            print(u'Dialog Status: ' + res.get_dialog().get_status())
        print(u'Entities:')
        for entity in res.get_entities():
            print(u'"%s":' % entity.get_name())
            print(u'Type: %s, Score: %s' % (entity.get_type(), entity.get_score()))

    def IdentifyIntent(self):
        try:
            TEXT = self.inputQuery
            CLIENT = LUISClient(self.__APPID__, self.__APPKEY__, True)
            res = CLIENT.predict(TEXT)
            while res.get_dialog() is not None and not res.get_dialog().is_finished():
                TEXT = raw_input(u'%s\n'%res.get_dialog().get_prompt())
                res = CLIENT.reply(TEXT, res)
            #self.process_res(res)
            return res
        except Exception, exc:
            print(exc)


    #    QueryHandler::ProcessQuery
    #    Description
    #        Entry point for any query. Process the tokens and decide on action
    #    Paramters
    #        inputQuery    :    Query to be processed. If None, use the self variable
    #    Returns
    #        None
    def ProcessQuery(self, inputQuery, intentModules):
        if inputQuery is None:
            print "Invalid Input"
        else:
            self.inputQuery = inputQuery

        userIntent = self.IdentifyIntent();
        topIntent = userIntent.get_top_intent().get_name()
        for intentMod in intentModules:
            if intentModules[intentMod].CanProcessIntent(topIntent):
                pluginResponse = intentModules[intentMod].ProcessIntent(userIntent)
                tts = gTTS(text=pluginResponse, lang='en')
                tts.save("jarvis.mp3")
                os.system("afplay jarvis.mp3")

    #    QueryHandler::PrintQuery
    #    Description
    #        Print a query on the console
    #    Paramters
    #        None
    #    Returns
    #        None
    def printQuery():
        print(self.inputQuery)












