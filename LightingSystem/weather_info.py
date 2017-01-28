import json
import urllib

class weather(object):

    def __init__(self):
        self.url = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=89b0d25b5372053b338f9bf0689921fd'
        self.urlout = urllib.urlopen(self.url)
        self.weather_info = json.loads(self.urlout.read())

    def getWeather(self):
        weather_detailed = self.weather_info['weather']
        weather_simplified = weather_detailed[0]['main']
        print 'weather condition is '+'"'+str(weather_simplified)+'"'
        return weather_simplified

    def getTemp(self):
        temp = self.weather_info['main']['temp']
        print 'current temp is '+str(temp)
        return temp

    def getHumidity(self):
        humid = self.weather_info['main']['humidity']
        print 'current humidity is '+str(humid)
        return humid

    def getPressure(self):
        pre = self.weather_info['main']['pressure']
        print 'current pressure is '+str(pre)
        return pre

    def getSunrise(self):
        rise = self.weather_info['sys']['sunrise']
        print rise
        return rise


    def getLevel(self):
        level = 1
        info = self.getWeather()
        if info == 'cloudy':
            level = 1
            return level

    def getSunset(self):
        set = self.weather_info['sys']['sunset']
        print set
        return set