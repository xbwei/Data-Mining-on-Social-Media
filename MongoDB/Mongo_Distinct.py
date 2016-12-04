'''
Created on Dec 2, 2016

@author: Xuebin Wei
www.lbsocial.net

Handle duplicate documents in mongodb
'''
import pymongo
from pymongo import MongoClient

client = MongoClient()

db = client.test
test_collection = db.test

'''
create another collection,
adding unique index based on the unique key
'''
unique_test_collection = db.unique_test_collection
unique_test_collection.create_index([("unique_id", pymongo.ASCENDING)],unique = True)




'''
copy the documents from the collection which has duplicate documents into the new collection
using try sentence to ignore duplicate errors
'''
cursor = test_collection.find()

for document in cursor:
    try:
        unique_test_collection.insert(document)
    except:
        pass
    
'''
print the new collection which only has unique documents
'''
cursor = unique_test_collection.find()

for document in cursor:
    print(document)