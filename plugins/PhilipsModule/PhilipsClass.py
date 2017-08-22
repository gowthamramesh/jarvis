#!/usr/bin/python
#
#    JARVIS
#    Author    :    Gowtham Ramesh
#    Date    :    Aug 21 2017
#    Desc    :     Jarvis is my personal assistant. Just like Ironman's
#
from phue import Bridge
import random
from time import sleep

class PhilipsClass:
    def __init__(self):
        self.MyIntentSet = ["HomeAutomation.TurnOn", "HomeAutomation.TurnOff"]
        self.brdg = Bridge('192.168.0.2')

        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        self.brdg.connect()


    def CanProcessIntent(self, topIntent):
        if topIntent in self.MyIntentSet:
            return True
        else:
            return False

    def process_res(self, res):
        '''
        A function that processes the luis_response object and prints info from it.
        :param res: A LUISResponse object containing the response data.
        :return: None
        '''
        print('---------------------------------------------')
        print('LUIS Response: ')
        print('Query: ' + res.get_query())
        print('Top Scoring Intent: ' + res.get_top_intent().get_name())
        if res.get_dialog() is not None:
            if res.get_dialog().get_prompt() is None:
                print('Dialog Prompt: None')
            else:
                print('Dialog Prompt: ' + res.get_dialog().get_prompt())
            if res.get_dialog().get_parameter_name() is None:
                print('Dialog Parameter: None')
            else:
                print('Dialog Parameter Name: ' + res.get_dialog().get_parameter_name())
            print('Dialog Status: ' + res.get_dialog().get_status())
        print('Entities:')
        for entity in res.get_entities():
            print('"%s":' % entity.get_name())
            print('Type: %s, Score: %s' % (entity.get_type(), entity.get_score()))


    def ProcessIntent(self, userIntent):
        #self.process_res(userIntent)
        lights_list = self.brdg.get_light_objects('list')
        if userIntent.get_top_intent().get_name() == 'HomeAutomation.TurnOn':
            brightness = 150
            for entity in userIntent.get_entities():
                if entity.get_type() == "HomeAutomation.Operation":
                    if entity.get_name() == 'disco':
                        try:
                            while True:
                                for light in lights_list:
                                    light.brightness = 254
                                    light.xy = [random.random(),random.random()]
                        except KeyboardInterrupt as e:
                            return "Hope that was fun!"

                    brightness = entity.get_name();
                    if brightness.endswith('%'):
                        brightness = int(brightness.rstrip("%"))
                        brightness = 255 * brightness / 100
                    else:
                        brightness = int(brightness)
                    
            for light in lights_list:
               light.on = True
               light.brightness = brightness
               light.hue = 12000
               light.saturation = 80
            return "Lights ON"
        elif userIntent.get_top_intent().get_name() == 'HomeAutomation.TurnOff':
            for light in lights_list:
               light.on = False
            return "Lights off"
        return "Done"

    def GetMyIntent(self):
        return "PhilipsMod"



