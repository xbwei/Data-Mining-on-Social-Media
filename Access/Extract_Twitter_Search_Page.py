'''
Created on Oct 30, 2016

@author: xuebin Wei
@website: www.lbsocial.net
'''

import pyodbc  # using the pyodbc library 
from bs4 import BeautifulSoup
from urllib import request

'''
Use bs4 to read webpage
'''

url_str = '' # fill in your search url from Twitter Search
response = request.urlopen(url_str)
html_data = response.read()
soup = BeautifulSoup(html_data,"html.parser")


'''
Connect to Access
'''
db_file = '' #define the location of your Access file

odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(db_file) 
conn = pyodbc.connect(odbc_conn_str) 
cursor = conn.cursor() 

'''
use bs4 to extract data
'''

num_web = 0
num_tweet = 0
num_user = 0

for  li in soup.find_all("li", attrs = {"data-item-type":"tweet"}):
    print ("-----")
    print (li["data-item-id"])
    tweet_id = li["data-item-id"]
    for div_cont in li.find_all("div",attrs = {"class":"content"}):
        for div_header in div_cont.find_all("div",attrs = {"class":"stream-item-header"}):
            for a_head in div_header.find_all("a", attrs = {"class":"account-group js-account-group js-action-profile js-user-profile-link js-nav"}):

                user_id = a_head["data-user-id"]
                for span_head in a_head.find_all("span",attrs = {"class":"username js-action-profile-name"}):
                    for b_head in span_head.find_all("b"):
                        user_name = b_head.string
                      
            for a_time in  div_header.find_all("a", attrs = {"class":"tweet-timestamp js-permalink js-nav js-tooltip"}):
                tweet_time = a_time["title"]
               
        for div_container in div_cont.find_all("div",attrs = {"class":"js-tweet-text-container"}):
            for p_container in div_container.find_all("p"):
                tweet_text = p_container.text
                
    num_web = num_web + 1
    
    '''
    save extracted data into Access
    '''
    
    sql_insert_user_statement = """insert into user (UserID,UserName) values (%s,%s)""" %(user_id, "'" +user_name+"'") 
                            

    try:
        cursor.execute(sql_insert_user_statement) 
        cursor.commit()
        num_user = num_user +1
        
    except: 
        print ('***error in inserting user name')
        pass

    sql_insert_tweet_statement ="""insert into tweet (TweetID, TweetText, UserID,TweetTime) values (%s,%s,%s,%s)"""\
                            %(tweet_id, "'"+ tweet_text+"'",user_id,"'"+ tweet_time+"'") 
    
                            

    try:
        cursor.execute(sql_insert_tweet_statement) 
        cursor.commit() 
        num_tweet = num_tweet+1
        
    except:
        print ('***error on inserting tweet')
        pass

cursor.close() 
conn.close() 
'''
print summary
'''

print ('=========')
print (num_web ," web records being collected")
print (num_user ," twitter users being inserted")
print (num_tweet ," tweets being inserted")
