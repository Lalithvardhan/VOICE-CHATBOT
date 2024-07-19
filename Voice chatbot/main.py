import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
import time
from ecapture import ecapture as ec
import ctypes
import subprocess
import winshell

openai.api_key = "API KEY"

text_speech = pyttsx3.init()
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    if not url.endswith(".com"):
        url += ".com"
    webbrowser.open(url)

def open_app(app_name):
    app_executables = {
        "whatsapp": "WhatsApp.exe",
        "chrome": "chrome.exe",
        "microsoft edge": "msedge.exe",
        "discord": "Discord.exe",
        "spotify": "Spotify.exe",
        # Add more app names and their corresponding executables as needed
    }
    
    app_name_lower = app_name.lower()
    if app_name_lower in app_executables:
        app_path = os.path.join("C:\\Program Files", app_executables[app_name_lower])
        if os.path.exists(app_path):
            os.system(f"start {app_path}")
            text_speech.say(f"Opening {app_name}")
            text_speech.runAndWait()
            return True
    text_speech.say(f"I'm sorry, I couldn't find the {app_name} app on your device.")
    text_speech.runAndWait()
    return False


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"
    return query


if __name__ == "__main__":
    while True:
        with microphone as source:
            print("Listening:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        try:
            user_input = recognizer.recognize_google(audio)
            print("You said:", user_input)
        except sr.UnknownValueError:
            print("Could not understand audio")
            continue
        except sr.RequestError as e:
            print("Error; {0}".format(e))
            continue
        
        
        user_input_lower = user_input.lower()

        if "write a note" in user_input_lower:
            text_speech.say("What should i write, sir")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            text_speech.say("Sir, Should i include date and time")
            snfm = takeCommand()
            file.write(note)

        else:
            if "show note" in user_input_lower:
                text_speech.say("Showing Notes")
                file = open("jarvis.txt", "r") 
                print(file.read())
                text_speech.say(file.read(6))

            if 'play music' in user_input_lower or "play song" in user_input_lower:
                try:
                    text_speech.say("Here you go with music")
                    # music_dir = "G:\\Song"
                    music_dir = "C:\\Users\\LALITH VARDHAN\\Music"
                    songs = os.listdir(music_dir)
                    print(songs)    
                    random = os.startfile(os.path.join(music_dir, songs[1]))
                except:
                    print("there is no songs in the directory")
                continue
            
            if "camera" in user_input_lower or "take a photo" in user_input_lower:
                ec.capture(0, "Jarvis Camera ", "img.jpg")
                continue
            elif 'lock window' in user_input_lower:
                    text_speech.say("locking the device")
                    ctypes.windll.user32.LockWorkStation()
                    break
            elif 'shutdown system' in user_input_lower:
                    text_speech.say("Hold On a Sec ! Your system is on its way to shut down")
                    subprocess.call('shutdown / p /f')
                    break
            elif "restart" in user_input_lower:
                subprocess.call(["shutdown", "/r"])
                break
            elif "hibernate" in user_input_lower or "sleep" in user_input_lower:
                text_speech.say("Hibernating")
                subprocess.call("shutdown /f")
                break

            elif "log off" in user_input_lower or "sign out" in user_input_lower:
                text_speech.say("Make sure all the application are closed before sign-out")
                time.sleep(5)
                subprocess.call(["shutdown", "/l"])
                break
            elif 'empty recycle bin' in user_input_lower:
                winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                text_speech.say("Recycle Bin Recycled")
                continue
            elif 'change background' in user_input_lower:
                ctypes.windll.user32.SystemParametersInfoW(20, 
                                                           0, 
                                                           "Location of wallpaper",
                                                           0)
                text_speech.say("Background changed successfully")
                continue
            
            if any(word in user_input_lower for word in ["quit", "exit", "bye"]):
                text_speech.say("Chatbot: I am going to shutdown")
                text_speech.runAndWait()
                break
            elif "open app" in user_input_lower and "in my device" in user_input_lower:
                app_name = user_input.split("open app ")[-1].split(" in my device")[0]
                if not open_app(app_name):
                    continue
            elif "open" in user_input_lower or "website" in user_input_lower:
                website_name = "".join(user_input.split("open ")[1:]).replace(" ", "")
                open_website(website_name)
                continue

            elif 'the time' in user_input_lower:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")  
                text_speech.say(f"Sir, the time is {strTime}")
                continue 
            else:
                response = chat_with_gpt(user_input)
                print("Chatbot:", response)
                text_speech.say(response)
                text_speech.runAndWait()