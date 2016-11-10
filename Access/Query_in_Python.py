import pyodbc  # using the pyodbc library 

db_file = '' #define the location of your Access file

odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' %(db_file) # define the odbc connection parameter

conn = pyodbc.connect(odbc_conn_str) # establish a database connection

cursor = conn.cursor() # create a cursor

sql_select_statement = '' # edit the SQL statement that you want to execute

cursor.execute(sql_select_statement) # execute the SQL statement

results = cursor.fetchall() # get the returned results
for row in results:
    print ('-----')
    for cell in row:
        try:
            print (cell)
        except:
            print ('***error in printing')
            pass

cursor.close()
conn.close()
