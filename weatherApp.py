import common
from pyowm import OWM #https://github.com/csparpa/pyowm/wiki/Usage-examples

def weatherCheck(inputText): # extract all relavent information from input text, returns a dictionary result
    print "Checking weather!"
    output = {}
    owm = OWM()
    longitude = 0
    latitude = 0

    if (owm.is_API_online()):
        print "OWM API is ONLINE"
        try: #Try to find location of device
            country = ""
            city = ""
            for c in ["canada", "us", "united states"]:
                if (str.find(inputText, c) != -1):
                    country = c

            cityList = []
            fil = open("city_list.txt", "r")
            for line in fil:
                cityData = line.split("\t")
                cityList.append([cityData[1], cityData[4]]) #City name and country
            fil.close()
            
            for c in cityList:
                if (c[0] != "" and common.wholeWordFind(inputText, c[0])):
                    city = c[0]
                    if (country == ""): #If we didn't find a country yet, specify it from the city
                        country = c[1].strip()
                    break
            
            if (country == "" or city == ""):
                raise NameError("No location")
            
        except NameError:
            if ((country == "") ^ (city == "")): #Logical xor
                print "Couldn't find the city and/or country: (city="+city+", country="+country+")"
            location = common.getLocation()
            city = location["city"]
            country = location["country_name"]

        print "City is "+city
        print "Country is "+country
        obs = owm.weather_at_place(city+","+country)
        
        w = obs.get_weather()
        output["clouds"] = w.get_clouds() #Cloud coverage
        output["rain"] = w.get_rain() #Rain volume
        output["snow"] = w.get_snow() #Snow volume
        output["wind"] = w.get_wind() #Wind direction and speed
        output["humidity"] = w.get_humidity() #Humidity percentage
        output["pressure"] = w.get_pressure() #Atmospheric pressure
        output["temperature"] = w.get_temperature("celsius") #Temperature
        output["status"] = w.get_detailed_status() #Get general status of weather
        output["sunrise"] = w.get_sunrise_time() #Sunrise time (GMT UNIXtime or ISO 8601)
        output["sunset"] = w.get_sunset_time() #Sunset time (GMT UNIXtime or ISO 8601)
    else:
        print "OWM API is OFFNLINE, FAILED"
        output["status"] = "FAILED"
    return output
