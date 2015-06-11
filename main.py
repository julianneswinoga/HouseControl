import speech_recognition
import time
import common
import interpreter
OKAY_HOUSE = False

data = {}

def callback(recognizer, audio):
    global data
    try:
        transcribedText = str(recognizer.recognize(audio, False))
        print ">>> ", transcribedText
        if (OKAY_HOUSE):
            if (common.wholeWordFind(transcribedText, "okay house")):
                transcribedText = transcribedText.lower().replace("okay house", "")
                data = interpreter.parseForKeywords(transcribedText)
        else:
            transcribedText = transcribedText.lower().replace("okay house", "")
            data = interpreter.parseForKeywords(transcribedText)
        
    except LookupError:
        print "Oops! Didn't catch that"
        
recognizer = speech_recognition.Recognizer()
recognizer.listen_in_background(speech_recognition.Microphone(), callback)

while True:
    if (data != None and data != {}): print data
    time.sleep(0.1)
