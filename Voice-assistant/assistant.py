import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import requests
import json
import os
app={
    'notepad':'notepad.exe',
}
def speak(text):
    print(f"[ASSISTANT] : {text}")
    engine=pyttsx3.init()
    engine.setProperty('volume',0.8)
    engine.setProperty('rate',170)
    engine.say(text)
    engine.runAndWait()


def take_command():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...........")
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source,timeout=5,phrase_time_limit=4)
    try:
        command = r.recognize_google(audio).lower()
        speak(f"You Said {command}")
        if command=="exit":
            return 'exit'
        return command
    except  :
        speak('Not understand what you said!! please speak clearly...')
        return ""
            
def get_weather(city):
        api='f05f017fe5b645f288a155348252601'
        url=f"http://api.weatherapi.com/v1/current.json?key={api}&q={city}&aqi=no"
        r=requests.get(url)
        wed=r.json()
        location = wed['location']['name']
        region= wed['location']['region']
        country=wed['location']['country']
        temp=wed['current']['temp_c']
        condition=wed['current']['condition']['text']
        return f'''the weather of {location} which is in {region} region in {country} country is {condition}. the temperature is {temp} celcious. '''

def process_command(command):
    if command=="":
        return
    elif 'exit' in command:
        speak("Quiting the program.")
        exit()
    elif "time" in command:
        current_time=datetime.datetime.now().strftime("%I:%M%p")
        speak(f"Current time is {current_time}")
    elif "open" in command.lower():
        website=command.replace("open", "" ).strip()
        speak(f"Openning {website} ")
        if website in app:
            os.startfilea(app[website])
        else:
            webbrowser.open(f"https://www.{website}.com")
        
    elif "search" in command.lower():
        topic = command.replace("search ","").strip()
        try:
            speak(f"Searching about {topic} in wikipedia")
            summery=wikipedia.summary(topic,sentences=3)
            speak(summery)
        except wikipedia.exceptions.DisambiguationError as e :
            speak("Too many topic to search : ")
            print(e.options)
        except wikipedia.exceptions.PageError:
            speak(f"Cannot find {topic}")
    elif "weather" in command.lower():
        city=command.replace("weather in"," ").replace("weather of","").replace("weather","").strip()
        speak(get_weather(city))


        
speak("Hello SID!!! I am you're Personal Assistant!!")
while True:
    command=take_command()
    if 'exit' in command:
        speak("Quiting the program.")
        break
    process_command(command)
    
    