import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import subprocess
import threading
import time

import math

def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        print("Error:", e)
        return None

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL_ADDRESS = '2203a52l04@sru.edu.in'
EMAIL_PASSWORD = 'achyuthreddy@sru'

def send_email(receiver_email, subject, body):
    try:
        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_server.starttls()
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        smtp_server.send_message(msg)
        smtp_server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", str(e))

def receive_emails():
    try:
        imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        imap_server.select('inbox')

        _, data = imap_server.search(None, 'ALL')
        email_ids = data[0].split()

        emails = []
        for email_id in email_ids:
            _, data = imap_server.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            subject = msg['Subject']
            sender = msg['From']
            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
            emails.append({'sender': sender, 'subject': subject, 'body': body})

        imap_server.close()
        imap_server.logout()

        return emails
    except Exception as e:
        print("Error receiving emails:", str(e))
        return []
    
# Initialize task list
tasks = []

def add_task(task_name):
    tasks.append({'name': task_name, 'completed': False})

def list_tasks():
    if tasks:
        speak("Here are your tasks:")
        for i, task in enumerate(tasks, start=1):
            status = "completed" if task['completed'] else "not completed"
            speak(f"{i}. {task['name']} ({status})")
    else:
        speak("You don't have any tasks.")

reminders = {}

def set_reminder(reminder_time, reminder_text):
    reminders[reminder_time] = reminder_text

def check_reminders():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        for reminder_time, reminder_text in list(reminders.items()):
            if current_time == reminder_time:
                speak(f"Reminder: {reminder_text}")
                del reminders[reminder_time]  # Remove the reminder after it's triggered
        time.sleep(30)  # Check for reminders every 30 seconds

# Start the background thread for checking reminders
reminder_thread = threading.Thread(target=check_reminders)
reminder_thread.start()

def mark_task_as_completed(task_number):
    try:
        index = int(task_number) - 1
        if 0 <= index < len(tasks):
            tasks[index]['completed'] = True
            speak(f"Task '{tasks[index]['name']}' marked as completed.")
        else:
            speak("Invalid task number.")
    except ValueError:
        speak("Invalid input. Please specify the task number.")

def delete_task(task_number):
    try:
        index = int(task_number) - 1
        if 0 <= index < len(tasks):
            del tasks[index]
            speak("Task deleted successfully.")
        else:
            speak("Invalid task number.")
    except ValueError:
        speak("Invalid input. Please specify the task number.")

def start_timer(duration, original_duration, unit):
    time.sleep(duration)
    speak(f"Timer finished for {original_duration} {unit}.")
# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

calendar = {}

def add_event_to_calendar(event, date):
    if date in calendar:
        calendar[date].append(event)
    else:
        calendar[date] = [event]

def get_upcoming_events(date):
    events = calendar.get(date, [])
    return events

def parse_date(date_str):
    today = datetime.date.today()
    if date_str == "today":
        return today
    elif date_str == "tomorrow":
        return today + datetime.timedelta(days=1)
    elif date_str == "day after tomorrow":
        return today + datetime.timedelta(days=2)
    else:
        # Assume the date string is in YYYY-MM-DD format
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

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
import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def get_antonyms_synonyms(word):
    antonyms = []
    synonyms = []
    url = f"https://www.wordhippo.com/what-is/another-word-for/{word}.html"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Corrected class name for antonyms
        antonyms_section = soup.find("div", class_="opposites-container")
        if antonyms_section:
            antonyms_list = antonyms_section.find_all("a", class_="linkify")
            if antonyms_list:
                antonyms = [a.text.strip() for a in antonyms_list]

        # Corrected class name for synonyms
        synonyms_section = soup.find("div", class_="synonyms-container")
        if synonyms_section:
            synonyms_list = synonyms_section.find_all("a", class_="linkify")
            if synonyms_list:
                synonyms = [a.text.strip() for a in synonyms_list]

    return antonyms, synonyms

# Define the base URL for the Open Exchange Rates API
BASE_URL = "https://open.er-api.com/v6/latest/"

def convert_currency(amount, from_currency, to_currency):
    try:
        # Construct the API URL for fetching exchange rates
        api_url = f"{BASE_URL}{from_currency.upper()}"
        response = requests.get(api_url)
        data = response.json()

        # Check if the response is successful
        if response.status_code == 200:
            # Retrieve the exchange rate for the target currency
            exchange_rate = data["rates"][to_currency.upper()]
            # Perform the currency conversion
            converted_amount = amount * exchange_rate
            return converted_amount
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


