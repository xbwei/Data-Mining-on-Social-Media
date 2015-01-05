'''
Created on Nov 18, 2013

@author: Xuebin Wei

weixuebin@gmail.com

Department of Geography, UGA

'''



import twitter
import dbf
import logging
import traceback
from datetime import datetime 
import sys



# import urllib2
# print twitter.api


'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('GetTweets')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('GetTweets.log')
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
get current system time as CheckTimeValue
'''
CheckTime = datetime.now()
CheckTimeValue = str(CheckTime.year)[0:4]+"-"+str(CheckTime.month)+"-"+str(CheckTime.day)+"-"+str(CheckTime.hour)+"-"+str(CheckTime.minute)

FieldList = ["CheckTime","TeetID","Text","Lat","Lon","TeetTime","UserID","UserName"]
# field list


'''
OAUTH
fill your info
'''

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OATH_TOKEN_SECRET = ""

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OATH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


def GetTweetByContent():

    '''
    search tweet by content
    q define the content
    geo define the location
    '''
    try:
        tweet_id_list = []   
        tweet_text_list = []
        tweet_time_list = []
        tweet_lat_list = []
        tweet_log_list = []
        tweet_user_id = []
        tweet_user_name = []
        tweet_user_location = []
        
         
#         q= "UGA"
        count = 100
        lang = "en"
        # geocode of athens, GA with a specified radius
#         geocode = "33.9500,-83.3833,20mi" 
        # geocode of atlanga,GA with a specified radius
        geocode = "33.7550,-84.3900,20mi"     
        # geocode of family housing
#         geocode = "33.927444,-83.377326,1.5mi"
        # geocode of geography
#         geocode = "33.948864,-83.375218,1.5mi"
        search_results = twitter_api.search.tweets(count=count,lang=lang,geocode=geocode)
        # print json.dumps(search_results,indent=1)
        statuses = search_results["statuses"]
        # for statue in statuses:
        #     print statue["text"].encode('gbk','ignore')   
                    
        for _ in range(100):
        #     print "Length of statuses", len(statuses)
            try:
                next_results = search_results ["search_metadata"]["next_results"]
#                 print next_results
                
            except KeyError: #no more results when next result doesn't exist
                break
            kwargs = dict([kw.split("=") for kw in next_results[1:].split("&")])
        #     print kwargs
            search_results = twitter_api.search.tweets(**kwargs)
            statuses += search_results["statuses"]
        #     print statuses
        i=0    
        for statue in statuses:
            print "---------------" + str(i)
            print "ID      | " + str(statue["id"])  
            print "Text    | " + str(statue["text"].encode('gbk','ignore'))            
            print "Place   | " + str(statue["place"])
            print "Time    | " + str(statue["created_at"])
            print "Geo     | " + str(statue["geo"])
            print "Cord.   | " +str(statue["coordinates"])
            print "ID      | " + str(statue["user"]["id"])
            print "Name    | " + str(statue["user"]["screen_name"].encode('gbk','ignore'))
            print "Location| " + str(statue["user"]["location"].encode('gbk','ignore'))
            tweet_id_list.append(str(statue["id"]))
            tweet_text_list.append(str(statue["text"].encode('gbk','ignore')))
            tweet_time_list.append(str(statue["created_at"]))  
            tweet_user_id.append(str(statue["user"]["id"]))
            tweet_user_name.append(str(statue["user"]["screen_name"].encode('gbk','ignore')))
            tweet_user_location.append(str(statue["user"]["location"].encode('gbk','ignore')))  
            if statue["geo"]<>None:
                print "Lat     | " + str(statue["geo"]["coordinates"][0])
                print "Lon     | " + str(statue["geo"]["coordinates"][1])
                tweet_lat_list.append(str(statue["geo"]["coordinates"][0]))
                tweet_log_list.append(str(statue["geo"]["coordinates"][1]))
            else:
                tweet_lat_list.append("0.0")
                tweet_log_list.append("0.0")
            i = i+1
        return tweet_id_list,tweet_text_list,tweet_time_list,tweet_lat_list,tweet_log_list, tweet_user_id, tweet_user_name , tweet_user_location
        
        # print json.dumps(statuses[0],indent =1)    
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )


TweetIDList,TweetTextList,TweetTimeList,TweetLatList,TweetLonList,UserIDList,UserNameList,UserLocList = GetTweetByContent()

'''
try using dbf library to export a dbf table
'''
try:
    table = dbf.Table("Tweet.dbf")
    table.open()
    
    for i in range(len(TweetIDList)):
        try:
            datum = (TweetIDList[i],TweetTextList[i],TweetTimeList[i],TweetLatList[i],TweetLonList[i],UserIDList[i],UserNameList[i],UserLocList[i],CheckTimeValue)
            table.append(datum)
        except UnicodeDecodeError:
            print sys.exc_info()[1]
            logger.info (sys.exc_info()[1])
            continue
        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )
            continue
    
    table.close()
except :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print ''.join('!! ' + line for line in lines)  # Log it or whatever here
    logger.info(''.join('!! ' + line for line in lines) )


