import re
import common
import weatherApp

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
            if(str.find(inputText, text) != -1 and text != ""):
                if (app == "weather"):
                    return weatherApp.weatherCheck(inputText)
                elif (app == "test"):
                    print "Test successful, recognized: " + text
                    return {"test":"success"}
                else:
                    print "ERROR!"
                    return {"error":0, "inputText":inputText, "search_text":text}
            #print "No " + text,
