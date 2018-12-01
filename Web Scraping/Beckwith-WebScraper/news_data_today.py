#!activate PythonData
# coding: utf-8

# Chrome Driver and Imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import prettify
import requests
import requests
import time
from citipy import citipy
import json
import tweepy
import datetime
from config import consumer_key, consumer_secret, access_token, access_token_secret
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

print(datetime.datetime.now())

from flask import Flask, jsonify, render_template
import pymongo

#set up connection to mlab
app = Flask(__name__)
DB_NAME = 'manufacture_consent'
DB_HOST = 'ds255403.mlab.com'
DB_PORT =  55403
DB_USER = 'edwardwisejr'
DB_PASS = 'Flender77!'
connection = pymongo.MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)

#ENTER STATE OF CHOICE
state = 'WI'

#####BROWSER####
url = f"https://www.stationindex.com/tv/by-state/{state}"
browser.visit(url)
html=(browser.html)
soup = bs(html, 'html.parser')
soup.encode("utf-8")
pretty = soup.prettify
links = soup.find_all('a')
callsigns = []
markets = []
urls = []
# get the links from the 
for link in links:
    if "tv/callsign" in link['href']:
        callsigns.append(link.string)
        urls.append(link['href'])
#         print(link.string)
    elif "tv/markets" in link['href']:
        markets.append(link.string)
stations = pd.DataFrame({
    "Callsign": callsigns,
    "Market": markets,
    "URL": urls
})
## GET WEBSITES FOR EACH LOCAL STATION IN THE STATE
page_twitters = []
website_links = []
station_urls = stations['URL']
for station in station_urls:
    browser.visit(station)
    html=(browser.html)
    soup = bs(html, 'html.parser')
    soup.encode("utf-8")
    links = soup.find_all('a')
    page_links=[]
    for link in links:
        page_links.append(link.text)
        if "http" in link.text:
            website_links.append(link.text)
# # ## New Headless Driver if needed
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=True)
## GET EVERY STATION'S LINKS WITH A FILTER
times = []
websites = []
states = []
link_texts = []
buzz_words = []
twitter_links = []
daily_news = db.mc_daily_state_news
for link in website_links:
    browser.visit(link)
    html=(browser.html)
    soup = bs(html, 'html.parser')
    soup.encode("utf-8")
    links = soup.find_all('a')
    for l in links:
        if "Trump" in l.text:
            print(f"Link Text on {link} : {l.text}")
            daily_state_news =  {
                "State": state,
                "Buzz Word": "Trump",
                "Website": link,
                "Time": datetime.datetime.now(),
                "Link Text": l.text
            }
            daily_news.insert_one(daily_state_news)
        elif "migrant" in l.text:
            print(f"Link Text on {link} : {l.text}")
            daily_state_news =  {
                "State": state,
                "Buzz Word": "migrant",
                "Website": link,
                "Time": datetime.datetime.now(),
                "Link Text": l.text
            }
            daily_news.insert_one(daily_state_news)
        elif "email" in l.text:
            print(f"Link Text on {link} : {l.text}")
            daily_state_news =  {
                "State": state,
                "Buzz Word": "email",
                "Website": link,
                "Time": datetime.datetime.now(),
                "Link Text": l.text
            }
        elif "Mueller" in l.text:
            print(f"Link Text on {link} : {l.text}")
            daily_state_news =  {
                "State": state,
                "Buzz Word": "Mueller",
                "Website": link,
                "Time": datetime.datetime.now(),
                "Link Text": l.text
            }
            daily_news.insert_one(daily_state_news)
        elif "Democrat" in l.text:
            print(f"Link Text on {link} : {l.text}")
            daily_state_news =  {
                "State": state,
                "Buzz Word": "Democrat",
                "Website": link,
                "Time": datetime.datetime.now(),
                "Link Text": l.text
            }
            daily_news.insert_one(daily_state_news)
        elif "Republican" in l.text:
            print(f"Link Text on {link} : {l.text}")
            daily_state_news =  {
                "State": state,
                "Buzz Word": "Republican",
                "Website": link,
                "Time": datetime.datetime.now(),
                "Link Text": l.text
            }
            daily_news.insert_one(daily_state_news)
        else:
            continue

news = pd.DataFrame(list(daily_news.find({})))

news.head()
buzz_words = news['Buzz Word']
date_times = news['Time']
website_urls = news['Website']

N = 100
fig = go.Figure()
fig.add_scatter(x=date_times,
                y=buzz_words,
                mode='markers',
                fillcolor="black",
                hovertext= buzz_words,
                marker={'size': 12,
                        'color': "blue",
                        'opacity': 0.07,
                        'colorscale': 'Viridis'
                       });
iplot(fig)



