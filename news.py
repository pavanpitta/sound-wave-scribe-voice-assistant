import requests
from bs4 import BeautifulSoup
from main import speak, listen

# Function to fetch news headlines from Bing for a specific city
def get_news_headlines(city):
    search_query = f"{city} news"
    url = f"https://www.bing.com/news?q={search_query}"
    headers = {
        "User-Agent": "Edg/91.0.864.67"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = soup.find_all("a", class_="title")
        if headlines:
            news_headlines = [headline.text.strip() for headline in headlines]
            return news_headlines[:3]  # Only top 5 headlines
        else:
            return "No news headlines found for the specified city."
    else:
        return "Failed to fetch news headlines."

# Main function to fetch and speak news headlines for a specific city
def fetch_and_speak_news():
    speak("Please specify the city for news headlines.")
    city = listen()  # Get city name through voice input
    if city:
        news_headlines = get_news_headlines(city)
        if isinstance(news_headlines, list):
            news_headlines_message = f"Here are the latest news headlines for {city}:"
            for i, headline in enumerate(news_headlines):
                news_headlines_message += f"\n{headline}"
            speak(news_headlines_message)
        else:
            speak(news_headlines)
    else:
        speak("Failed to recognize city name. Please try again.")

# Call the function to fetch and speak news headlines for a specific city
fetch_and_speak_news()
