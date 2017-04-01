'''
Created on Mar 31, 2017

@author: xuebin wei
www.lbsocial.net
'''

import twitter
from pprint import pprint

'''
OAuth
'''

CONSUMER_KEY      = "" 
CONSUMER_SECRET   = ""
OAUTH_TOKEN       = ""
OATH_TOKEN_SECRET = ""

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OATH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


'''
define query in REST API
'''
 
count = 100
geocode = ""
 
q= ''

'''
fetch data
'''
  
search_results = twitter_api.search.tweets( q=q, count=count,geocode=geocode)
         
statuses = search_results["statuses"]

'''
write data into a text file
'''
    
with open('tweet.txt', 'ba') as outfile:
    for statuse in statuses:
        try:
            print('---------------------')
            pprint(statuse)
            outfile.write(statuse['text'].encode('utf-8'))
        except:
            pass
