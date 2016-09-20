'''
Created on May 26, 2013
@author: Xuebin Wei
Dept of Geog, UGA
xbwei@uga.edu
weixuebin@gmail.com

Extract The air pollution data of Beijing, China from Beijing Municipal Environmental Monitoring Center
http://zx.bjmemc.com.cn/
Execute the py file hourly to record the air data in a mysql database
This py is to insert the data into the mysql table
'''
import urllib2
from bs4 import BeautifulSoup
import sys
import logging
import traceback
import mysql.connector
from mysql.connector import errorcode
import json
from datetime import datetime
import time
import socket

'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('Trysoupe')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('Trysoupe.log')
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


# List of stations
# StationList = ["Pinggu","Fangshan","Yizhuang","Yungang","Miyunshuiku","Huairou","Badalin","Wanshouxigong","Changpin","Mengtougou","Tongzhou","Daxing","Dingling","Qianmen","Dongsi","Tiantan","Aotizhongxin","Nongzhanguan","Miyun","Gucheng","Guanyuan","Nansanhuan","Beibuxincheng","Wanliu","Yongledian","Liulihe","Yongdingmennei","Yufa","Zhiwuyuan","Fengtaihuayuan","Shunyi","Yanqing","Donggaocun","Dongsihuan","Xizhibeimen","Huairoukuangou"]

# List without Huairoukuankou
StationList = ["Pinggu","Fangshan","Yizhuang","Yungang","Miyunshuiku","Huairou","Badalin","Wanshouxigong","Changpin","Mengtougou","Tongzhou","Daxing","Dingling","Qianmen","Dongsi","Tiantan","Aotizhongxin","Nongzhanguan","Miyun","Gucheng","Guanyuan","Nansanhuan","Beibuxincheng","Wanliu","Yongledian","Liulihe","Yongdingmennei","Yufa","Zhiwuyuan","Fengtaihuayuan","Shunyi","Yanqing","Donggaocun","Dongsihuan","Xizhibeimen"]

# List of Field
'''
previous wrong field list
'''
# FieldList = ["Time","Pm25","Pm25_24","Pm25IAQI","Pm25Level","Pm25Quality","Pm10","Pm10_24","Pm10IAQI","Pm10Level","Pm10Quality","So2","So2_24","So2IAQI","So2Level","So2Quality","O3","O3_24","O3IAQI","O3Level","O3Quality","Co","Co_24","CoIAQI","CoLevel","CoQuality","Pm10","Pm10_24","Pm10IAQI","Pm10Level","Pm10Quality"]

FieldList = ["Time","Pm25","Pm25_24","Pm25IAQI","Pm25Level","Pm25Quality","Pm10","Pm10_24","Pm10IAQI","Pm10Level","Pm10Quality","So2","So2_24","So2IAQI","So2Level","So2Quality","No2","No2_24","No2IAQI","No2Level","No2Quality","O3","O3_24","O3IAQI","O3Level","O3Quality","Co","Co_24","CoIAQI","CoLevel","CoQuality"]

#List of AIRIndex
AirIndexList = ["pm2.5","pm10","so2","no2","o3","co"]
#List of Station URL Code
StationURLList = ["%E5%B9%B3%E8%B0%B7","%E6%88%BF%E5%B1%B1","%E4%BA%A6%E5%BA%84","%E4%BA%91%E5%B2%97","%E5%AF%86%E4%BA%91%E6%B0%B4%E5%BA%93","%E6%80%80%E6%9F%94","%E5%85%AB%E8%BE%BE%E5%B2%AD","%E4%B8%87%E5%AF%BF%E8%A5%BF%E5%AE%AB","%E6%98%8C%E5%B9%B3","%E9%97%A8%E5%A4%B4%E6%B2%9F","%E9%80%9A%E5%B7%9E","%E5%A4%A7%E5%85%B4","%E5%AE%9A%E9%99%B5","%E5%89%8D%E9%97%A8","%E4%B8%9C%E5%9B%9B","%E5%A4%A9%E5%9D%9B","%E5%A5%A5%E4%BD%93%E4%B8%AD%E5%BF%83","%E5%86%9C%E5%B1%95%E9%A6%86","%E5%AF%86%E4%BA%91","%E5%8F%A4%E5%9F%8E","%E5%AE%98%E5%9B%AD","%E5%8D%97%E4%B8%89%E7%8E%AF","%E5%8C%97%E9%83%A8%E6%96%B0%E5%8C%BA","%E4%B8%87%E6%9F%B3","%E6%B0%B8%E4%B9%90%E5%BA%97","%E7%90%89%E7%92%83%E6%B2%B3","%E6%B0%B8%E5%AE%9A%E9%97%A8%E5%86%85","%E6%A6%86%E5%9E%A1","%E6%A4%8D%E7%89%A9%E5%9B%AD","%E4%B8%B0%E5%8F%B0%E8%8A%B1%E5%9B%AD","%E9%A1%BA%E4%B9%89","%E5%BB%B6%E5%BA%86","%E4%B8%9C%E9%AB%98%E6%9D%91","%E4%B8%9C%E5%9B%9B%E7%8E%AF","%E8%A5%BF%E7%9B%B4%E9%97%A8%E5%8C%97"]

