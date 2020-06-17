from gtts import gTTS #pip install gTTS
import datetime
import speech_recognition as sr #pip install speechRecognition
import webbrowser
import os
import smtplib
import wikipedia #pip install wikipedia
import subprocess

print('Aurora is Awakening...')

def AuroraSpeak(text):
    print(text)
    tts = gTTS(text=text, lang='en')
    speechAudio = tts.save('aurora.mp3')
    fileSave = './aurora.mp3'
    os.system('ffplay -nodisp -autoexit ' + fileSave)
    # subprocess.call(["ffplay", "-nodisp", "-autoexit", fileSave])
    os.remove(fileSave)
AuroraSpeak('Hi, my name is Aurora!')

#listen for commands

def myCommand():
    recog = sr.Recognizer()
    with sr.Microphone() as src:
        print('I am awaiting your next command')
        recog.pause_threshold = 1
        recog.adjust_for_ambient_noise = 1
        audio = recog.listen(src)

    try:
        command = recog.recognize_google(audio)
        print('You said' + command + '/n')

    #loop back to listen to commands incase of error

    except sr.UnknownValueError:
        AuroraSpeak('Uhh Ohh. There seems to be an error.')
        assistant(myCommand())
        return command

#function for executing commands
def assistant(command):
    if 'check weather' in command:
        AuroraSpeak('Alright, checking the weather forcast in your area.')
        subprocess(['weather'])

while True:
    #Keeps the assistant running and listening for commands
    assistant(myCommand())
