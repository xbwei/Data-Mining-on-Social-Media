'''
Created on Nov 19, 2013

@author: Xuebin Wei

weixuebin@gmail.com

Department of Geography, UGA
'''

'''
Create initial table for tweet storing
'''

import dbf

table = dbf.Table("Tweet.dbf","TweetID C(20);TweetText C(200);TweetTime C(30); TweetLat C(30);TweetLon C(30);UserID C(30);UserName C(30);UserLoc C(30); CheckTime C(20)")

table.close()