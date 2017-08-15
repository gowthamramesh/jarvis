#!/usr/bin/python
#
#    JARVIS
#    Author    :    Gowtham Ramesh
#    Date    :    Aug 12 2017
#    Desc    :     Jarvis is my personal assistant. Just like Ironman's
#

from evernote.api.client import EvernoteClient
from evernote.edam.type import ttypes
from evernote.edam.notestore import NoteStore

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
        self.dev_token = "S=s1:U=93ee0:E=16534e58a74:C=15ddd345e18:P=1cd:A=en-devtoken:V=2:H=4f78553252348f5484d827aacdcec982"
        self.client = EvernoteClient(token=self.dev_token)
        noteStore = self.client.get_note_store()
        notebooks = noteStore.listNotebooks()
        self.jarvisnotebook = None
        for n in notebooks:
            if n.name == 'JarvisNotes':
                self.jarvisnotebook = n
                break
        filter = NoteStore.NoteFilter()
        updated_filter = NoteStore.NoteFilter()
        # I also try to add as shown in below commented line the words parameters
        #updated_filter.words="intitle:Python"
        offset = 0
        max_notes = 10
        result_spec = NoteStore.NotesMetadataResultSpec(includeTitle=True)
        result_list = noteStore.findNotesMetadata(updated_filter, 0, max_notes, result_spec)

        JarvisListPresent = False
        for note in result_list.notes:
            if note.title == "JarvisList":
                self.jarvislist = noteStore.getNote(note.guid, True, False, False, False) 
                JarvisListPresent = True
                break
        if JarvisListPresent == False:
            self.jarvislist = self.makeNote(noteStore, "JarvisList", "", self.jarvisnotebook)

    def makeNote(self, noteStore, noteTitle, noteBody, parentNotebook=None):

        nBody = '<?xml version="1.0" encoding="UTF-8"?>'
        nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        nBody += '<en-note>%s</en-note>' % noteBody

        ## Create note object
        ourNote = ttypes.Note()
        ourNote.title = noteTitle
        ourNote.content = nBody

        ## parentNotebook is optional; if omitted, default notebook is used
        if parentNotebook and hasattr(parentNotebook, 'guid'):
            ourNote.notebookGuid = parentNotebook.guid

        ## Attempt to create note in Evernote account
        try:
            note = noteStore.createNote(ourNote)
        except Errors.EDAMUserException, edue:
            ## Something was wrong with the note data
            ## See EDAMErrorCode enumeration for error code explanation
            ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
            print "EDAMUserException:", edue
            return None
        except Errors.EDAMNotFoundException, ednfe:
            ## Parent Notebook GUID doesn't correspond to an actual notebook
            print "EDAMNotFoundException: Invalid parent notebook GUID"
            return None

        ## Return created note object
        return note

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

    def processAddToNote(self, query):
        nBody = ""
        if self.jarvislist.content is None:
            nBody = '<?xml version="1.0" encoding="UTF-8"?>'
            nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            nBody += '<en-note><div>%s</div></en-note>' % query
        else:
            nBody = self.jarvislist.content
            nBody = nBody[:-10]
            nBody += '<div>%s</div></en-note>' % query

        ## Create note object
        ourNote = self.jarvislist
        ourNote.content = nBody
        self.client.get_note_store().updateNote(ourNote)

    def CanProcessIntent(self, topIntent):
        if topIntent in self.MyIntentSet:
            return True
        else:
            return False

    def ProcessIntent(self, userIntent):
        #self.process_res(userIntent)
        topIntent = userIntent.get_top_intent().get_name()
        if topIntent == 'Note.AddToNote':
            for entity in userIntent.get_entities():
                if entity.get_type() == "Items":
                    self.processAddToNote(entity.get_name())
        elif topIntent == 'Note.Create':
            print "Processing create note"
        elif topIntent == 'Note.Delete':
            print "Processing delete note"
        else:
            print "Unknown Note processing"
        print ("Easy peasy... Done...")
    def GetMyIntent(self):
        return "GetNoteInfo"







