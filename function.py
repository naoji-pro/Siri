import requests
import wikipedia
import pywhatkit as kit
from newsapi import NewsApiClient
import smtplib
from decouple import config

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_line(query):
    TOKEN=''
    api_url='https://notify-api.line.me/api/notify'
    send_contents=query
    TOKEN_dic={'Authorization': 'Bearer' + ' ' + TOKEN}
    send_dic={'message': send_contents}
    requests.post(api_url, headers=TOKEN_dic, data=send_dic)

OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ja&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    temp_max=res["main"]["temp_max"]
    temp_min=res["main"]["temp_min"]
    return weather, f"{temperature}℃",f"{temp_max}℃",f"{temp_min}℃"

NEWS_API_KEY = config("NEWS_API_KEY")
def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=jp&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]
    