'''
Created on Jan 16, 2018

@author: weixx
'''

import sys
import logging
import traceback


import pyodbc  # using the pyodbc library 
from bs4 import BeautifulSoup
from urllib import request


'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('get house')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('get house.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


'''
Connect to Access
'''
db_file = '' #define the location of your Access file
 

odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(db_file) # define the odbc connection parameter

conn = pyodbc.connect(odbc_conn_str) # establish a database connection

cursor = conn.cursor() 
other_cursor = conn.cursor() 



def get_home_urls():
    '''
    get url of all available houses
    '''
    base_url_str = '' #fill in your search url from trulia
    for i in range(1,5):# the number of pages you want to extract
        if i == 1:
            search_url_str = base_url_str
        else:
            search_url_str = base_url_str+'%s_p'%(i)
        print (search_url_str)
        response = request.urlopen(search_url_str)
        html_data = response.read()
        soup = BeautifulSoup(html_data,"html.parser")
#         print (soup.encode("utf-8","ignore"))
         
         
        '''
        find url of each single house from the main page
        and save the address, url to an access table
        '''
        for  li in soup.find_all("li", attrs={"class":"xsCol12Landscape smlCol12 lrgCol8"}):
            div_ptm = li.find("div", class_ = "ptm cardContainer positionRelative clickable")
            div_card = div_ptm.find("div", class_ = "card backgroundBasic")
            for div in div_card.find_all("div"):
                if div.a is not None:
#                     print (div.a)
                    house_address = div.a["alt"]
                    house_url = ('https://www.trulia.com'+div.a["href"])#url of each single house
    #                 print (house_url)
                    print (house_address)
                    sql_insert_house_url = """insert into house_url (house_address,house_url) values (%s,%s)""" %("'"+house_address+"'","'"+ house_url+"'") 
                                 
     
                    try:
                        cursor.execute(sql_insert_house_url) 
                        cursor.commit()
     
                         
                    except: 
     
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                        print (''.join('!! ' + line for line in lines) ) # Log it or whatever here
                        logger.info(''.join('!! ' + line for line in lines) )
                        pass
         
    cursor.close() 
    conn.close() 
# get_home_urls()


def update_table(col,val,house_address):
    if type(val).__name__ == 'str':
        cursor.execute("update house_url set %s = %s where house_address = %s" %(col,"'"+val+"'","'"+house_address+"'"))

    else:
        cursor.execute("update house_url set %s = %s where house_address = %s" %(col,val,"'"+house_address+"'"))
    
def update_home_url():
    cursor.execute("SELECT ID,house_address, house_url from house_url ")
    for id,house_address,house_url in cursor.fetchall():
        try:
            print (id, house_address)
        
            house_url_str = house_url
            response = request.urlopen(house_url_str)
            html_data = response.read()
            soup = BeautifulSoup(html_data,"html.parser")
            street =''
            i = 0
            for street_item in house_address.split():
                if i == 0:
                    pass
                else:
    
                    street = street +' '+street_item
                i = 1
            street_info=(street.strip())
            update_table('street',street_info,house_address)
            
            for div_mvn in soup.find_all('div', class_ = 'mvn'):
                for span in div_mvn.find_all('span', class_ = 'h3'):
                    if "$" in span.text.strip():
                        price = float(span.text.strip().split('$')[-1].replace(',',''))
                    else:
                        price = 0.0
                    update_table('price',price,house_address)
            for div_mini in soup.find_all('div', class_ = 'miniCol24 xsCol24 smlCol24 mdCol16 lrgCol16 mhn phn'):
#                 print (div_mini)
                for div_row_mbm in div_mini.find_all('div', class_ = "row mbm"):
#                     print (div_row_mbm)
                    for li in div_row_mbm.find_all('li'):
                        detail_record = li.text.lower()
            
                            
                        if 'price' in detail_record:
                            pass
                            


                        elif 'bed' in detail_record:

                            bedroom= int(detail_record.split()[0])
                            update_table('bedroom',bedroom,house_address)
                            
                        elif 'bath' in detail_record:

                            bathroom = float(detail_record.split()[0])
                            update_table('bathroom',bathroom,house_address)
                            
                        elif 'single-family home' in detail_record:

                            house_type= (detail_record)
                            update_table('house_type',house_type,house_address)         

                                      
        
                        elif 'lot size' in detail_record:

                            lot_size = detail_record.split()[0]+detail_record.split()[1]
                            if 'acres' in lot_size:
                                lot_size = float(lot_size[:-5])*43560
                                
                            else:
                                lot_size = float(lot_size[:-4])

#                             print (lot_size)
                            
                            update_table('lot_size',lot_size,house_address) 
                            
                        elif 'built in' in detail_record:

                            built_in = int(detail_record.split()[2])  
                            update_table('built_in',built_in,house_address)  
            

    
                        elif 'condo' in detail_record:

                            house_type= (detail_record)  
                            update_table('house_type',house_type,house_address)   
                            
                            
                        elif 'townhouse' in detail_record:
                            house_type= (detail_record)  
                            update_table('house_type',house_type,house_address)   
# 


                        elif 'multi-family' in detail_record:
                            house_type= (detail_record)  
                            update_table('house_type',house_type,house_address)   
#                             

                        elif 'rooms' in detail_record:
    
                            rooms= int(detail_record.split(':')[1].strip())
                            update_table('rooms',rooms,house_address)  

                            
                        elif 'lot' in detail_record and 'land' in detail_record:
                            
                            house_type= ('lot or land')  
                            update_table('house_type',house_type,house_address) 
                            
                        elif 'day' in detail_record:
                            days = int(detail_record.split()[0])
                            update_table('days',days,house_address) 
                            
                        elif 'view' in detail_record:
                            views = int(detail_record.split()[0])
                            update_table('views',views,house_address) 
                            
                        elif 'hoa' in detail_record:
                            hoa = float(detail_record.split('/')[0][2:])
                            update_table('hoa',hoa,house_address) 
                        
                        elif 'sqft' in detail_record:
                            if '/' in detail_record:
                                pass
                            else:

                                area= float(detail_record.split()[0].replace(',','')) 
                                update_table('area',area,house_address) 
                        else:
                            
                            other_cursor.execute("SELECT other from house_url where house_address = %s" %("'"+house_address+"'"))
#                             other_content =''
                            other_pre_content = other_cursor.fetchone()
                            if other_pre_content[0] is not None:
                                other = other_pre_content[0]+','+detail_record

                            else:
                                other = detail_record
                            update_table('other',other,house_address)
                            
                             
                        update_table('iscollected',True,house_address)
   
                        cursor.commit() 
        except: 
    
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print (''.join('!! ' + line for line in lines) ) # Log it or whatever here
            print (house_address)
            print (id)
            update_table('iscollected',False,house_address)
            cursor.commit() 
            pass
    
    cursor.close() 
    conn.close() 
update_home_url()
