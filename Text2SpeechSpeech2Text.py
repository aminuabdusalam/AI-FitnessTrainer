from email.mime import audio
from gtts import gTTS
from playsound import playsound
from random import randint
import os
import speech_recognition as sr

r = sr.Recognizer() #initialize the speech_recognizer

def text_to_speech(text):
    # exercises = ["curls", "pushups", "squats"]
    # text = "available exercises include " + str(exercises)
    tts = gTTS(text)    #convert text to speech using Google Text-to-Speech library (a Python library and CLI tool to interface with Google Translate text-to-speech API)
    audio_name = "speech.mp3"
    tts.save(audio_name)
    playsound(audio_name) #play the audio using playsound module.
    print(text)
    if os.path.exists(audio_name):
        os.remove(audio_name)



def speech_to_text():
    text = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) #removes ambient noise
        print("Listening...")
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5) #reads audio file, taking first 20 seconds of the audio.
        while True:
            try:
                # convert speech to text
                text = r.recognize_google(audio_data)
                print(text)
                break
            except:
                text_to_speech("I didn't catch that - I would try listening again")
                speech_to_text()
                break
        return text
     

# def speech_to_text2():   
#     info = sr.AudioFile("text.mp3")   #load audio
#     #open the file
#     with info as source:
#         r.adjust_for_ambient_noise(source) #removes ambient noise
#         audio_data = r.record(source,duration=100) #reads audio file, taking first 100 seconds of the audio.
#         #recognize (convert from speech to text)
#         text = r.recognize_google(audio_data)
#         print(text)


def main():
    pass

if __name__ == "__main__":
    text = "Hello! My name is Aminu."
    text_to_speech(text)
    # speech_to_text()

# playsound("hi.mp3")
# os.system("hi.mp3")




# I was using playsound version = 1.3.0 | With this version i have found same error like you. For solution you have to downgrade your playsound version. For this you have to first uninstall your playsound module by this code...pip uninstall playsound then press "y" to proceed . Then install the old and 
# pure version of playsound by this command... pip install playsound==1.2.2 and then try to execute your code.It will work.


# How to get started with Google Text-to-Speech using Python | by Bharath K | Towards Data Science https://towardsdatascience.com/how-to-get-started-with-google-text-to-speech-using-python-485e43d1d544 