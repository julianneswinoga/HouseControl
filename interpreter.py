import re
import urllib2
import json
from pyowm import OWM #https://github.com/csparpa/pyowm/wiki/Usage-examples

def wholeWordFind(text, word):
    #print text + ", " + word
    word = word.strip().lower()
    nums = []
    tempText = text
    while (True): #Check for repeated occurances
        if (str.find(tempText, word) != -1):
            try:
                nums.append(str.find(tempText, word)+len(word)+nums[-1])
            except:
                nums.append(str.find(tempText, word))
            tempText = tempText[nums[-1]+len(word):]
        else:
            break
    for num in nums:
        if (num != -1):
            try:
                if (text[num-1] == " " and (num+len(word) == len(text) or text[num+len(word)] == " ")):
                    return True
                if (num == 0 and text[num+len(word)] == " "):
                    return True
            except:
                pass
    return False

def weatherCheck(inputText): # extract all relavent information from input text, returns a dictionary result
    output = {}
    owm = OWM()
    longitude = 0
    latitude = 0
    
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
            if (c[0] != "" and wholeWordFind(inputText, c[0])):
                city = c[0]
                if (country == ""): #If we didn't find a country yet, specify it from the city
                    country = c[1].strip()
                break
        
        if (country == "" or city == ""):
            raise NameError("No location")
        print "City is "+city
        print "Country is "+country
        obs = owm.weather_at_place(city+","+country)
    except NameError:
        if ((country == "") ^ (city == "")): #Logical xor
            print "Couldn't find a city and/or country: (city="+city+", country="+country+")"
        f = urllib2.urlopen('http://freegeoip.net/json/')
        json_string = f.read()
        f.close()
        location = json.loads(json_string)
        latitude = location["latitude"]
        longitude = location["longitude"]
        print "Latitude is "+str(latitude)
        print "Longitude is "+str(longitude)
        obs = owm.weather_at_coords(latitude,longitude)
    
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
    
    return output

def parseForKeywords (inputText): # returns a dictionary result
    inputText = str.lower(str.strip(re.sub(r'([^\s\w]|_)+', '', inputText)))

    fil = open("keywords.txt", "r")
    keyStrings = {}
    for line in fil:
        keyStrings[line.split(":")[0]] = line.split(":")[1].split(",")
    fil.close()
    
    print "Input string is: "+inputText
    for app in keyStrings:
        print "Checking for " + app + "... ",
        for text in keyStrings[app]:
            if(str.find(inputText, text) != -1):
                if (app == "weather"):
                    return weatherCheck(inputText)
                elif (app == "test"):
                    print "Test successful, recognized: " + text
                    return {"test":"success"}
                else:
                    print "ERROR!"
                    return {"error":0, "inputText":inputText, "search_text":text}
            print "No " + text
