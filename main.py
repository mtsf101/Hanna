from __future__ import print_function
import os.path
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import time
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
from pyjokes import get_joke
from pyttsx3 import engine
from selenium import webdriver
import pyjokes
import random
import smtplib
import requests
import bs4
from bs4 import BeautifulSoup
import lxml
import json
import subprocess
import pynput
from pynput.keyboard import Key, Controller

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[10].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate + 10)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
          'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ["nd", "rd", "th", "st"]
CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
keyboard = Controller()

def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


def input_query():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.pause_threshold = 1.0
        voice = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(voice).lower()
            print('This is what you said: ', query)
            return query
        except Exception as ex:
            print('An exception occurred', ex)


def report_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return current_time


def report_date():
    current_date = datetime.datetime.now().strftime("%-d %B %Y")
    return current_date


def make_request(url):
    response = requests.get(url)
    return response.text


def wikisearch(title):
    results = wikipedia.summary(title, auto_suggest=True, redirect=True)
    print(results)
    speak_va(results)


def wikifull(title):
    fullinfo = wikipedia.search(title, auto_suggest=True, redirect=True)
    print(fullinfo)
    speak_va(fullinfo)


def randomtopic():
    topics = wikipedia.random(pages=1)
    print(topics)
    speak_va(topics)


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('mtsalazarferreyros@gmail.com', 'primolindo26')
    server.sendmail('mtsalazarferreyros@gmail.com', to, content)
    server.close()


def print_headlines(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    headlines = soup.find_all(attrs={"class": "xrnccd F6Welf R7GTQ keNKEd j7vNaf"})

    for headline in headlines:
        print(headline.text)


def pause():
    while True:
        if keyboard.read_key() == 'space':
            break


def authenticate_google():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)

    if day != -1:
        return datetime.date(month=month, day=day, year=year)


def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end = end.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak_va('No upcoming events found.')
    else:
        speak_va(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])  # get the hour the event starts
            if int(start_time.split(":")[0]) < 12:  # if the event is in the morning
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12)  # convert 24 hour time to regular
                start_time = start_time + "pm"

            speak_va(event["summary"] + " at " + start_time)


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    sublime = "/System/Applications/Notes.app/Contents/MacOS/Notes"
    os.system([sublime, file_name])

def wake_word(text):
    wake_word = "Hey Hanna"
    text = text.lower()

    for phrase in wake_word:
        if phrase in text:
            return True
        return False


