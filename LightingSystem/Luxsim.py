from weather_info import weather
from datetime import datetime

class Luxsim(weather):
    
    def __init__(self):
        super(Luxsim, self).__init__()
        self.lux = self.setLux()

    def setCoeff(self):
        level = self.getLevel()
        coeff = 1
        return coeff
        
    def setLux(self):
        coeff = self.setCoeff()
        value = 0
        sunrise = datetime.fromtimestamp(self.getSunrise()).strftime("%Y-%m-%d %H:%M:%S")
        sunset = datetime.fromtimestamp(self.getSunset()).strftime("%Y-%m-%d %H:%M:%S")
        #currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        currenttime = datetime(2016, 6, 21, 14, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
        print "current time is = " + str(currenttime)
        currenttimehour = float(currenttime[11:13])
        currenttimemin = float(currenttime[14:16])
        sunrisehour = float(sunrise[11:13])
        sunsethour = float(sunset[11:13])
        sunrisemin = float(sunrise[14:16])
        sunsetmin = float(sunset[14:16])
        print "sunrise and sunset time : " + str(sunrise) + "  " + str(sunset)
        dayinterval = sunsethour - sunrisehour + (sunsetmin - sunrisemin) / 60
        dayinterval = round(dayinterval, 1)
        print "dayinterval = " + str(dayinterval) + " hours"
        if (currenttimehour >= sunrisehour) & (currenttimehour <= sunsethour):
            if round((currenttimehour + currenttimemin/60), 1) <= round(dayinterval/2, 1):
                time1 = round(currenttimehour + currenttimemin/60, 1)
                time2 = round(sunrisehour + sunrisemin/60, 1)
                value = (time2 - time1) * 1000/round(dayinterval/2, 1)
                self.lux = value * coeff
            else:
                time1 = round(currenttimehour + currenttimemin/60, 1)
                time2 = round(sunsethour + sunsetmin/60, 1)
                value = 1000 - (time2 - time1) * 1000/round(dayinterval/2, 1)
                self.lux = value * coeff
        else:
            print "It is night time"
            self.lux = 0
        print "current lux value is set to = " + str(self.lux)

L = Luxsim()