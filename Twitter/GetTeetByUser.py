'''
Created on Dec 29, 2014

@author: xuebin
email: weixuebin@gmail.com
department of geography
university of Georgia
'''
import twitter
# import json
import sys
import logging
import traceback

from bs4 import BeautifulSoup
import urllib2
import psycopg2
import time

# import urllib2


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

ngo_tweet_list = [""]



def GetTweetIDByName(name,start,end):
    '''
    get real time tweets ID from twitter.com/search
    by time and name
    return tweets ID 
    insert collected tweet ID into postgresql table
    '''
    try:
        name = name

        start = start

        end = end

        
        # url = "https://twitter.com/search?q=lang%3Aen%20near%3A%22Athens%2CGA%22%20within%3A15mi&src=typd"
        url = "https://twitter.com/search?f=realtime&q=from%3A"+name+"%20since%3A"+start+"%20until%3A"+end+"&src=typd"
        tweets = urllib2.urlopen(url).read()
    
        # print tweets
        soup = BeautifulSoup(tweets)
        tweetID=[]
        # install the tweets ID
        
        # i=0
        for li in soup.find_all("li", attrs = {"data-item-type":"tweet"}):
        # find the li tag in which the name of data-item-type is tweet
        #     i = i+1
            tweetID.append(li["data-item-id"])
            # append the tweet id to the list
        # print i
        # # print tweetID
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
        for tweetid in tweetID:
            try:
                cursor.execute('SELECT tweetid FROM tweetid WHERE tweetid ='  +"'"+str(tweetid)+"'")
                test = cursor.fetchone()
    #                 print test
                if (test):
                    print "duplicated tweet id: "+tweetid
                else:
#                     print "start" +start
#                     print "end" + end
                    cursor.execute('INSERT INTO tweetid (tweetid,tweetuser,starttime,endtime)'
                                                    'VALUES(%s,%s,%s,%s)',
                                                    (tweetid,name,start,end,))
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
                    
            connection.commit()
        cursor.close()
        connection.close()
                
        print"\t total tweets", len(tweetID)
    #     print tweetID[0]
    #     print tweetID[len(tweetID)-1]
    #     print url
    #         print soup
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )

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

            try:
                cursor.execute('SELECT tweetid FROM tweet WHERE tweetid ='  +"'"+str(tweetid)+"'")
                test = cursor.fetchone()
#                 print test
                if (test):
                    print "duplicated tweet id: "+tweetid
                else:
                    cursor.execute('INSERT INTO tweet (tweetid,tweetuser,year,month,day,time,hashtags,mention,replyuser,retweetuser,text)'
                                                    'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                                    [tweetid,tweetuser,createyear,createmonth,createday,createtime,hashtags,mention,replyuser,retweetuser,text])
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
                
            connection.commit()
        cursor.close()
        connection.close()
        # return current month and year for date check
        return createmonth,createyear

    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )


def GetTweetFromUser(username):
    '''
    get tweet from user time line
    '''
    try:

        search_results = twitter_api.statuses.user_timeline(screen_name =username)
    except twitter.TwitterHTTPError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print  "rate limit exceeded" # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )
            time.sleep(900)
#         search_results = twitter_api.statuses.home_timeline(screen_name =username,contributor_details ='True')

#         statuses=search_results["statuses"]
#         json_result = json.dumps(search_results)
#         print json_result
    earliest_month, earliest_year = InsertStatus(search_results)
#     print earliest_month
    
    while(len(search_results)>1 and (earliest_month == "Dec" or earliest_month =="Nov" or earliest_month == "Oct" ) and (earliest_year == "2014" or earliest_year == "2015") ):
        '''
        use max_id to retrieve earlier tweets
        '''
        try:
#             print "\t later tweetid: %s", (search_results[0]["id_str"])
#             print "\t earlier tweetid: %s", (search_results[len(search_results)-1]["id_str"])
            print "\t current month: " , (earliest_month)
            try:
                search_results = twitter_api.statuses.user_timeline(screen_name =username,max_id =search_results[len(search_results)-1]["id_str"] )
            
            except twitter.TwitterHTTPError:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print  "rate limit exceeded" # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )
                time.sleep(900)
            
            earliest_month,earliest_year = InsertStatus(search_results)
        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )

        


# print len(ngo_tweet_list)
# GetTweetFromUser("xuebinwei")
def GetTweetIDbySearch():
    '''
    collect public tweets ID for each user day by day
    '''
 
    i = 0
    for ngo_tweet in ngo_tweet_list:
        i = i +1
        try:
            print "------- "+ str(i)
            print "get tweet of " + str(ngo_tweet)
            for month in range(10,12):
                print "\t month of: ",(month)
                for day in range(1,31):
                    GetTweetIDByName(ngo_tweet,'2014-'+str(month)+'-'+str(day),'2014-'+str(month)+'-'+str(day+1))
    #         GetTweetFromUser(ngo_tweet)
        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )
            continue
        
# GetTweetIDbySearch()        

        
def GetTweetbyREST():
    '''
    collect tweets of each user 
    '''
    i = 0
    for ngo_tweet in ngo_tweet_list:
        i = i +1
        try:
            print "------- "+ str(i)
            print "get tweet of " + str(ngo_tweet)
            GetTweetFromUser(ngo_tweet)
        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )
            continue
GetTweetbyREST()
