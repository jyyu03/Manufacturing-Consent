
# coding: utf-8

# In[185]:


# bulk of Dependencies
import tweepy
import base64
import pandas as pd
import requests
import time
import json
import dateutil.parser as parser
# API Keys
from config import (consumer_key, 
                    consumer_secret, 
                    access_token, 
                    access_token_secret)
from config2 import geo_api_key
from flask import Flask, jsonify, render_template
import pymongo


# In[186]:


#set up connection to mlab
import pymongo
app = Flask(__name__)
DB_NAME = 'manufacture_consent'
DB_HOST = 'ds255403.mlab.com'
DB_PORT =  55403
DB_USER = 'edwardwisejr'
DB_PASS = 'Flender77!'
connection = pymongo.MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)


# In[76]:


# get bearer token for twitter api
bearer_token_credentials = base64.urlsafe_b64encode(
    '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')).decode('ascii')
url = 'https://api.twitter.com/oauth2/token'
headers = {
    'Authorization': 'Basic {}'.format(bearer_token_credentials),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
}
data = 'grant_type=client_credentials'
response = requests.post(url, headers=headers, data=data)
response_data = response.json()
if response_data['token_type'] == 'bearer':
    bearer_token = response_data['access_token']
else:
    raise RuntimeError('unexpected token type: {}'.format(response_data['token_type']))


# In[95]:


#fromDate= '201811210000'
#toDate= '201811220000'

endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json" 
headers = {"Authorization":'Bearer {}'.format(bearer_token), "Content-Type": "application/json"}  
data ='{"query":"drain swamp place:wisconsin", "fromDate": "201602010000", "toDate": "201602280000"}' 
#'{"query":"clinton email place:wisconsin", "fromDate": "201811210000", "toDate": "201811220000"}' 
#''{query:{} place:wisconsin, fromDate: {}, toDate: {}}".format(quer, fromDate, toDate) 
public_tweets = requests.post(endpoint,data=data,headers=headers).json()


# In[108]:


endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json" 
headers = {"Authorization":'Bearer {}'.format(bearer_token), "Content-Type": "application/json"}  
data ='{"query":"economy place:wisconsin", "fromDate": "201611010000", "toDate": "201611300000"}' 
#'{"query":"clinton email place:wisconsin", "fromDate": "201811210000", "toDate": "2018112320000"}' 
#''{query:{} place:wisconsin, fromDate: {}, toDate: {}}".format(quer, fromDate, toDate) 
public_tweets = requests.post(endpoint,data=data,headers=headers).json()

locations_collection = db['mc_locations']
locations = locations_collection.find({}, {"location": 1, "_id": 0}).distinct("location")
query = "economy"
new_locations=[]
events = {}
tweets_collection = db['mc_tweets']
import pprint as pp
for tweet in public_tweets['results']:
    if tweet['user']['location'] not in locations:
        new_locations.append(tweet['user']['location'])
    if 'retweeted_status' not in tweet:
        if 'extended_tweet' in tweet:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['extended_tweet']['full_text']
                ,"location":tweet['user']['location']
                ,"retweet_location": None
                ,"retweet_user": None
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
        else:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['text']
                ,"location":tweet['user']['location']
                ,"retweet_location": None
                ,"retweet_user": None
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
                
    else:
        if 'extended_tweet' in tweet:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['extended_tweet']['full_text']
                ,"location":tweet['user']['location']
                ,"retweet_location":tweet['retweeted_status']['user']['location']
                ,"retweet_user":tweet['retweeted_status']['user']['name']
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
        else:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['text']
                ,"location":tweet['user']['location']
                ,"retweet_location":tweet['retweeted_status']['user']['location']
                ,"retweet_user":tweet['retweeted_status']['user']['name']
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
geojson = []
place=[]
places={}


for location in new_locations:
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(location)
    geocode_url = geocode_url + "&key={}".format(geo_api_key)
    results = requests.get(geocode_url)
    results = results.json()
    for place in results['results']:
        if len(place) > 0:
            spot={
            "location": location
            ,"lat": str(place['geometry']['location']['lat']) 
            ,"long": str(place['geometry']['location']['lng'])
            ,"address": place['formatted_address']}
            post_id = locations_collection.insert_one(spot).inserted_id


# In[97]:


for location in new_locations:
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(location)
    geocode_url = geocode_url + "&key={}".format(geo_api_key)
    results = requests.get(geocode_url)
    results = results.json()
    for place in results['results']:
        if len(place) > 0:
            spot={
            "location": location
            ,"lat": str(place['geometry']['location']['lat']) 
            ,"long": str(place['geometry']['location']['lng'])
            ,"address": place['formatted_address']}
            post_id = locations_collection.insert_one(spot).inserted_id


# In[1]:


#records = json.loads(df.T.to_json()).values()
#db.myCollection.insert(records)
tweets_df=pd.DataFrame(list(tweets_collection.find({})))
tweets_df


# In[115]:


places_df = pd.DataFrame(list(locations_collection.find({})))
locations_collection = db['mc_locations']
locations = locations_collection.find({}, {"location": 1, "_id": 0}).distinct("location")
query = "wall/immigration"
new_locations=[]
events = {}
tweets_collection = db['mc_tweets']


# In[190]:


locations_collection = db['mc_locations']
locations_df = pd.DataFrame(list(locations_collection.find({})))
tweets_collection=db['mc_tweets']
tweets_df =pd.DataFrame(list(tweets_collection.find({})))

