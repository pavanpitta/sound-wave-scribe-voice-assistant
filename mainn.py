import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import weather

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print(text)  # Print the text to verify output
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio).lower()
            print("You said:", query)
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Sorry, I couldn't request results. Check your internet connection.")
            return ""

def perform_task(query):
    if "hi" in query:
        speak("Hello! How can I assist you today?")
    elif "how are you" in query:
        speak("I'm doing well, thank you for asking!")
    elif "who are you" in query:
        speak("I am a voice assistant created by ChatGPT. I'm here to help you with tasks.")
    elif "what's going on" in query:
        speak("Not much, just here to assist you.")
    elif "open" in query:
        website = query.split("open")[1].strip()
        webbrowser.open_new_tab("https://www." + website + ".com")
        speak("Opening " + website)
    elif "weather" in query:
        weather.fetch_and_speak_weather()  # Call function from weather module
    elif "news" in query:
        import news
    elif "time in" in query:
        import timein
    elif "time" in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + time)
    elif "exit" in query:
        speak("Thank you! Have a nice day. If any further assistance is needed, feel free to run me again.")
        exit()
    else:
        speak("I'm not sure how to help with that.")

if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    
    while True:
        query = listen()
        if "exit" in query:
            perform_task(query)
        else:
            perform_task(query)
