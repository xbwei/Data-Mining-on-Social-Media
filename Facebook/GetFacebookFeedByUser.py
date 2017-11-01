'''
Created on Nov 1, 2017

@author: xuebin wei
email: weixuebin@gmail.com
website:www.lbsocial.net
'''

import facebook
import json
from urllib import request
import pymongo
from pymongo import MongoClient
from pprint import pprint


client = MongoClient() # fill in your mongodb server setting

db = client.gpdemo #use your mongodb database name

db_collection = db.facebook_collection #use your mongodb collection name
db_collection.create_index([("id", pymongo.ASCENDING)],unique = True)

# get your token from https://developers.facebook.com
ACCESS_TOKEN = ""

g= facebook.GraphAPI(ACCESS_TOKEN)

user_id = '' # the id of the Facebook user
name = g.get_object(user_id)["name"]
print (name)


'''
collect the data
'''

feeds = g.get_connections(user_id,'feed')
 
 
 
for feed in feeds['data']:
    try:
        db_collection.insert(feed)
        print (feed['id'])
    except:
        pass
 
'''
the following part will collect the data from all previous pages 
'''
if 'paging' in feeds:
    next_page = feeds['paging']['next']
     
    while next_page:
        response = request.urlopen(next_page)
         
         
        html_str = response.read().decode("utf-8") 
        feeds = json.loads(html_str)
     
         
        for feed in feeds['data']:
            try:
                db_collection.insert(feed)
                print (feed['id'])
            except:
                pass
 
        if 'paging' in feeds:
            next_page = feeds['paging']['next']
        else:
            next_page = None


'''
query the data
'''
print (db_collection.count())
feeds = db_collection.find()
for feed in feeds:
    try:
        pprint (feed)
    except:
        pass