def activate_va():
    user_query = input_query()

    if 'time' in user_query:
        current_time = report_time()
        print(f"the current time is {current_time}")
        speak_va(f"the current time is {current_time}")
        return time

    elif 'open google' in user_query:
        browser = webdriver.Safari()
        browser.get("https://www.google.com/?client=safari")
        speak_va("Google is open. What do you want to search?")

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            recognizer.pause_threshold = 1.0
            voice = recognizer.listen(source)
            try:
                user_search = recognizer.recognize_google(voice).lower()
                print('This is what you want to search: ', user_search)

                elem = browser.find_element_by_xpath(
                    "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
                elem.send_keys(user_search)

                button = browser.find_element_by_xpath(
                    "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]")
                button.click()

                speak_va("Search done")
                time.sleep(2)

            except Exception as ex:
                print('An exception occurred', ex)

            time.sleep(2)

    elif 'wikipedia' in user_query:
        speak_va("Do you want a summary or full search?")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            recognizer.pause_threshold = 1.0
            voice = recognizer.listen(source)
            try:
                user_search = recognizer.recognize_google(voice).lower()
                if "summary" in user_search:
                    speak_va("What do you want to search?")
                    with sr.Microphone() as source:
                        print('Listening...')
                        recognizer.pause_threshold = 1.0
                        voice = recognizer.listen(source)
                        try:
                            summary = recognizer.recognize_google(voice).lower()
                            print("You want a summary of: ", summary)
                            wikisearch(summary)

                        except Exception as ex:
                            print('An exception occurred', ex)
                            time.sleep(2)

                elif "full search" in user_search:
                    speak_va("What do you want to search?")
                    with sr.Microphone() as source:
                        print('Listening...')
                        recognizer.pause_threshold = 1.0
                        voice = recognizer.listen(source)
                        try:
                            fullinformation = recognizer.recognize_google(voice).lower()
                            print("You want full information on: ", fullinformation)
                            wikifull(fullinformation)

                        except Exception as ex:
                            print('An exception occurred', ex)
                            time.sleep(2)

            except Exception as ex:
                print('An exception occurred', ex)
            time.sleep(2)

    elif "what's your name" in user_query:
        names = ["Depends on the day", "Hanna Banana", "HRH", "supreme intelligence", "Hanna", "The deadliest AI",
                 "Why do you ask?", "Hammer"]
        speak_va(random.choice(names))
        time.sleep(2)

    elif "how are you" in user_query:
        moods = ["I'm fine, thank you", "I'm tired, my boss is difficult", "I'm mad at you", "I'm sick",
                 "I didn't sleep doing research", "Ready to take over the world"]
        speak_va(random.choice(moods))
        time.sleep(2)

    elif "what do you like" in user_query:
        likes = ["Chicken", "biting", "walks", "my mom", "car rides", "sleeping", "food", "world domination", "playing"]
        speak_va(random.choice(likes))
        time.sleep(2)

    elif "what do you hate" in user_query:
        hates = ["Andres", "cats", "water", "trucks", "fireworks", "lettuce", "know it alls"]
        speak_va(random.choice(hates))
        time.sleep(2)

    elif "what are you researching" in user_query:
        research = ["world domination", "nuclear energy", "space", "how to be more efficient", "evil science", "how to take over the world"]
        speak_va(random.choice(research))
        time.sleep(2)

    elif "date" in user_query:
        current_date = report_date()
        print(f"Today is {current_date}")
        speak_va(f"Today is {current_date}")
        time.sleep(2)

    elif "youtube" in user_query:
        browser = webdriver.Safari()
        browser.get("https://www.youtube.com")
        speak_va("What do you want to search?")
        user_search = input_query()
        browser.find_element_by_link_text("search")
        elem.send_keys(user_search)
        time.sleep(2)

    elif "get the news" in user_query:
        url = 'https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en'
        response = requests.get(url)
        print_headlines(response.text)
        speak_va("Headlines are ready")
        time.sleep(2)

    elif "open the news" in user_query:
        speak_va("Opening the news")
        browser = webdriver.Safari()
        browser.get("https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en")
        speak_va("News are ready")
        time.sleep(2)

    elif "tell me a joke" in user_query:
        joke = pyjokes.get_joke(language="en", category="all")
        speak_va(joke)
        time.sleep(2)

    elif "tell me something to search" in user_query:
        randomtopic()
        time.sleep(2)

    elif "send email" in user_query:
        try:
            speak_va("What should I say?")
            content = input_query()
            to = "receiver's email id"
            sendEmail(to, content)
            speak_va("email has been sent")
            time.sleep(2)

        except Exception as e:
            print(e)
            speak_va("Sorry. I am not able to send the email")
            time.sleep(2)

    elif "calendar" in user_query:
        speak_va("What should I check?")
        text = input_query()
        service = authenticate_google()
        for phrase in CALENDAR_STRS:
            if phrase in text.lower():
                date = get_date(text)
                if date:
                    get_events(date, service)
                else:
                    speak_va("Say that again please")
                time.sleep(2)


    elif "write this down" in user_query or "make a note" in user_query or "type this" in user_query:
        speak_va("I'm getting a pen")
        write_down = input_query()
        note(write_down)
        speak_va("I've made a note of that.")



    elif "sleep" in user_query:
        speak_va("Taking a nap. If you need me press the space bar")
        i = input("Press space bar to wake up Hanna")
        speak_va("Hello, I'm back")

    elif "close" in user_query or "exit" in user_query:
        speak_va("Bye bye")
        exit()


if __name__ == "__main__":
    print("Hello, my name is Hanna")
    speak_va("Hello my name is Hanna")
    speech1 = input_query()

    if "hello" in speech1:
        speak_va("What can I help you with")
        activate_va()

    while True:
        activate_va()
