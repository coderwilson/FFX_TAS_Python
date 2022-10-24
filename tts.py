import pyttsx3
engine = pyttsx3.init()

def message(value:str):
    engine.say(value)
    engine.runAndWait()