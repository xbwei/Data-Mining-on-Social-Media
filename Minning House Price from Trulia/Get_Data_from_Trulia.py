'''
Created on Aug 13, 2017

@author: Xuebin Wei
xuebin@gmail.com
www.lbsocial.net
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
 
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' %(db_file) 
conn = pyodbc.connect(odbc_conn_str) 
cursor = conn.cursor() 
other_cursor = conn.cursor() 



def get_home_urls():
    '''
    get url of all available houses
    '''
    base_url_str = '' #fill in your search url from trulia
                    # e.g.: https://www.trulia.com/for_sale/38.207278362404,38.660160967549,-79.135529519735,-78.672043801962_xy/11_zm/
    for i in range(1,42):# the number of pages you want to extract
        if i == 1:
            search_url_str = base_url_str
        else:
            search_url_str = base_url_str+'%s_p'%(i)
        print (search_url_str)
        response = request.urlopen(search_url_str)
        html_data = response.read()
        soup = BeautifulSoup(html_data,"html.parser")
    #     print (soup.encode("utf-8","ignore"))
         
         
        '''
        find url of each single house from the main page
        and save the address, url to an access table
        '''
        for  li in soup.find_all("li", attrs={"class":"smlCol12 lrgCol8"}):
            div_ptm = li.find("div", class_ = "ptm cardContainer positionRelative clickable")
            div_card = div_ptm.find("div", class_ = "card backgroundBasic")
            for div in div_card.find_all("div"):
                if div.a is not None:
    #                 print (div.a)
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
            
            
            for detail_ul in soup.find_all ("ul", class_ = "listInline pdpFeatureList"):
                for deail_ul_li in detail_ul.find_all("li"):
                    for listed_detail_ul in deail_ul_li.find_all("ul", class_ ="listBulleted mbn"):
                        for detail_ul_li_ul_li in listed_detail_ul.find_all("li"):
                            detail_record = detail_ul_li_ul_li.text.strip().lower()
                            
                            if 'price' in detail_record:
                                
    
                                price = float(detail_record.split('$')[-1].replace(',',''))
                                update_table('price',price,house_address)
                            elif 'bedroom' in detail_record:
    
                                bedroom= int(detail_record.split()[0])
                                update_table('bedroom',bedroom,house_address)
                                
                            elif 'bathroom' in detail_record:
    
                                bathroom = int(detail_record.split()[0])
                                update_table('bathroom',bathroom,house_address)
                                
                            elif 'single-family home' in detail_record:
    
                                house_type= (detail_record)
                                update_table('house_type',house_type,house_address)         
                    
                            elif 'air conditioning' in detail_record:
                                update_table('air_conditioning',True,house_address) 
    
                                
                            elif 'status' in detail_record:
     
                                status =  (detail_record.split(':')[1].strip())  
                                update_table('status',status,house_address)
                                
                            elif 'parking' in detail_record:
                                status =  (detail_record.split(':')[1].strip())  
                                update_table('parking',status,house_address)

    
                                 
                            elif 'heating fuel' in detail_record:
    
                                heating_fuel = (detail_record.split(':')[1].strip())    
                                update_table('heating_fuel',heating_fuel,house_address)
                                  
                            elif 'basement' in detail_record:
                                update_table('basement',True,house_address)
       
                                
                            elif 'lawn' in detail_record:
                                update_table('lawn',True,house_address)
                                
                            elif 'attic' in detail_record:
                                update_table('attic',True,house_address)
                                        
                                    
                            elif 'refrigerator' in detail_record:
                                update_table('refrigerator',True,house_address)
    
            
                            elif 'dishwasher' in detail_record:
                                update_table('dishwasher',True,house_address)
                                
    
                                                          
                            elif 'microwave' in detail_record:
                                update_table('microwave',True,house_address)                            
    
                                
                            elif 'fireplace' in detail_record:
                                update_table('fireplace',True,house_address)  
       
                                
                            elif 'porch' in detail_record:
                                update_table('porch',True,house_address) 
           
            
                            elif 'deck' in detail_record:
                                update_table('deck',True,house_address) 
           
            
                            elif 'garden' in detail_record:
                                update_table('garden',True,house_address)      
                                
                            elif 'washer' in detail_record:
                                update_table('washer',True,house_address) 
     
        
                            elif 'dryer' in detail_record:
                                update_table('dryer',True,house_address) 
                                          
            
                            elif 'lot size' in detail_record:
    
                                if "," in detail_record.split(':')[1].split()[0]:
                                    lot_size= float(detail_record.split(':')[1].split()[0].replace(',',''))
                                else:
                                    lot_size = float(detail_record.split(':')[1].split()[0])  
                                update_table('lot_size',lot_size,house_address) 
                
                            elif 'built in' in detail_record:
    
                                built_in = int(detail_record.split()[2])  
                                update_table('built_in',built_in,house_address)  
                
                            elif 'mls/source id:' in detail_record:
    
                                mls_id= (detail_record.split(':')[1].strip())  
                                update_table('mls_id',mls_id,house_address)  
                                
                            elif 'zip' in detail_record:
    
                                zip = (detail_record.split(':')[1].strip())    
                                update_table('zip',zip,house_address)  
    
                            elif 'floors' in detail_record:
                                
                                floors = (detail_record.split(':')[1].strip())   
                                update_table('floors',floors,house_address)  
    
                            elif 'roof' in detail_record:
                                
                                roof = (detail_record.split(':')[1].strip())   
                                update_table('roof',roof,house_address) 
                            elif 'patio' in detail_record:
                                update_table('patio',True,house_address) 
    
        
                            elif 'condo' in detail_record:
    
                                house_type= (detail_record)  
                                update_table('house_type',house_type,house_address)   
                                
                            elif 'vaulted ceiling' in detail_record:
                                update_table('vaulted_ceiling',True,house_address) 
     
                                
                            elif 'new construction' in detail_record:
                                update_table('new_construction',True,house_address)
    
                                
                            elif 'townhouse' in detail_record:
                                house_type= (detail_record)  
                                update_table('house_type',house_type,house_address)   
    
        
                            elif 'skylight' in detail_record:
                                update_table('skylight',True,house_address)
    
                            elif 'multi-family' in detail_record:
                                house_type= (detail_record)  
                                update_table('house_type',house_type,house_address)   
                                
                            elif 'pool' in detail_record:
                                update_table('pool',True,house_address)
    
                                
                            elif 'jetted bath tub' in detail_record:
                                update_table('jetted_bath',True,house_address)
    
        
                            elif 'security system' in detail_record:
                                update_table('security_system',True,house_address)
    
        
                                
                            elif 'virtual tour' in detail_record:
                                continue
    
                                
                            elif 'garbage disposal' in detail_record:
                                update_table('garbage_disposal',True,house_address)
    
                                
                            elif 'ceiling fan' in detail_record:
                                update_table('ceiling_fan',True,house_address)
    
                                
                            elif 'double-pane window' in detail_record:
                                update_table('double_pan_windows',True,house_address)
    
        
                            elif 'exterior' in detail_record:
        
                                exterior= (detail_record.split(':')[1].strip())  
                                update_table('exterior',exterior,house_address)
                                
                            elif 'view' in detail_record:
        
                                view = (detail_record.split(':')[1].strip()) 
                                update_table('view',view,house_address)  
                            
                            elif 'rooms' in detail_record:
        
                                rooms= int(detail_record.split(':')[1].strip())
                                update_table('rooms',rooms,house_address)  
                                
                            elif 'heating' in detail_record:
    
                                heating = (detail_record.split(':')[1].strip()) 
                                update_table('heating',heating,house_address) 
                                                 
                            elif 'architecture' in detail_record:
    
                                architecture= (detail_record[:-12].strip()) 
                                update_table('architecture',architecture,house_address) 
                                
                            elif 'lot' in detail_record and 'land' in detail_record:
                                
                                house_type= ('lot or land')  
                                update_table('house_type',house_type,house_address) 
    
                            
                            elif 'sqft' in detail_record:
    
                                area= float(detail_record.split()[0].replace(',','')) 
                                update_table('area',area,house_address) 
                            else:
                                
                                other_cursor.execute("SELECT other from house_url where house_address = %s" %("'"+house_address+"'"))
                                other_content =''
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
    