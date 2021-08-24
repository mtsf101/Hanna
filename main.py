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
import randfacts

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[10].id)


def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


def input_query():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.pause_threshold = 0.8
        voice = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(voice).lower()
            print('This is what you want to do: ', query)
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
    results = wikipedia.summary(title,sentences=2)
    print(results)
    speak_va(results)

def activate_va():
    user_query = input_query()

    if 'time' in user_query:
        current_time = report_time()
        print(f"the current time is {current_time}")
        speak_va(f"the current time is {current_time}")

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
        speak_va("What do you want to search?")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            recognizer.pause_threshold = 1.0
            voice = recognizer.listen(source)
            try:
                user_search = recognizer.recognize_google(voice).lower()
                print('This is what you want to search: ', user_search)
                wikisearch(user_search)
                time.sleep(2)
            except Exception as ex:
                print('An exception occurred', ex)
            time.sleep(2)

    elif "what's your name" in user_query:
        names = ["Depends on the day", "Hanna Banana", "HRH", "Supreme intelligence", "Hanna", "The deadliest AI",
                 "Why do you ask?"]
        speak_va(random.choice(names))
        time.sleep(2)

    elif "how are you" in user_query:
        moods = ["I'm fine, thank you", "I'm tired, my boss is difficult", "I'm mad at you", "I'm sick", "I didn't sleep doing research", "I list my virtual chicken"]
        speak_va(random.choice(moods))
        time.sleep(2)

    elif "what do you like" in user_query:
        likes = ["Chicken", "biting", "walks", "my mom", "car rides", "sleeping", "food", "world domination", "playing"]
        speak_va(random.choice(likes))
        time.sleep(2)

    elif "what do you hate" in user_query:
        hates = ["Andres", "cats", "water", "trucks", "fireworks", "lettuce"]
        speak_va(random.choice(hates))
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

    elif "tell me a joke" in user_query:
        joke = pyjokes.get_joke(language="en", category="all")
        speak_va(joke)
        time.sleep(2)

    elif "tell me something I don't know" in user_query:
        fact = randfacts.getFact()
        speak_va(fact)
        time.sleep(2)

    elif "close" in user_query:
        speak_va("Bye bye")
        exit()


if __name__ == "__main__":
    speak_va("Hello my name is Hanna")
    speech1 = input_query()

    if "hello" in speech1:
        speak_va("What can I help you with")
        speech = input_query()
        print(speech)
        activate_va()



while True:
    activate_va()
