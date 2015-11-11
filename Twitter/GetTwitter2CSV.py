'''
Created on Dec 29, 2014

@author: xuebin
'''
import twitter
# import json
import sys
import logging
import traceback
import csv
import json

import urllib2
# print twitter.api


'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('GetTwitter')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('GetTwitter.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


'''
OAUTH
'''

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OATH_TOKEN_SECRET = ""

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OATH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

csvfile = open('tweet.csv', 'w') 
fieldnames = ['tweetid','tweetuser','year','month','day','time','timestamp','hashtags','mention','replyuser','retweetuser','text','lat','lon']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def InsertStatus(search_results):
    '''
    insert tweet into postgresql table
    '''
     
        

    try:
        for statue in search_results:
#             print json.dumps(statue)
#             print statue
            tweetid = statue["id_str"]
            tweetuser = statue["user"]["screen_name"].encode('utf-8','ignore')
            collected_time = statue["created_at"]
            createyear = collected_time.split(" ")[5]
            createmonth = collected_time.split(" ")[1]
            createday = collected_time.split(" ")[2]
            createtime = collected_time.split(" ")[3]

#             print statue["entities"]["hashtags"]
            if len(statue["entities"]["hashtags"])>0:
#                 hashtags = json.dumps(statue["entities"]["hashtags"])
                hashtags = ''.join(hashtag["text"]+',' for hashtag in statue["entities"]["hashtags"])
            else:
                hashtags = None
            if len(statue["entities"]["user_mentions"])>0:
                mention = ''.join(user["screen_name"]+',' for user in statue["entities"]["user_mentions"])
#                 mention = json.dumps(statue["entities"]["user_mentions"])
            else:
                mention = None
            if statue["in_reply_to_screen_name"]:
                replyuser = statue["in_reply_to_screen_name"].encode('utf-8','ignore')
            else:
                replyuser = None
            if "retweeted_status" in statue:

                retweetuser = statue["retweeted_status"]["user"]["screen_name"].encode('utf-8','ignore')
            else:
                retweetuser = None
            text = statue["text"].encode('utf-8','ignore')
            if statue["geo"]<>None:
                lat = statue["geo"]["coordinates"][0]
                lon = statue["geo"]["coordinates"][1]
            else:
                lat = -999.99
                lon = -999.99

            try:
                
                writer.writerow({'tweetid': tweetid,
                                   'tweetuser': tweetuser,
                                   'year':createyear,
                                   'month':createmonth,
                                   'day':createday,
                                   'time':createtime,
                                   'timestamp':collected_time,
                                   'hashtags':hashtags,
                                   'mention':mention,
                                   'replyuser':replyuser,
                                   'retweetuser':retweetuser,
                                   'text':text,
                                   'lat':lat,
                                   'lon':lon
                                   })
#                     [tweetid,tweetuser,createyear,createmonth,createday,createtime,hashtags,mention,replyuser,retweetuser,text])

            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )
                continue
                



    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        

def getTWeet():
    try:
        count = 100
        lang = "en"
#         q = "WhatAFeeling"
        geocode = "38.435092,-78.8697548,50mi"     
        search_results = twitter_api.search.tweets(count=count,lang=lang,geocode=geocode)
        statuses = search_results["statuses"]
#         print json.dumps(search_results)
        next_url = search_results["search_metadata"]["next_results"]
        since_id = next_url.split("=")[1].split("&")[0]
#         print since_id

#         print len(statuses)

        for _ in range(0,20):
            search_results = twitter_api.search.tweets(count=count,lang=lang,geocode=geocode,max_id =since_id )
            next_url = search_results["search_metadata"]["next_results"]
            since_id = next_url.split("=")[1].split("&")[0]
#             print since_id
            
            statuses+=search_results["statuses"]
#             print "Length of statuses", len(statuses)

#             print len(statuses)
            
        InsertStatus(statuses)
        
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        
getTWeet()