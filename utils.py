import json
import os
import requests
from math import ceil
import pandas as pd
import datetime as dt
from urllib.parse import quote

def get_key():
    with open('apikey.txt','r') as key_file:
        key = key_file.read()
    return key

def create_prompt():
    with open('topics.txt','r') as topics_file:
        topics = topics_file.read()
    prompt = 'Write a short article about a specific topic of these categories, dive into details, do not provide an overview, be highly technical and provide links:\n'
    prompt += topics
    if os.path.exists(r'already_covered.xlsx'):
        already_covered = pd.read_excel('already_covered.xlsx')
        prompt += '\n\nAnd exclude this recently treated topics:\n'
        prompt += already_covered['title'].tail(5).to_string(index=False)
    else:
        already_covered = pd.DataFrame()
    return already_covered, prompt

def send_telegram(message):
    message = message.replace("\\n", "\n")
    bot_file = open('telegram_bot.json')
    bot = json.load(bot_file)
    message_size = len(message)
    if message_size > 4096:
        n_chunks = ceil(message_size/4096)
        chunk_size = ceil(message_size/n_chunks)
        for k in range(n_chunks):
            if k != n_chunks-1:
                trimmed_message = message[:chunk_size]
                message = message[chunk_size:]
            print(trimmed_message)
            url = f"https://api.telegram.org/bot{bot['token']}/sendMessage?chat_id={bot['chat_id']}&text={quote(trimmed_message)}"
            print(requests.get(url).json())
    else:
        url = f"https://api.telegram.org/bot{bot['token']}/sendMessage?chat_id={bot['chat_id']}&text={quote(message)}"
        print(requests.get(url).json())

def storicize_article(already_covered, today_title):
    today_row = {'date':dt.date.today().date, 'title':today_title}
    already_covered = already_covered.append(today_row, ignore_index = True)
    already_covered.to_excel('already_covered.xlsx', index=False)