'''
Created on Dec 29, 2014

@author: xuebin
This script can retrive historic tweet ID by sending request to https://twitter.com/search-advanced?lang=en
With the collected tweet ID, tweets can be downloaded by suing rest api
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
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import urllib2
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


twitter_user_list = []

def scrape_url(url):
    '''
    get tweet id from scrolling page
    '''
 
    # Load WebDriver and navigate to the page url.
    # This will open a browser window.
    driver = webdriver.Firefox()

    driver.get(url)
   
    tweetid_list = []
#     print driver.page_source.encode("utf-8")
 
    # First scroll to the end of the table by sending Page Down keypresses to
    # the browser window.
    try:
        for i in range(0,50):
    
                                           
                                           
            elem = driver.find_element_by_tag_name('li')
            elem.send_keys(Keys.PAGE_DOWN)
         
        # Once the whole table has loaded, grab all the visible tweetid.    
        tweetids = driver.find_elements_by_tag_name('li')
        for tweetid in tweetids:
            if tweetid.get_attribute('data-item-id') is not None:
                
                tweetid_list.append(tweetid.get_attribute('data-item-id'))
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        print url

         
    driver.quit()
           
    return tweetid_list

def getByBS4(url):
    
    '''
    use beautiful soup to extract tweetid from static webpage
    '''
    try:
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
        return tweetID
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
            
    


def GetTweetIDByName(name,start,end):
    '''
    get tweets ID from twitter.com/search
    by time and name
    return tweets ID 
    insert collected tweet ID into postgresql table
    '''
    try:
        name = name

        start = start

        end = end
        url = "https://twitter.com/search?f=realtime&q=from%3A"+name+"%20since%3A"+start+"%20until%3A"+end+"&src=typd"
        
        '''
        use beautiful soup to extract tweetid from static webpage
        '''

#         tweetID = getByBS4(url)

        '''
        use selenimu to extract tweetid from scrooling webpage
        '''
        tweetID = scrape_url(url) 
        
        
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
        for tweetid in tweetID:
            try:
                cursor.execute('SELECT tweetid FROM cpne.tweetid WHERE tweetid ='  +"'"+str(tweetid)+"'")
                test = cursor.fetchone()
    #                 print test
                if (test):
                    print "duplicated tweet id: "+tweetid
                else:
#                     print "start" +start
#                     print "end" + end
                    cursor.execute('INSERT INTO cpne.tweetid (tweetid,tweetuser,starttime,endtime)'
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
                
        print"\t total tweets from ",start," to",end,":", len(tweetID)
    #     print tweetID[0]
    #     print tweetID[len(tweetID)-1]
    #     print url
    #         print soup
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )

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
                cursor.execute('SELECT tweetid FROM cpne.tweet WHERE tweetid ='  +"'"+str(tweetid)+"'")
                test = cursor.fetchone()
#                 print test
                if (test):
                    print "duplicated tweet id: "+tweetid
                else:
                    cursor.execute('INSERT INTO cpne.tweet (tweetid,tweetuser,year,month,day,time,hashtags,mention,replyuser,retweetuser,text)'
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

def GetTweetIDbySearch():
    '''
    collect public tweets ID for each user day by day
    '''
 
    i = 0
    for tweet_user in tweet_user_list:
    #     print tweet_user

        i = i +1
        try:
            print "------- "+ str(i)
            print "get tweet of " + str(ngo_tweet)
            for month in range(1,13):
                print "\t month of: ",(month)
                for day in range(1,31):
                    GetTweetIDByName(tweet_user,'2015-'+str(month)+'-'+str(day),'2015-'+str(month)+'-'+str(day+1))

        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )
            continue
        
GetTweetIDbySearch()    
