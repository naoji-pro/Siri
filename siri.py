from asyncio import subprocess
import pyttsx3
import speech_recognition as sr
from tool import open_calculator, open_camera, open_cmd, open_notepad, open_excel,open_line
from function import  play_on_youtube, search_on_google, search_on_wikipedia, send_line, get_weather_report
from random import choice
from utils import opening_text
import requests
from function import *
engine = pyttsx3.init('sapi5')

#話す早さ
engine.setProperty('rate', 150)

#音量
engine.setProperty('volume', 1.0)

# Text to Speech Conversion
def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
        text='ご用件は何でしょう？'
        print(text)
        talk='ご用件はなんでしょう？'
        speak(talk)

def take_user_input():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='ja-JP')
        if not 'なんでもない' in query:
            speak(' ')
        else:
            speak("はい、わかりました。")
            exit()
    except Exception:
        #認識できなければ実行
        opening_text = [
            'すみません、なんとおっしゃったのかわかりません。',
            'すみません、うまく聞き取れませんでした。',
            'すみません、よくわかりません。',
        ]
        speak(choice(opening_text))
        query = 'None'
        exit()
    
    return query
import time
from datetime import date
from datetime import datetime as dt

def now_time():
       tdatetime= dt.now()
       tstr=tdatetime.strftime('%H時%M分%S秒です。')
       print(tstr)
       speak(tstr)

def set_timer(tl):
        left=int(tl)
        while left>0:
           print("残り時間 :"+str(left)+"秒")
           time.sleep(1)
           left-=1
        print("時間です。")
        speak("時間です。")

def open_alarm(query):
        str=query
        str=str.split('で設定して')[0]
        str=str.split('に設定して')[0]
        str=str.replace('時',':').replace('分','')
        print("設定時間",str)
        d_today=date.today()                        #今日の日付
        df_today=d_today.strftime("%Y-%m-%d")       #今日の日付を文字列型に変換
        dx_today=df_today+' '+str                   #今日の日付と設定した時刻
        dex=dt.strptime(dx_today,'%Y-%m-%d %H:%M')  #今日の日付と設定した時刻をdatetime型に変換
        cdt=dt.now()
        time_second=(dex-cdt).seconds               #設定時間から現在の時刻の差
        while time_second>0:
           time.sleep(1)
           time_second-=1
           if time_second==0:
               print("時間です。")
               speak('時間です。')

if __name__ == '__main__':
    greet_user()
    query = take_user_input().lower()
    if '今何時' in query or '時刻' in query:
            now_time()
    elif 'タイマー' in query:
            speak("何秒後に設定しますか？")
            query = take_user_input().lower()
            if '分' in query and '秒後' in query:
                ms=query                          #2分45秒後
                ms1=ms.split('分')[0]             #2
                ms2=ms.split('分')[1]             #45秒後
                ms2=ms2.split('秒後')[0]          #45
                ms3=int(ms1)*60+int(ms2)
                set_timer(ms3)
            elif '分後' in query:
                minutes=query
                minutes=minutes.split('分後')[0]
                minutes=int(minutes)*60
                set_timer(minutes)
            elif '秒後' in query:
                seconds=query
                seconds=seconds.split('秒後')[0]
                set_timer(seconds)
    elif 'アラーム'in query:
            speak("アラームをいつに設定しますか？")
            query = take_user_input().lower()
            open_alarm(query)
    elif 'メモ' in query:
            open_notepad()
    elif 'コマンド'  in query:
            open_cmd()
    elif 'カメラ' in query:
            open_camera()        
    elif '計算' in query:
            open_calculator()
    elif  'excel' in query:
            open_excel()
    elif  'line' in query:
            open_line()
            speak("誰にメッセージを送信しますか？")
            query = take_user_input().lower()
            if '送信して' in query:
                speak("なんて送りますか？")
                query = take_user_input().lower()
                print("送信内容 :",query)
                send_line(query)
            elif 'しなくていい' in query:
                exit()
    elif 'おはよう' in query:
            speak("おはようございます")
    elif  'お腹空いた' in query or '飲食店' in query:
            speak("なにが食べたいですか？")
            query = take_user_input().lower()
            if "おすすめ" in query or "決めて" in query:
                foods = [
                '焼肉','ラーメン','お寿司',
                ]
                query=choice(foods)
                speak(f"私のおすすめは{query}です。")
            else:
                query=query.replace("が食べたい。"," ")
            search_on_google(f"近くの{query}のお店")
    elif 'wikipedia' in query:
            speak('ウィキぺディアでなにについて調べますか?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            print(results)
            speak(f"ウィキペディアによると, {results}")
    elif 'youtube' in query:
            speak('ユーチューブでどんな動画を見ますか?')
            video = take_user_input().lower()
            play_on_youtube(video)
    elif 'google' in query or '検索' in query:
            TEXT=query
            TEXT=TEXT.split('で検索して')[0]
            if 'google' in query:
                speak('グーグルでなにを調べますか?')
                query = take_user_input().lower()
                TEXT2=query
                TEXT2=TEXT2.split('について調べて')[0]
                TEXT2=TEXT2.split('で調べて')[0]
                print("検索 :",TEXT2)
                search_on_google(TEXT2)
            elif '検索' in query:
                print("検索 :",TEXT)
                search_on_google(TEXT)
    elif '天気' in query or '気温' in query:
            city = "your city"
            speak(f"{city}の天気の情報を取得しています。")
            weather, temperature , temp_max, temp_min= get_weather_report(city)
            speak(f"現在の天気は {weather}で、気温は {temperature}です。")
            speak(f"最高気温は {temp_max}で、最低気温は {temp_min}です。")
            print(f"天気: {weather}\n気温: {temperature}\n最高気温: {temp_max}  最低気温: {temp_min}")
    elif 'ニュース' in query:
            speak("最新のニュース記事を取得しています。")
            speak("取得したニュース記事のタイトルを書き記ます。")
            print(*get_latest_news(), sep='\n')
            speak(get_latest_news())
    else:
            speak('すみません、お力になれません。')
            