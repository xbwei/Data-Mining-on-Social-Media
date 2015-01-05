'''
Created on Jan 3, 2015

@author: xuebin
email: weixuebin@gmail.com
department of geography
university of Georgia
'''
import sys
import logging
import traceback

# from bs4 import BeautifulSoup
import urllib2
import psycopg2
import time
import facebook
import json
import urllib

'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('GetFacebook')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('GetFacebook.log')
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

ACCESS_TOKEN = ""

g= facebook.GraphAPI(ACCESS_TOKEN)

ngo_facebook_list = [""]


def GetFeed(ngo):
    try:

    #     print json.dumps(g.get_connections(ngo,'posts'))
    #     print json.dumps(g.get_connections(ngo,'photos'))
    
    #     print ngo," :",g.get_object(ngo)["name"]
    #     print json.dumps(g.get_connections(ngo,'statuses'))
        '''
        Get facebook feed for ngo facebook user
        insert feed into postgresql table
        '''
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
        ngo_name = g.get_object(ngo)["name"]
        feeds = g.get_connections(ngo,'feed')
		# since parameter doesn't work for me 
		
#         print json.dumps(feeds)
        test_feed = feeds["data"][0]["created_time"][5:7]
        create_month = test_feed
        
        while (feeds["data"] and int(create_month)<>9):
            try:
        #         print "\t current month: ", create_month
                paging = feeds ["paging"]["next"]
                for feed in feeds["data"]:
                    try:
            #             print'----'
                        fromuser = feed["from"]["name"].encode('utf-8','ignore')
            #             print fromuser
                        if "to" in feed:
                            if "paging"in feed["to"]:
                                if "next" in feed["to"]["paging"]:
                                    while(feed["to"]["data"]):
                                        if "next" in feed["to"]["paging"]:
                                            topaging = feed["to"]["paging"]["next"]
                    
                                            to_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["to"]["data"])
                    
                                            toreq = urllib2.urlopen(topaging,timeout = 600)
                                            feed["to"] = json.load(toreq)
                                            print "\t \t number of to users: ", len(feed["to"]["data"])
                                            print "\t to user:", feed["to"]["data"]
                                        else:
                                            to_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["to"]["data"])
                                            feed["to"]["data"]=None
            
                                else:
                                    to_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["to"]["data"])
                            else:
                                to_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["to"]["data"])
                                
            
            #                 print to_users
                        else:
                            to_users = None
                            
                        if "tags" in feed:
                            print json.dumps(feed["tags"])
                            if "paging"in feed["tags"]:
                                if "next" in feed["tags"]["paging"]:
                                    while(feed["tags"]):
                                        if "next" in feed["tags"]["paging"]:
                                            tagpaging = feed["tags"]["paging"]["next"]
                    
                                            default_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["tags"])
                    
                                            tagreq = urllib2.urlopen(tagpaging,timeout = 600)
                                            feed["tags"] = json.load(tagreq)
                                            print "\t \t number of default tags user", len(feed["tags"])
                                            print "\t tags user:", feed["tags"]
                                        else:
                                            default_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed)
                                            feed["tags"]=None
            
                                else:
                                    default_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["tags"])
                            else:
                                default_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["tags"])
                                
            
            #                 print to_users
                        else:
                            default_tag_users = None
                            
                        if "message_tags" in feed:
