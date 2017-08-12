#!/usr/bin/python
#
#    JARVIS
#    Author    :    Gowtham Ramesh
#    Date    :    Aug 12 2017
#    Desc    :     Jarvis is my personal assistant. Just like Ironman's
#

class NoteClass:
    def __init__(self):
        self.MyIntentSet = [
	        "Note.AddToNote",
			"Note.CheckOffItem",
			"Note.Clear",
			"Note.Confirm",
			"Note.Create",
			"Note.Delete",
			"Note.DeleteNoteItem",
			"Note.ReadAloud",
			"Note.ShowNext"
		]
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

    def CanProcessIntent(self, topIntent):
    	if topIntent in self.MyIntentSet:
    		return True
    	else:
    		return False

    def ProcessIntent(self, userIntent):
    	self.process_res(userIntent)

    def GetMyIntent(self):
        return "GetNoteInfo"







