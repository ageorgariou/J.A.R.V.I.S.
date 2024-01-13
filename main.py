#Imports
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
from AppOpener import open
import pyautogui
import smtplib
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

#Engine start
print('Loading your AI personal assistant - jarvis')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

#Email sending
def send_email(to, subject, body):
    email = "your_email"
    password = "your_app_password"

    msg = EmailMessage()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
            return "Email sent successfully."
    except Exception as e:
        return str(e)

def get_email_info():
    speak("To who do you want to send the email?")
    to_email = input(print("Please type the email adress."))
    time.sleep(6)
    speak(f"You said: {to_email}. Is this correct?")
    confirmation = takeCommand()
    if 'yes' in confirmation:
        speak("What is the subject of your email?")
        subject = takeCommand()
        speak("What should I say in your email?")
        body = takeCommand()
        speak("Should I send the email?")
        send_confirmation = takeCommand()
        if 'yes' in send_confirmation:
            response = send_email(to_email, subject, body)
            speak(response)
        else:
            speak("Email not sent.")
    else:
        get_email_info()


#Get calendar
def get_calendar_events():
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.readonly'])
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.readonly'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', ['https://www.googleapis.com/auth/calendar.readonly'])
                creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        time.sleep(1)
        speak(f"You have an event {event['summary']} at {start}")

#Brains
def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

speak("Loading your AI personal assistant jarvis")
wishMe()

#Functions
if __name__=='__main__':


    while True:
        speak("Tell me how can I help you?")
        statement = takeCommand().lower()
        if statement==0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement  or "shut down" in statement  or "shut up" in statement or "goodbye" in statement  or "bye" in statement:
            speak('your personal assistant jarvis is shutting down,Good bye')
            print('your personal assistant jarvis is shutting down,Good bye')
            break

        if "take a screenshot" in statement or "screenshot" in statement:
            myScreenshot = pyautogui.screenshot()
            speak("What do you want the name to be?")
            name = takeCommand()
            myScreenshot.save(rf'C:\Users\Alex\Desktop\Images\{name}.png')
            speak('I saved the screenshot')

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Opening youtube-")
            time.sleep(3)
        
        elif 'open discord' in statement:
            open("discord")
            speak("Opening discord")
            time.sleep(3)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Opening google")
            time.sleep(3)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Opening Gmail")
            time.sleep(3)
        
        elif 'open vs' in statement or 'vs' in statement or 'visual code' in statement or 'visual studio' in statement:
            open("visual studio code")
            speak("Opening Visual Studio code")
            webbrowser.open_new_tab("https://chat.openai.com/")
            speak("Happy coding!")
            time.sleep(2)
        

        elif "weather" in statement:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            complete_url=base_url+"appid="+api_key+"&q="+"Athens"
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))



        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am jarvis version 1 point O your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')


        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Alex")
            print("I was built by Alex")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")
            time.sleep(3)

        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines.')
            time.sleep(3)
          
        elif 'search'  in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(3)

        elif 'ask' in statement or 'i have a question' in statement or 'question' in statement or 'what is' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=takeCommand()
            app_id="R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
            time.sleep(3)

        elif 'music' in statement:
            webbrowser.open_new_tab("https://open.spotify.com/")
            speak("Enjoy some tunes")
            time.sleep(3)

        elif 'send an emai' in statement or 'send a email' in statement or 'send email' in statement:
            print("It is working")
            get_email_info()
            print("Email sent")
            speak("Email sent")
            time.sleep(3)

        elif 'calendar' in statement:
            get_calendar_events()
            time.sleep(3)

        elif "log off" in statement or "sign out" in statement:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

time.sleep(3)
