'''
Created on Oct 18, 2016

@author: Xuebin Wei
@website: www.lbsocial.net
'''
import pymongo
from pymongo import MongoClient

import urllib
from urllib import request
import json


client = MongoClient()

db = client.db_demo 

collection_demo  = db.collection_demo 


# insert data

url_str = 'https://graph.facebook.com/http://www.jmu.edu'

response = request.urlopen(url_str)

html_str = response.read().decode("utf-8") 


json_data = json.loads(html_str)
collection_demo.insert(json_data)

cursor = collection_demo.find()
 
for document in cursor:
    print (document)

''' 
# query data
cursor = collection_demo.find().sort("share.share_count", pymongo.DESCENDING)
                                     
 
for document in cursor:
    print (document)

'''


'''
# update data
collection_demo.update_one(
                            {"id":"http://www.uga.edu"},
                            {"$set":{"og_object.title":"uga"} }
                            )

cursor = collection_demo.find({"id":"http://www.uga.edu"})
for document in cursor:
    print (document)

'''


'''
# delete data


result = collection_demo.delete_many({"id":"http://www.jmu.edu"})
print result.deleted_count
cursor = collection_demo.find()
for document in cursor:
    print (document)

'''

'''
# aggregate data

cursor = collection_demo.aggregate(
                                    [{"$group":
                                    {"_id":"$og_object.type",
                                     "count":{"$sum":1}}}]
                                    )
                                     
for document in cursor:
    print (document)
'''

'''
# create index

collection_demo.create_index([
                               ("share.comment_count", pymongo.ASCENDING),
                               ("share.share_count", pymongo.ASCENDING)
                               ])
'''                               
    
