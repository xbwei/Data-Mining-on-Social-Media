'''
Created on Jan 29, 2018

@author: Xuebin Wei
www.lbsocial.net

this python code collects json data from https://www.census.gov/data/developers/data-sets/acs-1year.html
example of urls: https://api.census.gov/data/2016/acs/acs1.html
definition of variables: https://api.census.gov/data/2016/acs/acs1/variables.html
census state code:https://www.census.gov/geo/reference/ansi_statetables.html
census cunty code:https://www.census.gov/geo/reference/codes/cou.html
get your key from https://api.census.gov/data/key_signup.html

'''


from urllib import request
import json
# from pprint import pprint
import xlwt
# import xlrd
# from xlutils.copy import copy

census_api_key = '' #get your key from https://api.census.gov/data/key_signup.html
 
 
url_str = 'https://api.census.gov/data/2016/acs/acs5?get=B01001_001E,B01001_002E,NAME&for=county:*&in=state:51&key='+census_api_key # create the url of your census data
 
response = request.urlopen(url_str) # read the response into computer
 
 
book = xlwt.Workbook() # create a new excel file
sheet_test = book.add_sheet('test') # add a new sheet named test
html_str = response.read().decode("utf-8") # convert the response into string
i = 0 
if (html_str):
    json_data = json.loads(html_str) # convert the string into json
    for row in json_data:
        cl1, cl2, cl3, cl4,cl5 =row
 
        #write format (row_num, col_num, value)
        sheet_test.write(i,0,cl1)
        sheet_test.write(i,1,cl2)
        sheet_test.write(i,2,cl3)
        sheet_test.write(i,3,cl4)
        sheet_test.write(i,4,cl5)
        i = i+1
          
book.save()#define the location of your excel file