CheckURL = "http://zx.bjmemc.com.cn/ashx/Data.ashx?Action=GetWRWInfo_ByStationAndWRWType&StationName="

# parameter to prevent force close by remote server
sleep_download_time = 10

'''
get general table data
'''
try:
    print "Getting General table..."
    try:
        req = urllib2.urlopen("http://zx.bjmemc.com.cn/ashx/Data.ashx?Action=GetAQIClose1h",timeout = 120)
        
        data = json.load(req)
        # print data
    except urllib2.URLError,e:
        logger.info("General table is not updated due to - "+str(e.reason))
        print str(e.reason)
        time.sleep(sleep_download_time)
        data=[]
        pass
    except socket.error as s:
        logger.info("General table is not updated due to - socket time out")
        print "socket time out"
        time.sleep(sleep_download_time)
        data=[]
        pass
        
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        data=[]
        pass
    if len(data)>0:    
        for p in data:
        #     print "General Table"
        #     print "\t"+ p["StationName"]
        #     print "\t"+ p["Time"]
        #     print "\t"+ p["AQIName"]
        #     print "\t"+ p["AQIValue"]
        #     print "\t"+ p["QLevel"]
        #     print "\t"+ p["Quality"]
        
            try:
            
                '''
                database connect
                '''
                cnx = mysql.connector.connect(user='',
                                                database='',
                                                password='',
                                              host='',)
                cursor = cnx.cursor()
                
                '''
                insert value to general table
                '''
                add_general = ("INSERT INTO general "
                               "(CheckTime,Name,  Time,PrimaryName,PrimaryValue,PrimaryLevel,PrimaryQuality) "
                               "VALUES (%s,%s, %s,%s,%s,%s,%s)")
        #         print add_general
            
                data_general = (datetime.now(),p["StationName"],p["Time"],p["AQIName"],p["AQIValue"],p["QLevel"],p["Quality"])
        #         print data_general
                
                # Insert new general data
                cursor.execute(add_general, data_general)
            
                
                # Make sure data is committed to the database
                cnx.commit()
        
            
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    logger.info("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    logger.info("Database does not exists")   
                else:
                    logger.info("General table has an error of "+str(err)+"in "+str(p["StationName"]))
                    continue  
            except :
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )
                continue        
except :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print ''.join('!! ' + line for line in lines)  # Log it or whatever here
    logger.info(''.join('!! ' + line for line in lines) )
    


try:

    '''
    database connect
    '''
    cnx = mysql.connector.connect(user='',
                                    database='',
                                    password='',
                                  host='',)
    cursor = cnx.cursor()

      
    #index j to loop the url query
    j = 0
    # index t to loop the table update
    print "Getting Station Time..."
    try:
        TimeURL = urllib2.urlopen("http://zx.bjmemc.com.cn/ashx/Data.ashx?Action=GetLastPubDTime",timeout = 30).read()
        # print TimeURL.split(":")[1][1:].decode('unicode-escape').encode("gb18030")
        StationTime = str(TimeURL.split(":")[1][1:].decode('unicode-escape').encode("utf-8"))
    except urllib2.URLError,e:
        logger.info("Station Time is not updated due to - "+str(e.reason))
        print str(e.reason)
        StationTime = "error"
        time.sleep(sleep_download_time)
        pass
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        StationTime = "error"
        pass
                    
       
    for Station in StationList:
        try:

            print "Getting "+ str(Station)+"..."

            StationValue=[]
            StationValue.append(datetime.now())
            StationValue.append(StationTime)

            for AirIndex in AirIndexList:
                try:
                 
                    print '\t'+ str(AirIndex)
                    
