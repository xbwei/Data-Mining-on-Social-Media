'''
Created on Oct 25, 2016

@author: weixx
'''

import pymongo
from pymongo import MongoClient
import json

import tweepy
#override tweepy.StreamListener to add logic to on_status

from pprint import pprint
import sys


'''
OAUTH
'''

CONSUMER_KEY      = "" # fill your oauth
CONSUMER_SECRET   = "" # fill your oauth
OAUTH_TOKEN       = "" # fill your oauth
OATH_TOKEN_SECRET = "" # fill your oauth

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OATH_TOKEN_SECRET)

api = tweepy.API(auth)


'''
connect mongodb database
'''
      

client = MongoClient()

db = client.tweet_db

tweet_collection = db.tweet_collection


'''
define query in Stream API
'''

track = ['election']

locations = [-84.56,33.62,-84.20,33.91]

'''
fetch data
'''

# class MyStreamListener(tweepy.StreamListener):
#   
#     def on_status(self, status):
#         print (status.id_str)
#         tweet_collection.insert(status._json)
#   
#   
#     def on_error(self, status_code):
#         if status_code == 420:
#             #returning False in on_data disconnects the stream
#             return False
#   
# myStreamListener = MyStreamListener()
#   
#   
# myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#   
#   
# myStream.filter(track=track, locations = locations, async=True)



'''
query collected data in MongoDB
'''
 
tweet_cursor = tweet_collection.find()
    
print (tweet_cursor.count())
    
user_cursor = tweet_collection.distinct("user.id")
    
    
print (len(user_cursor))
   
   
    
for document in tweet_cursor:
    try:
        print ('----')      
#         pprint (document)
 
    
        print ('name:', document["user"]["name"])
        print ('text:', document["text"])
    except:
        print ("***error in encoding")

        pass
#      