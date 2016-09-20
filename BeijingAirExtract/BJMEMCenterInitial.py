'''
Created on May 24, 2013

@author: Xuebin Wei
Dept of Geog, UGA
xbwei@uga.edu
weixuebin@gmail.com

Extract The air pollution data of Beijing, China from Beijing Municipal Environmental Monitoring Center
http://zx.bjmemc.com.cn/
Execute the py file hourly to record the air data in a mysql database
This py is to create the mysql table
'''

   
# Using the sqllite3 to create new table

import sys
import logging
import traceback
import mysql.connector
from mysql.connector import errorcode




'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('BeijingInitial')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('BeijingInitial.log')
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
StationList = ["Pinggu","Fangshan","Yizhuang","Yungang","Miyunshuiku","Huairou","Badalin","Wanshouxigong","Changpin","Mengtougou","Tongzhou","Daxing","Dingling","Qianmen","Dongsi","Tiantan","Aotizhongxin","Nongzhanguan","Miyun","Gucheng","Guanyuan","Nansanhuan","Beibuxincheng","Wanliu","Yongledian","Liulihe","Yongdingmennei","Yufa","Zhiwuyuan","Fengtaihuayuan","Shunyi","Yanqing","Donggaocun","Dongsihuan","Xizhibeimen","Huairoukuangou"]

# List of Field (old, two pm10 in the list)
# FieldList = ["Time","Pm25","Pm25_24","Pm25IAQI","Pm25Level","Pm25Quality","Pm10","Pm10_24","Pm10IAQI","Pm10Level","Pm10Quality","So2","So2_24","So2IAQI","So2Level","So2Quality","O3","O3_24","O3IAQI","O3Level","O3Quality","Co","Co_24","CoIAQI","CoLevel","CoQuality","Pm10","Pm10_24","Pm10IAQI","Pm10Level","Pm10Quality"]
# List of Field

'''
previous wrong field list
'''
# FieldList = ["Time","Pm25","Pm25_24","Pm25IAQI","Pm25Level","Pm25Quality","Pm10","Pm10_24","Pm10IAQI","Pm10Level","Pm10Quality","So2","So2_24","So2IAQI","So2Level","So2Quality","O3","O3_24","O3IAQI","O3Level","O3Quality","Co","Co_24","CoIAQI","CoLevel","CoQuality"]

FieldList = ["Time","Pm25","Pm25_24","Pm25IAQI","Pm25Level","Pm25Quality","Pm10","Pm10_24","Pm10IAQI","Pm10Level","Pm10Quality","So2","So2_24","So2IAQI","So2Level","So2Quality","No2","No2_24","No2IAQI","No2Level","No2Quality","O3","O3_24","O3IAQI","O3Level","O3Quality","Co","Co_24","CoIAQI","CoLevel","CoQuality"]


# List of General Table
GeneralFieldList = ["Name","Time","PrimaryName","PrimaryValue","PrimaryLevel","PrimaryQuality"]


'''
connect database
'''
try:
    cnx = mysql.connector.connect(user='',
                                database='',
                                password='',
                              host='',)
    cursor = cnx.cursor()
    DB_NAME = 'beijingair'
    TABLES = {}
    '''
    Create general table
    '''
    GeneralField=""
    for generalfield in GeneralFieldList:
        GeneralField = GeneralField+ str(generalfield)+" varchar(45),"
    #print GeneralField

    TABLES['General'] = (
        "CREATE TABLE `General` ("
        "  `GeneralID` int(11) NOT NULL AUTO_INCREMENT,`CheckTime` TIMESTAMP NULL,"+GeneralField+
        " PRIMARY KEY (`GeneralID`),"
        "  UNIQUE INDEX `GeneralID_UNIQUE` (`GeneralID` ASC));"
        )
    
    '''
    Create table for each station
    '''
    for station in StationList:
        TableField = ""
        for SingleTableField in FieldList:
            TableField =TableField+ str(SingleTableField)+" varchar(45),"
#         print TableField
        
        TABLES[station] = (
            "CREATE TABLE "+ str(station)+" ("
        "  `ID` int(11) NOT NULL AUTO_INCREMENT,`CheckTime` TIMESTAMP NULL,"+TableField+
        " PRIMARY KEY (`ID`),"
        "  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC));"
            )

    #print TABLES
    
    '''
    Execute SQL to create table
    '''
    for name, ddl in TABLES.iteritems():
#         print "\t Create the table of " + name
#         print ddl
        try:
            print("Creating table {}: ".format(name))
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            print "\t Error, Check the Log."
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logger.info("already exists.")
            else:
                logger.info(err.msg)
        else:
            print("\t OK")
            
    print "Complete the table creation."
#    print cursor
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