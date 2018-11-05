'''
Sentiment Analysis on Collected Tweets in MongoDB
 
@author: Xuebin Wei
@gmail: weixuebin@gmail.com
website: www.lbsocial.net

1.retrive data from mongodb
2.calculate sentiments of tweets with TextBlob
3.save the results in an Access table.
'''
import pymongo
from pymongo import MongoClient
import re
from textblob import TextBlob
import pyodbc  # using the pyodbc library 


'''
coonect access
'''
db_file = r'' #define the location of your Access file

odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(db_file) # define the odbc connection parameter

conn = pyodbc.connect(odbc_conn_str) # establish a database connection

cursor = conn.cursor() # create a cursor


'''
connect mongodb database
'''


client = MongoClient()

db = client.demo #change to your tweet database

tweet_collection = db.demo # change to your tweet collection
tweet_collection.create_index([("id", pymongo.ASCENDING)],unique = True) # add index 

tweet_cursor = tweet_collection.find()

for tweet in tweet_cursor:
    try:
        if tweet['text']:
            tweet_text =tweet['text']
            tweet_id = tweet['id']
    
            
            text_without_url = re.sub(r"http\S+", "", tweet_text)
            
            result = TextBlob(text_without_url)
            polarity = result.sentiment.polarity
            subjectivity = result.sentiment.subjectivity
    
            
            sql_insert_statement = "insert into tweet_sentiment(tweet_id,polarity,subjectivity) values({},{},{})".format(tweet_id,polarity,subjectivity) # edit the SQL statement that want to execute
    
            cursor.execute(sql_insert_statement) # execute the SQL statement
    
            cursor.commit() # let the database commit the changes in the tables
            print("inserting {}".format(tweet_id))

    except:

        pass
    

print('Done!')
cursor.close() # close the cursor
conn.close() # close the connection to the database