#                    time.sleep(sleep_download_time)
    
    #                URLP = urllib2.urlopen(str(CheckURL+StationURLList[j]+"&WRWType="+AirIndex)).read()
                    URLP = urllib2.urlopen(str(CheckURL+StationURLList[j]+"&WRWType="+AirIndex),timeout = 60)
    #                req = urllib2.Request(str(CheckURL+StationURLList[j]+"&WRWType="+AirIndex))
    #                response = urllib2.urlopen(req)
    #                the_page = response.read()
    
                    soup = BeautifulSoup(URLP.read())
                    URLP.close()
                    tag = soup.find_all("span")
    
                    if len(tag[2].string.split(" "))>2:
    #                     print '\t'+'\t'+"Current "+tag[2].string.split(" ")[15][:2]
    #                     print tag[2].string.split(" ")[15][:3]
                        StationValue.append(str(tag[2].string.split(" ")[15][:3]))
    
                    else:
    #                     print '\t'+'\t'+"Current "+tag[2].string
    #                     print tag[2].string
                        StationValue.append(str(tag[2].string))
    
    #                 print '\t'+'\t'+"24Hour "+tag[7].string
    #                 print tag[7].string
                    StationValue.append(str(tag[7].string))
    
    #                 print '\t'+'\t'+"IQAI "+tag[10].string
    #                 print tag[10].string
                    StationValue.append(str(tag[10].string))
    
    #                 print '\t'+'\t'+"Level "+tag[12].string
    #                 print tag[12].string
                    StationValue.append(str(tag[12].string.encode("utf-8")))
    
    #                 print '\t'+'\t'+"Quality "+tag[13].string
    #                 print tag[13].string
                    StationValue.append(str(tag[13].string.encode("utf-8")))
    
    #                 print StationValue
                except urllib2.URLError,e:
                    logger.info(AirIndex + " - " + Station +" is not updated due to - "+str(e.reason))
                    print str(e.reason)
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    time.sleep(sleep_download_time)
                    continue
                except socket.error as s:
                    logger.info("General table is not updated due to - socket time out")
                    print "socket time out"
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    time.sleep(sleep_download_time)
                    continue
                    
                except :
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                    logger.info(''.join('!! ' + line for line in lines) )
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    StationValue.append("error")
                    time.sleep(sleep_download_time)
                    continue
                    
                    


           

            add_station = ("INSERT INTO "+str(Station)+
                           "(CheckTime,Time,Pm25,Pm25_24,Pm25IAQI,Pm25Level,Pm25Quality,Pm10,Pm10_24,Pm10IAQI,Pm10Level,Pm10Quality,So2,So2_24,So2IAQI,So2Level,So2Quality,No2,No2_24,No2IAQI,No2Level,No2Quality,O3,O3_24,O3IAQI,O3Level,O3Quality,Co,Co_24,CoIAQI,CoLevel,CoQuality) "
                           "VALUES (%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s)")
#             print add_station
            data_station = tuple(StationValue)
#             print data_station
            
            # Insert new station data
            cursor.execute(add_station, data_station)
        
            
            # Make sure data is committed to the database
            j = j+1
            cnx.commit()
            print "Done!"
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.info("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.info("Database does not exists")   
            else:
                logger.info(str(Station)+" table has an error of "+str(err)+"in "+str(AirIndex))  
        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )
            continue
        

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logger.info("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logger.info("Database does not exists")   
    else:
        logger.info(err)  
except :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print ''.join('!! ' + line for line in lines)  # Log it or whatever here
    logger.info(''.join('!! ' + line for line in lines) )


else:
    cursor.close()
    cnx.close() 
    

