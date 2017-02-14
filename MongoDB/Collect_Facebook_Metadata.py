'''
Created on Oct 19, 2016

@author: xuebin wei
@website: www.lbsocial.net
'''


from urllib import request
import json
from pprint import pprint


website_list = ['http://www.jmu.edu'] # place your list of website urls, e.g., http://jmu.edu
 
for website in website_list:
    url_str = 'https://graph.facebook.com/'+website # create the url for facebook graph api
   
    response = request.urlopen(url_str) # read the reponse into computer

    html_str = response.read().decode("utf-8") # convert the reponse into string

    json_data = json.loads(html_str) # convert the string into json
    pprint (json_data) 
    
    '''
    do something here
    '''
