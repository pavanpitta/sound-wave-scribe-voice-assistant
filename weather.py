
from main import speak, listen
import requests
from bs4 import BeautifulSoup
def get_city_name():
    speak("Please say the name of the city.")
    city = listen()
    return city

def get_weather_from_google(city):
    search_query = f"Weather in {city}"
    url = f"https://www.bing.com/search?q={search_query}"
    #url = f"https://www.google.com/search?q={search_query}"
    headers = {
        "User-Agent": "Edg/91.0.864.67"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        weather_card = soup.find("div", class_="wtr_currTemp b_focusTextLarge")
        if weather_card:
            return weather_card.text.strip()
        else:
            return "Weather information not found."
    else:
        return "Failed to fetch weather information."
        # example usage
city = get_city_name()
weather_info = get_weather_from_google(city)
weather_info1="the weather in " +city+ " is " +weather_info+ " degree celcius"
        

        # You can add code here to fetch the weather information using APIs like OpenWeatherMap
        #speak("Sorry, I can't fetch the weather right now.")
speak(weather_info1)