def perform_task(query):

    if "hi" in query:
        speak("Hello! How can I assist you now?")

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
        #import weather
        subprocess.run(["python","weather.py"])

    elif "news" in query:
        #import news
        subprocess.run(["python","news.py"])
    
    elif any(q in query for q in ["what is the time now", "can you say the time", "what is the current time", 
                      "can you tell me the time", "what time is it right now", "could you let me know the current time",
                      "do you have the time", "i need to know the time, can you help", "what's the time",
                      "can you say the time, please", "do you have a clock", "is it possible to know the time"]):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The current time is " + current_time)

    elif "take notes" in query:
        speak("Sure, please dictate your note. Say 'save the file' when you're done.")
        note_text = ""
        while True:
            note_part = listen()
            if "save the file" in note_part:
                break
            note_text += note_part + "\n"
    
        if note_text:
        # Get the current date and time
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Open a file in append mode and write the note along with the timestamp
            with open("notes.txt", "a") as file:
                file.write(f"\n\n{current_datetime}:\n{note_text}")
        
            speak("Note taken successfully and saved to file.")
        else:
            speak("No notes were recorded.")

    elif "show notes" in query:
        try:
            with open("notes.txt", "r") as file:
                notes = file.read()
            if notes:
                speak("Here are your notes:")
                speak(notes)
            else:
                speak("No notes available.")
        except FileNotFoundError:
            speak("No notes available.")
    
    elif "antonyms for" in query:
        word = query.split("antonyms for ")[1]
        antonyms, _ = get_antonyms_synonyms(word)
        if antonyms:
            speak(f"Antonyms for {word} are: {' '.join(antonyms)}")
        else:
            speak(f"No antonyms found for {word}.")

    elif "synonyms for" in query:
        word = query.split("synonyms for ")[1]
        _, synonyms = get_antonyms_synonyms(word)
        if synonyms:
            speak(f"Synonyms for {word} are: {' '.join(synonyms)}")
        else:
            speak(f"No synonyms found for {word}.")

    elif "set timer for" in query:
        try:
            # Extract the timer duration from the query
            duration_text = query.split("for ")[1]
            original_duration = duration_text.split()[0]  # Extract the original duration text
            
            if "hour" in duration_text:
                duration = int(duration_text.split("hour")[0].strip()) * 3600
                unit = "hour"
            elif "minute" in duration_text:
                duration = int(duration_text.split("minute")[0].strip()) * 60
                unit = "minute"
            elif "second" in duration_text:
                duration = int(duration_text.split("second")[0].strip())
                unit = "second"
            else:
                raise ValueError("Invalid duration format")
            
            if duration <= 0:
                speak("Please provide a valid duration for the timer.")
            else:
                speak(f"Timer set for {original_duration} {unit}.")
                timer_thread = threading.Thread(target=start_timer, args=(duration, original_duration, unit))
                timer_thread.start()
        except ValueError:
            speak("Sorry, I couldn't understand the duration for the timer.")

    elif "exit" in query:
        speak("Thank you! Have a nice day. If any further assistance is needed, feel free to run me again.")
        exit()

    today_date_phrases = ["today's date", "what is the date today", "date today", "current date"]

    # Check if the query contains any phrases related to today's date
    if any(phrase in query for phrase in today_date_phrases):
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {today_date}.")

    elif "add event to calendar" in query:
        try:
            speak("Sure, please specify the event.")
            event = listen()
            speak("Got it. Now, please specify the date for the event (e.g., today, tomorrow, or YYYY-MM-DD).")
            date_str = listen().lower()
            event_date = parse_date(date_str)
            add_event_to_calendar(event, event_date)
            speak(f"Event '{event}' added to the calendar on {event_date}.")
        except ValueError:
            speak("Sorry, I couldn't understand the date format.")

    elif "upcoming events" in query:
        speak("Sure, please specify the date for which you want to check the events (e.g., today, tomorrow, or YYYY-MM-DD).")
        date_str = listen().lower()
        check_date = parse_date(date_str)
        upcoming = get_upcoming_events(check_date)
        if upcoming:
            speak(f"Here are your upcoming events for {check_date}:")
            for event in upcoming:
                speak(event)
        else:
            speak(f"No events found for {check_date}.")

    elif "set reminder" in query:
        speak("Sure, please specify the reminder time in HH:MM format.")
        reminder_time = listen()
        speak("Got it. Now, please specify the reminder text.")
        reminder_text = listen()
        set_reminder(reminder_time, reminder_text)
        speak("Reminder set successfully.")


    elif "send email" in query:
        try:
            speak("Sure, please specify the recipient email address.")
            receiver_email = listen()
            speak("Got it. Now, please specify the email subject.")
            subject = listen()
            speak("Please dictate the email body.")
            body = listen()
            send_email(receiver_email, subject, body)
            speak("Email sent successfully.")
        except Exception as e:
            speak("Sorry, there was an error sending the email.")

    elif "check emails" in query:
        emails = receive_emails()
        if emails:
            speak("Here are your latest emails:")
            for email_data in emails:
                speak(f"From: {email_data['sender']}, Subject: {email_data['subject']}, Body: {email_data['body']}")
        else:
            speak("No new emails found.")

    elif "add task" in query:
        speak("Sure, please specify the task.")
        task_name = listen()
        add_task(task_name)
        speak("Task added successfully.")

    elif "list tasks" in query:
        list_tasks()

    elif "mark task as completed" in query:
        speak("Sure, please specify the task number.")
        task_number = listen()
        mark_task_as_completed(task_number)

    elif "delete task" in query:
        speak("Sure, please specify the task number.")
        task_number = listen()
        delete_task(task_number)
    
    elif "convert currency" in query:
        try:
            speak("Sure, please specify the amount, the currency to convert from, and the currency to convert to.")
            user_input = listen().split()
            amount = float(user_input[0])
            from_currency = ""
            to_currency = ""
            for word in user_input[1:]:
                if word.lower() == "to":
                    break
                from_currency += word
            for word in user_input[user_input.index("to") + 1:]:
                to_currency += word
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            if from_currency and to_currency:
                converted_amount = convert_currency(amount, from_currency, to_currency)
                if converted_amount is not None:
                    speak(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}.")
                else:
                    speak("Sorry, unable to perform currency conversion.")
            else:
                speak("Sorry, unable to perform currency conversion. Please provide valid input.")
        except Exception as e:
            speak("Sorry, unable to perform currency conversion. Please provide valid input.")

    elif "add" in query:
        # Replace "add" with "+"
        expression = query.replace("add", "+")
        try:
            result = calculate(expression)
            if result is not None:
                speak(f"The result of {expression} is {result}.")
            else:
                speak("Sorry, unable to perform the calculation.")
        except Exception as e:
            speak("Sorry, unable to perform the calculation. Please provide a valid expression.")

    elif "subtract" in query:
        # Replace "subtract" with "-"
        expression = query.replace("subtract", "-")
        try:
            result = calculate(expression)
            if result is not None:
                speak(f"The result of {expression} is {result}.")
            else:
                speak("Sorry, unable to perform the calculation.")
        except Exception as e:
            speak("Sorry, unable to perform the calculation. Please provide a valid expression.")

    elif "multiply" in query:
        # Replace "multiply" with "*"
        expression = query.replace("multiply", "*")
        try:
            result = calculate(expression)
            if result is not None:
                speak(f"The result of {expression} is {result}.")
            else:
                speak("Sorry, unable to perform the calculation.")
        except Exception as e:
            speak("Sorry, unable to perform the calculation. Please provide a valid expression.")

    elif "divide" in query:
        # Replace "divide" with "/"
        expression = query.replace("divide", "/")
        try:
            result = calculate(expression)
            if result is not None:
                speak(f"The result of {expression} is {result}.")
            else:
                speak("Sorry, unable to perform the calculation.")
        except Exception as e:
            speak("Sorry, unable to perform the calculation. Please provide a valid expression.")


    else:
        speak("Sorry, I didn't understand that. Could you please repeat or try a different command?")
    

if __name__ == "__main__":
    speak("Hello! How can I assist you now?")
    
    while True:
        query = listen()
        if "exit" in query:
            speak("Thank you! Have a nice day, If any further assist needed feel free to run me again")
            break
        perform_task(query)
