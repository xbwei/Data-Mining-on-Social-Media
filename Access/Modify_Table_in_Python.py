'''
Created on Sep 5, 2016

@author: xuebin wei
website: www.lbsocial.net 
'''

import pyodbc  # using the pyodbc library 

db_file = '' #define the location of your Access file

odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(db_file) # define the odbc connection parameter

conn = pyodbc.connect(odbc_conn_str) # establish a database connection

cursor = conn.cursor() # create a cursor

sql_modify_statement = '' # edit the SQL statement that want to execute

cursor.execute(sql_modify_statement) # execute the SQL statement
cursor.commit() # let the database commit the changes in the tables

cursor.close() # close the cursor
conn.close() # close the connection to the database
