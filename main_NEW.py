#---------------------------------------------------------------------------------#

# all imports
import datetime
import os
import speech_recognition as sr
import win32com.client
import webbrowser
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import requests
#---------------------------------------------------------------------------------#

# api configuration
genai.configure(api_key='AIzaSyDSw3nQn5DaaU5BBHWyltCXZwUDRcAU0J4')
model = genai.GenerativeModel('gemini-pro')

#---------------------------------------------------------------------------------#

# craeting instance for speech genration
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# speak function
def say(text):
    speaker.Speak(text)

#---------------------------------------------------------------------------------#

# for taking commands using speech recognition
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said : {query}")
            return query
        except Exception as e:
            return 'Some error occured!'

#---------------------------------------------------------------------------------#
 
def greeting():
 hour = datetime.datetime.now().strftime('%H')
 if int(hour)<12:
  say('Good morning!')
 elif int(hour)>12 and int(hour)<18:
  say('Good afternoon!')
 else:
  say('Good evening!')

#---------------------------------------------------------------------------------#

def open_websites(query):
 sites = [['youtube','https://youtube.com'],['wikipedia','https://wikipedia.com'],['google','https://google.com'],['github','https://github.com'],['chat gpt','https://chat.openai.com/c/cc8ebe28-7fe1-41bd-b4fa-a9a877cfd119',],['whatsapp','https://web.whatsapp.com/']]
 for x in range(len(sites)):
  if sites[x][0].lower() in query.lower():
   say(f'Opening {sites[x][0]}!')
   webbrowser.open(sites[x][1])

#---------------------------------------------------------------------------------#

def play_music(query):
 musicpath = r'"C:\Users\admin\Desktop\jarvis recordings\mymusic.mp3"'
 try:
  os.startfile(musicpath)
  say("Playing music")
 except Exception as e:
  print("Error:", e)  # Print any error that occurs

#---------------------------------------------------------------------------------#

def get_time():
 hour = datetime.datetime.now().strftime('%H')
 minutes = datetime.datetime.now().strftime('%M')
 say(f'Sir the time is {hour} past {minutes}')

#---------------------------------------------------------------------------------#

def stop_function():
 for j in range(5):
  raise KeyboardInterrupt

#---------------------------------------------------------------------------------#
def push_data_to_flask(data):
    url = 'http://localhost:5000/generate_data'  # Change the URL if your Flask app is running on a different host/port
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    if response.ok:
        print("Data pushed successfully to Flask app")
    else:
        print("Failed to push data to Flask app")


def generate_function(query):
  try:
    response = model.generate_content(query)
    text = response.text
    data_to_push = {
    'prompt': query,
    'output': text
    }
    push_data_to_flask(data_to_push)
    say('Data saved into Database!')
    with open(f'{query[10:40]}.txt', 'w') as file:
      file.write(response.text)
    say('Sir an output file is generated for your prompt!')
  except Exception:
    say('Output was not generated due to some error!')

#---------------------------------------------------------------------------------#

# increasing/decreasing audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

def audio_function(query,num):
 current_volume = volume.GetMasterVolumeLevel()
 if 'increase'.lower() in query.lower():
  try:
   volume.SetMasterVolumeLevel(current_volume + int(num), None)
  except Exception:
   say('Volume cannot be increased with that value')
 else:
  try:
   volume.SetMasterVolumeLevel(current_volume - int(num), None)
  except Exception:
   say('Volume cannot be decreased with that value')

#---------------------------------------------------------------------------------#
# battery percentage
import psutil

def battery_function():
 battery = psutil.sensors_battery()
 percentage = battery.percent
 say(f"Battery percentage is {percentage}%")

#---------------------------------------------------------------------------------#
# opening an app

apps = [['postman',r'C:\Users\admin\AppData\Local\Postman\Postman.exe'],['notepad','notepad.exe']]
def app_function():
 for x in range(len(apps)):
  if apps[x][0].lower() in query.lower():
   say(f'Opening {apps[x][0]}!')
   os.startfile(apps[x][1]) 

#---------------------------------------------------------------------------------#

# main function
if __name__ == '__main__':

#---------------------------------------------------------------------------------#
    # basic greeting
    print("Program running!")
    greeting()
    say("I am Jarvis, How may I help you?")

#---------------------------------------------------------------------------------#
    # basic queries
    while True:
        # taking input
        print('Listening...')
        query = takeCommand()
#---------------------------------------------------------------------------------#
        # battery percentage
        if 'battery percentage'.lower() in query.lower():
         battery_function()

#---------------------------------------------------------------------------------#
        # for playing music
        if 'play music'.lower() in query.lower():
         play_music(query)

#---------------------------------------------------------------------------------#
        # for getting time
        if 'the time' in query.lower():
         get_time()
        
#---------------------------------------------------------------------------------#
        # increase/decrease audio
        if 'audio'.lower() in query.lower():
         audio_function(query,query[-2:])
        
#---------------------------------------------------------------------------------#
        # opening an app
        if 'open app'.lower() in query.lower():
         app_function()

#---------------------------------------------------------------------------------#
        # opening sites
        if 'open website'.lower() in query.lower():
         open_websites(query)

#---------------------------------------------------------------------------------#
        # generating using AI
        if 'generate'.lower() in query.lower():
          generate_function(query)

#---------------------------------------------------------------------------------#
        # stop function
        if 'stop executing'.lower() in query.lower():
         stop_function()

#---------------------------------------------------------------------------------#
