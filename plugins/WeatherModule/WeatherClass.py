#!/usr/bin/python
#
#    JARVIS
#    Author    :    Gowtham Ramesh
#    Date    :    Aug 12 2017
#    Desc    :     Jarvis is my personal assistant. Just like Ironman's
#
import pyowm
import json
import urllib2

class WeatherClass:
    def __init__(self):
        self.owm = pyowm.OWM('5d4091f8e8c4cb29bea4c484925012e6')  # You MUST provide a valid API key
        self.MyIntentSet = ["Weather.GetCondition", "Weather.GetForecast"]

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

    def DisplayWeatherCondition (self, w, observation):
        location = observation.get_location().get_name()
        clouds = w.get_clouds()                                     # Get cloud coverage
        
        rain = w.get_rain()                                       # Get rain volume
        #{'3h': 0}

        snow = w.get_snow()                                       # Get snow volume
        #{}

        wind = w.get_wind()                                       # Get wind degree and speed
        #{'deg': 59, 'speed': 2.660}

        humidity = w.get_humidity()                                   # Get humidity percentage

        pressure = w.get_pressure()                                   # Get atmospheric pressure
        #{'press': 1009, 'sea_level': 1038.381}

        temp = w.get_temperature()                                # Get temperature in Kelvin
        #{'temp': 293.4, 'temp_kf': None, 'temp_max': 297.5, 'temp_min': 290.9}
        #>>> w.get_temperature(unit='celsius')                  # ... or in Celsius degs
        temp_farenheit = w.get_temperature(unit = 'fahrenheit')                    # ... or in Fahrenheit degs

        # w.get_status()                                     # Get weather short status
        #'clouds'
        status = w.get_detailed_status()                           # Get detailed weather status
        #'Broken clouds'

        #>>> w.get_weather_code()                               # Get OWM weather condition code
        #803

        #>>> w.get_weather_icon_name()                          # Get weather-related icon name
        #'02d'

        sunrise = w.get_sunrise_time('iso')                               # Sunrise time (GMT UNIXtime or ISO 8601)
        #1377862896L
        sunset = w.get_sunset_time('iso')                           # Sunset time (GMT UNIXtime or ISO 8601)
        #'2013-08-30 20:07:57+00'

        print ('Weather Condition:')
        print ('    Location : %s ' % location)
        print ('    Today : %s ' % status)
        print ('    Temperature : %s' % str(temp_farenheit['temp']))
        print ('      High : %s' % str(temp_farenheit['temp_max']))
        print ('      Low : %s' % str(temp_farenheit['temp_min']))
        print ('    Wind Speed : %s' % str(wind['speed']))
        print ('    Humidity : %s' % humidity)
        print ('    Sunrise : %s,  Sunset %s' % (sunrise, sunset))
        print ('    Cloud coverage : %s' % clouds)
        print ('    Rain volume : %s' % rain)
        print ('    Snow volume : %s' % snow)

    def GetWeatherCondition (self, userIntent):
        first_entity = None
        for entity in userIntent.get_entities ():
            first_entity = entity
            break
        w = None
        observation = None
        if first_entity is not None:
            observation = self.owm.weather_at_place(first_entity.get_name())
            w = observation.get_weather()
        else:
            try:
                location = json.load(urllib2.urlopen('http://ipinfo.io/json'))
                lat,lon = location['loc'].split(',')
                observation = self.owm.weather_at_coords(float(lat),float(lon))
                w = observation.get_weather()
            except urllib2.HTTPError:
                observation = self.owm.owm.weather_at_place('San Fransisco')
                w = observation.get_weather()

        self.DisplayWeatherCondition (w, observation)
        temp_farenheit = w.get_temperature(unit = 'fahrenheit')   
        status = w.get_detailed_status()  

        UserMessage = ''
        UserMessage = 'Today is going to be ' 
        UserMessage+= status
        UserMessage+= 'With Highs of around '
        UserMessage+= str(temp_farenheit['temp_max'])
        UserMessage+= ' and lows of '
        UserMessage+= str(temp_farenheit['temp_min'])
        UserMessage+= ' in'
        UserMessage+= observation.get_location().get_name()

        return UserMessage

    def GetForecastInfo (self, userIntent):
        return ' Forecast is nice. Good day'


    def ProcessIntent(self, userIntent):
        #self.process_res(userIntent)
        userMessage = ''
        if userIntent.get_top_intent().get_name() == 'Weather.GetCondition':
            userMessage = self.GetWeatherCondition (userIntent)
        elif userIntent.get_top_intent().get_name() == 'Weather.GetForecast':
            userMessage = self.GetForecastInfo (userIntent)

        return userMessage

    def GetMyIntent(self):
        return "GetWeatherInfo"








