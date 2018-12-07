'''
Collect Senators' vote from https://www.senate.gov/legislative/votes.htm
Created on Sep 24, 2018

@author: Xuebin wei
@email: weixuebin@gmail.com
@website: www.lbsocial.net
'''


import urllib.request
from bs4 import BeautifulSoup
import pyodbc
 
url_str = '' # url of the senate website
response = urllib.request.urlopen(url_str)
html_data = response.read()

soup = BeautifulSoup(html_data,'html.parser')
# print (soup)


db_file = r'' #define the location of your Access file
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(db_file) # define the odbc connection parameter
conn = pyodbc.connect(odbc_conn_str) # establish a database connection
cursor = conn.cursor() # create a cursor

for div in soup.find_all('div', class_ = 'contenttext'):
    if div.b:
        if div.b.text.strip() == 'Vote Number:':
            vote_number = div.text.split(':')[1].strip()
            print ('Collecting vote number: {}'.format(vote_number))
            
        if div.b.text.strip() == 'Vote Date:':
            vote_date = div.text.split(':')[1].strip()
            
        if div.b.text.strip() == 'Nomination Number:':
            print (div.a.get('href'))
            

if vote_number and vote_date:     
    for div in soup.find_all('div',class_ = 'newspaperDisplay_3column'):
        try:
            if ',' in div.span.text:
                results =div.span.text.split('\n')
                
                for result in results:
                    if result:
                        name_party_state, vote = result.split(',')
                        vote= vote.strip()
                        
                        name,party_state =name_party_state.split('(')
                        name = name.strip()
                        
                        party,state =party_state.split('-')
                        party =party
                        state =state[:-1]
                        
                        sql_insert_snator = "insert into senator(sname,party,state) values('{}','{}','{}')".format(name,party,state)
                        try:
                            cursor.execute(sql_insert_snator)
                        except:
                            pass
                              
                        sql_insert_vote = "insert into vote(sname,vote,vote_number,vote_date) values('{}','{}','{}','{}')".format(name,vote,vote_number,vote_date)
                        try:
                            cursor.execute(sql_insert_vote)
                        except:
                            pass
                        cursor.commit()
        except:
            pass
                                  
cursor.close()
conn.close()
print('Done.')


