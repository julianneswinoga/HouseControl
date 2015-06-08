import speech_recognition
import time
OKAY_HOUSE = False

def callback(recognizer, audio):
    try:
        transcribedText = recognizer.recognize(audio, True)
        print(">>> " + transcribedText)
        
    except LookupError:
        print("Oops! Didn't catch that")
        
recognizer = speech_recognition.Recognizer()
recognizer.listen_in_background(speech_recognition.Microphone(), callback)

while True:
    time.sleep(0.1)
