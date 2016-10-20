'''
Created on Oct 19, 2016

@author: xuebin wei
@website: www.lbsocial.net
'''


import pymongo
from pymongo import MongoClient

import urllib2
import json

client = MongoClient()

db = client.db_demo 

collection_demo = db.collection_demo

website_list = [] # place your list of website urls, e.g., http://www.cnn.com
 
for website in website_list:
    url_str = 'https://graph.facebook.com/'+website
   
    response = urllib2.urlopen(url_str)
       
    json_data= json.load(response)
    # print json_data
       
    collection_demo.insert(json_data)


cursor = collection_demo.find()
for document in cursor:
    print (document)