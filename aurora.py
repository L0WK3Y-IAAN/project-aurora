#add an idle mode 
#add an activation command such as "Hey, Aurora"
#implement AI
#add chat feature (AI chatbot)
#add proper KeyboardInterrut message 
#add music function


from gtts import gTTS  # pip install gTTS
import datetime
import speech_recognition as sr  # pip install speechRecognition
import webbrowser
import os
import smtplib
import wikipedia  # pip install wikipedia
import subprocess
from playsound import playsound
import requests
import json
import random
import keyboard
import operator


print('Aurora is Awakening...\n\n')


startUpAudio = './assets/StartUp.mp3'
powerDownAudio = './assets/PowerDown.mp3'
playsound(startUpAudio)

ttsResponses = random.choice(
    ['Hi, my name is Aurora, your virtual assistant, how may I help?!\n\n', 'Hello, how may I help?!\n\n', "What's up?!\n\n"])


def AuroraSpeak(ttsResponses):  # Aurora's speech function
    print(ttsResponses)
    tts = gTTS(text=ttsResponses, lang='en')
    tts.save('aurora.mp3')
    fileSave = './aurora.mp3'
    playsound(fileSave)
    os.remove(fileSave)


AuroraSpeak(ttsResponses)  # Aurora's speech output


recog = sr.Recognizer()  # Initializes speech recognition


def myCommand(ask=False):  # Listen for commands

    with sr.Microphone() as src:
        if ask:
            print(ask)
        print('Awaiting your command...\n\n')
        recog.pause_threshold = 1  # optional
        recog.adjust_for_ambient_noise = 1  # optional
        audio = recog.listen(src)
        voiceCommand = ""

    try:
        voiceCommand = recog.recognize_google(audio, language='en-us')
        print('You said: ' + voiceCommand + ' \n')

    # loop back to listen to commands incase of error

    except sr.UnknownValueError:
        errorRespones = random.choice(["Sorry. I didn't quite get that. Please try again.",
                                       "Sorry. I didn't quite get that. Here's a list of possible commands. \n"])
        AuroraSpeak(errorRespones)
        if errorRespones == "Sorry. I didn't quite get that. Here's a list of possible commands. \n":
            print("List of commands: \n\n" + 'locate - Search for a location on Google Maps \n\n' + 'wikipedia - Make a search on wikipedia \n\n' +
                  "check the weather | weather | what's the weather - Checks the weather in your location \n\n" + 'exit - Exits the program \n\n')

    except sr.RequestError:
        AuroraSpeak(
            "Sorry. I could not request results from Google Speech Recognition. It seems my speech services are down. \n")

    return voiceCommand


def main(voiceCommand):  # Main program (All possible commands)

    def calculator():
        # Reference https://www.codespeedy.com/voice-command-calculator-in-python/
        if 'calculator' in voiceCommand:
            with sr.Microphone() as src:
                AuroraSpeak(
                    "What would you like to calculate? For example say: 3 plus 3 \n")
                recog.adjust_for_ambient_noise = 1  # optional
                audio = recog.listen(src)
                calculation = recog.recognize_google(
                    audio, language='en-us')
                print(calculation)

            def get_operator_fn(op):
                return {
                    '+': operator.add,
                    '-': operator.sub,
                    '*': operator.mul,
                    'x': operator.mul,
                    'times': operator.mul,
                    'divided': operator.__truediv__,
                    '/': operator.__truediv__,
                    'Mod': operator.mod,
                    'mod': operator.mod,
                    '^': operator.xor,
                    'to the power of': operator.pow,
                    'power': operator.pow
                }[op]

            def eval_binary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)

            result = eval_binary_expr(*(calculation.split()))
            AuroraSpeak("The answer is: " + str(result) + ' \n')
    calculator()

    def searchCommands():
        if 'search' in voiceCommand:
            with sr.Microphone() as src:
                AuroraSpeak(
                    "What would you like to search for? \n")
                recog.adjust_for_ambient_noise = 1  # optional
                audio = recog.listen(src)
                search = recog.recognize_google(
                    audio, language='en-us')
                print(search + '\n')
            url = "https://www.google.com/search?q=" + search
            AuroraSpeak("Here's what I found for " + search)
            webbrowser.get().open_new_tab(url)
    searchCommands()

    def locationCommands():
        if 'locate' in voiceCommand:
            locationData = voiceCommand.split(" ")
            locationOutput = locationData[1]
            AuroraSpeak('Locating ' + locationOutput)
            url = "https://www.google.nl/maps/place/" + locationOutput + "/&amp;"
            webbrowser.get().open_new_tab(url)
    locationCommands()

    def wikipediaCommands():
        if 'wikipedia' in voiceCommand.lower():
            AuroraSpeak('Searching wikipedia...')
            # voiceCommand = voiceCommand.replace('wikipedia', '')
            results = wikipedia.summary(voiceCommand, sentences=2)
            AuroraSpeak(results)
    wikipediaCommands()

    def weatherCommands():
        if 'check the weather' in voiceCommand:
            # voiceCommand = voiceCommand.replace('weather', '')
            AuroraSpeak(
                'Alright, checking the weather forcast in your area.')
            send_url = 'http://ip-api.com/json/'
            req = requests.get(send_url)
            jsonData = json.loads(req.text)
            zipCode = jsonData['zip']
            url = 'https://weather.com/weather/today/l/' + zipCode
            webbrowser.get().open_new_tab(url)
    weatherCommands()

    def systemCommands():
        # Add 'have a nice day/night' depending on time
        ttsResponses = random.choice(
            ['See you later!\n\n', 'Goodbye!\n\n', 'Catch you later!\n\n'])
        if 'exit' in voiceCommand:
            AuroraSpeak(ttsResponses)
            playsound(powerDownAudio)
            exit()

    systemCommands()

    def helpCommands():
        if 'what can you do' in voiceCommand:
            AuroraSpeak("Here's a list of possible commands. \n")
            print("List of commands: \n\n" + 'locate - Search for a location on Google Maps \n\n' + 'wikipedia - Make a search on wikipedia \n\n' +
                  "check the weather | weather | what's the weather - Checks the weather in your location \n\n" + 'exit - Exits the program \n\n' + 'calculator - Performs basic calculations\n\n' + 'search - Performs a Google search\n\n')

    helpCommands()


while 1:  # Keeps the assistant running and listening for commands
    voiceCommand = myCommand()
    main(voiceCommand)