tweets_to_plot_df = pd.merge(tweets_df,places_df,on="location",how="left")
tweets_to_plot_df = tweets_to_plot_df[['buzz_word','date','source','lat','long']]
#tweets_to_plot_json = tweets_to_plot_df.to_json(orient='index')
# with open('data.txt', 'w') as outfile:  
#     json.dump(tweets_to_plot_json , outfile)
tweets_to_plot_df.to_csv(test.csv)


# In[118]:


records = json.loads(tweets_to_plot_df.T.to_json()).values()
db.mc_tweets_to_plot.insert(records)


# In[36]:


#tweets_collection = db['mc_tweets']tweets_df

tweets_collection = db['mc_tweets']
tweets=pd.DataFrame(list(tweets_collection.find({})))
tweets['name'] = tweets['name'] .apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))
tweets['text'] = tweets['text'] .apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))     
tweets = tweets[['buzz_word','text','date','location','name','retweet_location','retweet_user','screen_name','source','year']]


# In[37]:


records = json.loads(tweets.to_json()).values()


# In[50]:


db.mc_test.insert(records)


# In[156]:


#test =db.mc_test.find(filter={"location": "Massachusetts"})
tweets_collection=db['mc_tweets']
#tweets_collection.update_many({"buzz_word":"wall/immigration"},{ '$set': { "buzz_word": "wall or immigration" }})
tweets_df =pd.DataFrame(list(tweets_collection.find({"screen_name":"wxow"})))
tweets_df


# In[ ]:


"@kbjr6news" OR "@WAOW" OR "@MeTV" OR "@nbc26" OR "@fox6now" OR "@WKOW" OR "@wqow" OR "@tmj4" OR "@tbn" OR "@wxow"


# In[157]:


#endpoint2 = "https://api.twitter.com/1.1/tweets/search/30day/dev.json" 
headers = {"Authorization":'Bearer {}'.format(bearer_token), "Content-Type": "application/json"}  
data ='{"query":"@kbjr6news", "fromDate": "201611010000", "toDate": "201611300000"}' 
#'{"query":"clinton email place:wisconsin", "fromDate": "201811210000", "toDate": "2018112320000"}' 
#''{query:{} place:wisconsin, fromDate: {}, toDate: {}}".format(quer, fromDate, toDate) 
public_tweets = requests.post(endpoint,data=data,headers=headers).json()
public_tweets


# In[ ]:


public_tweets


# In[169]:


endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json" 
headers = {"Authorization":'Bearer {}'.format(bearer_token), "Content-Type": "application/json"}  
data ='{"query":"economy from:kbjr6news", "fromDate": "201601010000", "toDate": "201611300000"}' 
#'{"query":"clinton email place:wisconsin", "fromDate": "201811210000", "toDate": "2018112320000"}' 
#''{query:{} place:wisconsin, fromDate: {}, toDate: {}}".format(quer, fromDate, toDate) 
public_tweets = requests.post(endpoint,data=data,headers=headers).json()

locations_collection = db['mc_locations']
locations = locations_collection.find({}, {"location": 1, "_id": 0}).distinct("location")
query = "clinton email or hillary email"
new_locations=[]
events = {}
tweets_collection = db['mc_test']
import pprint as pp
for tweet in public_tweets['results']:
    if tweet['user']['location'] not in locations:
        new_locations.append(tweet['user']['location'])
    if 'retweeted_status' not in tweet:
        if 'extended_tweet' in tweet:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['extended_tweet']['full_text']
                ,"location":tweet['user']['location']
                ,"retweet_location": None
                ,"retweet_user": None
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
        else:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['text']
                ,"location":tweet['user']['location']
                ,"retweet_location": None
                ,"retweet_user": None
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
                
    else:
        if 'extended_tweet' in tweet:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['extended_tweet']['full_text']
                ,"location":tweet['user']['location']
                ,"retweet_location":tweet['retweeted_status']['user']['location']
                ,"retweet_user":tweet['retweeted_status']['user']['name']
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
        else:
            stuff ={
                  "buzz_word": query
                    , "source": "Public"
                ,"date":time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                , "year":parser.parse(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))).year
                ,"name":tweet['user']['name']
                ,"screen_name":tweet['user']['screen_name']
                ,"text":tweet['text']
                ,"location":tweet['user']['location']
                ,"retweet_location":tweet['retweeted_status']['user']['location']
                ,"retweet_user":tweet['retweeted_status']['user']['name']
                #,"place": tweet['place']['name']
                }
            events[tweet['id']]=stuff
            post_id = tweets_collection.insert_one(stuff).inserted_id
geojson = []
place=[]
places={}
stuff


# In[170]:


public_tweets


# In[172]:


import plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

N = 40
x = np.linspace(0, 1, N)
y = np.random.randn(N)
df = pd.DataFrame({'x': x, 'y': y})
df.head()

data = [
    go.Bar(
        x=df['x'], # assign x as the dataframe column 'x'
        y=df['y']
    )
]

# IPython notebook
# py.iplot(data, filename='pandas-bar-chart')

url = py.plot(data, filename='pandas-bar-chart')


# In[197]:


data=db['mc_tweets_to_plot']
data_df =pd.DataFrame(list(data.find({})))

#tweets_to_plot_json = tweets_to_plot_df.to_json(orient='index')
# with open('data.txt', 'w') as outfile:  
#     json.dump(tweets_to_plot_json , outfile)
data_df.to_csv('twitterdata.csv')

