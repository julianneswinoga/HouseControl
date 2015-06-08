import re

def weatherCheck(inputText): # extract all relavent information from input text
    output = []

    
    return output

def parseForKeywords (inputText):
    inputText = str.lower(str.strip(re.sub(r'([^\s\w]|_)+', '', inputText)))

    fil = open("keywords.txt", "r")
    keyStrings = {}
    for line in fil:
        keyStrings[line.split(":")[0]] = line.split(":")[1].split(",")

    for app in keyStrings:
        print "Checking for " + app + "... ",
        for text in keyStrings[app]:
            if(str.find(inputText, text) != -1):
                if (app == "weather"):
                    return weatherCheck(inputText)
                elif (app == "test"):
                    print "Test successful, recognized: " + text
                    return ["test"]
                else:
                    print "ERROR!"
                    return ["error"]
            print "No " + text
