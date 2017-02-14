'''
Created on Oct 19, 2016

@author: xuebin wei
@website: www.lbsocial.net
'''


import pymongo
from pymongo import MongoClient

import urllib
from urllib import request
import json

client = MongoClient()

db = client.db_demo 

collection_demo = db.collection_demo

website_list = [] # place your list of website urls, e.g., http://www.cnn.com
 
for website in website_list:
    url_str = 'https://graph.facebook.com/'+website
   
    response = request.urlopen(url_str)

    html_str = response.read().decode("utf-8") 


    json_data = json.loads(html_str)
    collection_demo.insert(json_data)
   
   
    


cursor = collection_demo.find()
for document in cursor:
    print (document)