#                             print json.dumps(feed["message_tags"])
#                             for key in feed["message_tags"]:
#                                 print key
#                                 print feed["message_tags"][str(key)][0]["name"]
                            if "paging"in feed["message_tags"]:
                                if "next" in feed["message_tags"]["paging"]:
                                    while(feed["message_tags"]):
                                        if "next" in feed["message_tags"]["paging"]:
                                            tagpaging = feed["message_tags"]["paging"]["next"]
                    
                                            message_tag_users= ''.join(feed["message_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["message_tags"])
                    
                                            tagreq = urllib2.urlopen(tagpaging,timeout = 600)
                                            feed["message_tags"] = json.load(tagreq)
                                            print "\t \t number of message_tags user", len(feed["message_tags"])
                                            print "\t tags user:", feed["message_tags"]
                                        else:
                                            message_tag_users= ''.join(feed["message_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["message_tags"])
                                            feed["message_tags"]=None
            
                                else:
                                    message_tag_users= ''.join(feed["message_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["message_tags"])
                            else:
                                message_tag_users= ''.join(feed["message_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["message_tags"])
                                
            
            #                 print to_users
                        else:
                            message_tag_users = None
        #                     print "\t no tags"
                        if "story_tags" in feed:
#                             print json.dumps(feed["story_tags"])
                            if "paging"in feed["story_tags"]:
                                if "next" in feed["story_tags"]["paging"]:
                                    while(feed["story_tags"]):
                                        if "next" in feed["story_tags"]["paging"]:
                                            tagpaging = feed["story_tags"]["paging"]["next"]
                    
                                            story_tag_users= ''.join(feed["story_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["story_tags"])
                    
                                            tagreq = urllib2.urlopen(tagpaging,timeout = 600)
                                            feed["story_tags"] = json.load(tagreq)
                                            print "\t \t number of story_tags user", len(feed["story_tags"])
                                            print "\t tags user:", feed["story_tags"]
                                        else:
                                            story_tag_users= ''.join(feed["story_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["story_tags"])
                                            feed["story_tags"]=None
            
                                else:
                                    story_tag_users= ''.join(feed["story_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["story_tags"])
                            else:
                                story_tag_users= ''.join(feed["story_tags"][str(key)][0]["name"].encode('utf-8','ignore')+',' for key in feed["story_tags"])
                                
                        else:
                            story_tag_users = None
                            
                        if "name_tags" in feed:
                            print json.dumps(feed["name_tags"])
                            if "paging"in feed["name_tags"]:
                                if "next" in feed["name_tags"]["paging"]:
                                    while(feed["name_tags"]):
                                        if "next" in feed["name_tags"]["paging"]:
                                            tagpaging = feed["name_tags"]["paging"]["next"]
                    
                                            photo_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["name_tags"])
                    
                                            tagreq = urllib2.urlopen(tagpaging,timeout = 600)
                                            feed["name_tags"] = json.load(tagreq)
                                            print "\t \t number of name_tags user", len(feed["name_tags"])
                                            print "\t tags user:", feed["name_tags"]
                                        else:
                                            photo_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["name_tags"])
                                            feed["name_tags"]=None
            
                                else:
                                    photo_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["name_tags"])
                            else:
                                photo_tag_users= ''.join(to_user["name"].encode('utf-8','ignore')+',' for to_user in feed["name_tags"])
                                
            
            #                 print to_users
                        else:
                            photo_tag_users = None      
#                             print "\t no tags"

                        '''
                        record liked users
						some posts may have thousands of likes
                        '''
        #                 if "likes" in feed:
        #                     if "next" in feed["likes"]["paging"]:
        #                         while(feed["likes"]["data"]):
        #                             if "next" in feed["likes"]["paging"]:
        #                                 likepaging = feed["likes"]["paging"]["next"]
        #         
        #                                 feed_likes= ''.join(feed_like["name"].encode('utf-8','ignore')+',' for feed_like in feed["likes"]["data"])
        #         
        #                                 likereq = urllib2.urlopen(likepaging,timeout = 600)
        #                                 feed["likes"] = json.load(likereq)
        #                                 print "\t \t number of likes", len(feed["likes"]["data"])
        # #                                 print  "\t like user:", feed["likes"]["data"]
        #                             else:
        #                                 feed_likes= ''.join(feed_like["name"].encode('utf-8','ignore')+',' for feed_like in feed["likes"]["data"])
        #                                 feed["likes"]["data"]=None
        # 
        #                     else:
        #                         feed_likes= ''.join(feed_like["name"].encode('utf-8','ignore')+',' for feed_like in feed["likes"]["data"])
        # 
        #     #                 print feed_likes
        #                 else:
        #                     feed_likes = None
                        feed_likes = None
        
                            
                        if "comments" in feed:
                            if "next" in feed["comments"]["paging"]:
                                while(feed["comments"]["data"]):
                                    if "next" in feed["comments"]["paging"]:
                                        commentpaging = feed["comments"]["paging"]["next"]
                
                                        comments= ''.join(comment["from"]["name"].encode('utf-8','ignore')+',' for comment in feed["comments"]["data"])
                
                                        commentreq = urllib2.urlopen(commentpaging,timeout = 600)
                                        feed["comments"] = json.load(commentreq)
                                        print "\t \t number of comments", len(feed["comments"]["data"])
        #                                 print  "\t comments user:", feed["comments"]["data"]
                                    else:
                                        comments= ''.join(comment["from"]["name"].encode('utf-8','ignore')+',' for comment in feed["comments"]["data"])
                                        feed["comments"]["data"]=None
        
                            else:
                                comments= ''.join(comment["from"]["name"].encode('utf-8','ignore')+',' for comment in feed["comments"]["data"])
        
            #                 print comments
                        else:
                            comments = None
                        feedid = feed["id"]
            #             print feedid
                        create_timestamp = feed["created_time"]
                        print '\t ' + create_timestamp
                        create_year= create_timestamp[:4]
                        create_month= create_timestamp[5:7]
                        create_day= create_timestamp[8:10]
                        create_time= create_timestamp[11:16]
            
            #             print create_time
                        if "type" in feed:
                            feed_type=feed["type"]
                        else:
                            feed_type = None
            #             print feed_type
                        if "message" in feed:
                            feed_text = feed["message"].encode('utf-8','ignore')
            #                 print feed_text
                        else:
                            feed_text = None
                        if "story" in feed:
                            feed_story = feed["story"].encode('utf-8','ignore')
            #                 print feed_story
                        else:
                            feed_story = None
            
                        
                        cursor.execute('SELECT feedid FROM facebookfeed WHERE feedid ='  +"'"+str(feedid)+"'")
                        test = cursor.fetchone()
            #                 print test
                        if (test):
                            print "duplicated feed id: "+feedid
                        else:
                            cursor.execute('INSERT INTO facebookfeed (feedid,text,fromuser,commentuser,defaulttag,messagetag,storytag,phototag,ngo,touser,type,story,likeuser,year,month,day,time)'
                                                            'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                                            (feedid,feed_text,fromuser,comments,default_tag_users,message_tag_users,story_tag_users,photo_tag_users,ngo_name,to_users,feed_type,feed_story,feed_likes,create_year,create_month,create_day,create_time,))
                            
                    except psycopg2.IntegrityError:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                        print "warning: duplicated feedid"  # Log it or whatever here
                        logger.info(''.join('!! ' + line for line in lines) )
                        pass
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                        logger.info(''.join('!! ' + line for line in lines) )
                    
                    connection.commit()
                req = urllib2.urlopen(paging,timeout = 600)
                feeds = json.load(req)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )
                
        cursor.close()
        connection.close()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
# GetFeed("")
        
# print len(ngo_facebook_list)
def CollectFacebookFeed():
    for ngo in ngo_facebook_list:
        print "get feeds from: ",ngo
        
        GetFeed(ngo)
        
CollectFacebookFeed()