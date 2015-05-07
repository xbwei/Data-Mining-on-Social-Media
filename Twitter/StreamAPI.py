'''
Created on May 2, 2015

@author: xuebin
'''
import twitter
# import json
import sys
import logging
import traceback

import psycopg2
import time
# import urllib2
# print twitter.api


'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('StramAPI')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('StramAPI.log')
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




CONSUMER_KEY=""
CONSUMER_SECRET=""


OAUTH_TOKEN=""
OATH_TOKEN_SECRET=""

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OATH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)


twitter_api = twitter.Twitter(auth=auth)

def InsertStatus(search_results):
    '''
    insert tweet into postgresql table
    '''
    connection = psycopg2.connect(dbname = '', user = '',password='')
    cursor = connection.cursor()
    try:
        for statue in search_results:
#             print json.dumps(statue)
#             print statue
            if 'id_str' in statue:
                tweetid = statue["id_str"]
                print tweetid
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
                    
                if 'text' in statue:
                    
                    text = statue["text"].encode('utf-8','ignore')
                else:
                    text = None
                
                if statue["coordinates"]<>None:
                    lon = float(statue["coordinates"]["coordinates"][0])
                    lat = float(statue["coordinates"]["coordinates"][1])
    
                else:
                    lat = None
                    lon = None
    
                if statue["place"]<>None:
                    place_id = statue["place"]["id"]
                    place_fullname = statue["place"]["full_name"]
                else:
                    place_id = None
                    place_fullname = None
    
                try:
                    cursor.execute('SELECT tweetid FROM streamtweet WHERE tweetid ='  +"'"+str(tweetid)+"'")
                    test = cursor.fetchone()
    #                 print test
                    if (test):
                        print "duplicated tweet id: "+tweetid
                    else:
                        cursor.execute('INSERT INTO streamtweet (tweetid,tweetuser,year,month,day,time,hashtags,mention,replyuser,retweetuser,text,lat,lon,placeid,placename)'
                                                        'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                                        [tweetid,tweetuser,createyear,createmonth,createday,createtime,hashtags,mention,replyuser,retweetuser,text,lat,lon,place_id,place_fullname])
                except psycopg2.IntegrityError:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print "warning: duplicated tweetid"  # Log it or whatever here
                    logger.info(''.join('!! ' + line for line in lines) )
                    pass
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                    logger.info(''.join('!! ' + line for line in lines) )
                    continue
                
            connection.commit()
        cursor.close()
        connection.close()
        # return current month and year for date check


    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )


def streamAPI():
    try:
#         q = 'uga'
#        locations = "-83.40,33.93,-83.37,33.94 "
        locations = "-84.56,33.62,-84.20,33.91"
        
#         print >> sys.stderr,'Filtering the public timeline for track = "%s"' %(q)
        
        
        
        twitter_stream = twitter.TwitterStream(auth = twitter_api.auth)
#        print twitter_stream
        
        stream = twitter_stream.statuses.filter(locations = locations)
#        print stream

        InsertStatus(stream)

        


        
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        
streamAPI()