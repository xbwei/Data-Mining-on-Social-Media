'''
Created on Sep 25, 2017

@author: xuebin Wei
@website: www.lbsocial.net
Collect each JMU IA faculty member's info into an Access database.
'''
import pyodbc  # using the pyodbc library 
from bs4 import BeautifulSoup
from urllib import request

'''
Connect to Access
'''
db_file = "" #define the location of your Access file
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(db_file) # define the odbc connection parameter
conn = pyodbc.connect(odbc_conn_str) # establish a database connection
cursor = conn.cursor() # create a cursor

'''
read data into beautifulsoup
'''
url_str = 'https://www.jmu.edu/ia/people/index.shtml' # fill in  url 
response = request.urlopen(url_str)
html_data = response.read()
soup = BeautifulSoup(html_data,"html.parser")
# print (soup.encode("utf-8","ignore"))

'''
find the div tag contains the p_url and p_name
'''
div_yui3_s = soup.find_all('div', class_ = 'yui3-u-1-4')
for div_yui3 in div_yui3_s:
    div_gridpads = div_yui3.find_all('div', class_ = 'gridpad')
    for div_gridpad in div_gridpads:
        div_rwdwys = div_gridpad.find_all('div', class_ = 'rwdwysiwyg profilespace')
        for div_rwdwy in div_rwdwys:        
            p_url =div_rwdwy.a.get('href')
            p_url = p_url.replace('../..','https://www.jmu.edu')
            p_name = div_rwdwy.p.text
            p_name = p_name.strip()
            
            print (p_url)
            print (p_name)
            
            '''
            insert the p_name and p_url into urls table
            '''
            sql_statement = "insert into urls (p_name,p_url) values('{}','{}')".format(p_name,p_url)
            try:
                cursor.execute(sql_statement)
            except:
                pass
            cursor.commit()
            

'''
collect individual professor's info
'''

sql_query_statement = "select p_url from urls"
cursor.execute(sql_query_statement)

results = cursor.fetchall()

for p_url in results:
    url_str = p_url[0]
    response = request.urlopen(url_str)
    html_data = response.read()
    soup = BeautifulSoup(html_data,"html.parser")
    
    
    '''
    find professor.p_name, research.p_name
    '''
    div_apages = soup.find_all('div',id = 'apage')
    for div_apage in div_apages:
        div_mainpagecontents = div_apage.find_all('div',id = 'mainpagecontent')
        for div_mainpagecontent in div_mainpagecontents:
            div_yui3_g_r_s = div_mainpagecontent.find_all('div',class_ = 'yui3-g-r' )
            for div_yui3_g_r in div_yui3_g_r_s:
                div_titles = div_yui3_g_r.find_all('div', id = 'titles')
                for div_title in div_titles:
                    div_pagecontainers = div_title.find_all('div', class_ = 'pagecontainer')
                    for div_pagecontainer in div_pagecontainers:
                        div_yi03_u_s = div_pagecontainer.find_all('div',class_ = 'yui3-u-3-4')
                        for div_yi03_u in div_yi03_u_s:
                            div_h_s = div_yi03_u.find_all('h1', id = 'pagetitle')
                            for div_h in div_h_s:
                                p_name = div_h.text
#                                 print (p_name)

    '''
    find professor.p_mail
    ''' 
     
    div_apages = soup.find_all('div',id = 'apage')
    for div_apage in div_apages:
        div_mainpagecontents = div_apage.find_all('div',id = 'mainpagecontent')
        for div_mainpagecontent in div_mainpagecontents:
            div_maincontentwarappers = div_mainpagecontent.find_all('div',id= 'maincontentwrapper')
            for div_maincontentwarapper in div_maincontentwarappers:
                div_pagecontainers = div_maincontentwarapper.find_all('div', class_ = 'pagecontainer tabular')
                for div_pagecontainer in div_pagecontainers:
                    div_tabulars = div_pagecontainer.find_all('div', class_ = 'tabular-row')
                    for div_tabular in div_tabulars:
                        div_maincontentareas = div_tabular.find_all('div', id ='maincontentarea')
                        for div_maincontentarea in div_maincontentareas:
                            div_yui3_g_r_s = div_maincontentarea.find_all('div', class_ = 'yui3-g-r')
                            for div_yui3_g_r in div_yui3_g_r_s:
                                div_yui3_u_1_s = div_yui3_g_r.find_all('div',class_ = 'yui3-u-1')
                                for div_yui3_u_1 in div_yui3_u_1_s:
                                    div_yui3_u_1_2_s = div_yui3_u_1.find_all('div', class_ ='yui3-u-1-2' )
                                    for div_yui3_u_1_2 in div_yui3_u_1_2_s:
                                        div_gridpads = div_yui3_u_1_2.find_all('div', class_ = 'gridpad')
                                        for div_gridpad in div_gridpads:
                                            div_rwdwysiwygs = div_gridpad.find_all('div', class_ ='rwdwysiwyg' )
                                            for div_rwdwysiwyg in div_rwdwysiwygs:                                         
                                                p_s = div_rwdwysiwyg.find_all ('p') # find p_mail
                                                for p in p_s:
                                                    a_mails = p.find_all('a')
                                                    for a_mail in a_mails:
                                                        if '@' in a_mail.text:
                                                            p_mail = a_mail.text
#                                                             print (p_mail)

    '''
    find professor.p_hedu
    '''
    div_apages = soup.find_all('div',id = 'apage')
    for div_apage in div_apages:
        div_mainpagecontents = div_apage.find_all('div',id = 'mainpagecontent')
        for div_mainpagecontent in div_mainpagecontents:
            div_maincontentwarappers = div_mainpagecontent.find_all('div',id= 'maincontentwrapper')
            for div_maincontentwarapper in div_maincontentwarappers:
                div_pagecontainers = div_maincontentwarapper.find_all('div', class_ = 'pagecontainer tabular')
                for div_pagecontainer in div_pagecontainers:
                    div_tabulars = div_pagecontainer.find_all('div', class_ = 'tabular-row')
                    for div_tabular in div_tabulars:
                        div_maincontentareas = div_tabular.find_all('div', id ='maincontentarea')
                        for div_maincontentarea in div_maincontentareas:
                            div_yui3_g_r_s = div_maincontentarea.find_all('div', class_ = 'yui3-g-r')
                            for div_yui3_g_r in div_yui3_g_r_s:
                                div_yui3_u_1_s = div_yui3_g_r.find_all('div',class_ = 'yui3-u-1')
                                for div_yui3_u_1 in div_yui3_u_1_s:
                                    div_yui3_u_1_2_s = div_yui3_u_1.find_all('div', class_ ='yui3-u-1-2' )
                                    for div_yui3_u_1_2 in div_yui3_u_1_2_s:
                                        div_gridpads = div_yui3_u_1_2.find_all('div', class_ = 'gridpad')
                                        for div_gridpad in div_gridpads:
                                            h5s = div_gridpad.find_all ('h5')
                                            for h5 in h5s:
                                                if h5.text == 'Education':
                                                    div_rwdwysiwygs = div_gridpad.find_all('div', class_ ='rwdwysiwyg' )
                                                    for div_rwdwysiwyg in div_rwdwysiwygs:
                                                        uls = div_rwdwysiwyg.find_all('ul')
                                                        for ul in uls:
                                                            lis = ul.find_all('li')
                                                            p_hedu = lis[0].text
#                                                             print (p_hedu)      
    '''
    insert data into professor table
    '''

    sql_insert_statement = "insert into professor(p_name,p_mail,p_hedu) values('{}','{}','{}')".format(p_name,p_mail,p_hedu)
    try:
        cursor.execute(sql_insert_statement)
    except:
        pass
    cursor.commit()

                        
    '''
    find research.p_research
    '''
    div_apages = soup.find_all('div',id = 'apage')
    for div_apage in div_apages:
        div_mainpagecontents = div_apage.find_all('div',id = 'mainpagecontent')
        for div_mainpagecontent in div_mainpagecontents:
            div_maincontentwarappers = div_mainpagecontent.find_all('div',id= 'maincontentwrapper')
            for div_maincontentwarapper in div_maincontentwarappers:
                div_pagecontainers = div_maincontentwarapper.find_all('div', class_ = 'pagecontainer tabular')
                for div_pagecontainer in div_pagecontainers:
                    div_tabulars = div_pagecontainer.find_all('div', class_ = 'tabular-row')
                    for div_tabular in div_tabulars:
                        div_maincontentareas = div_tabular.find_all('div', id ='maincontentarea')
                        for div_maincontentarea in div_maincontentareas:
                            div_yui3_g_r_s = div_maincontentarea.find_all('div', class_ = 'yui3-g-r')
                            for div_yui3_g_r in div_yui3_g_r_s:
                                div_yui3_u_1_s = div_yui3_g_r.find_all('div',class_ = 'yui3-u-1')
                                for div_yui3_u_1 in div_yui3_u_1_s:

                                    div_gridpads = div_yui3_u_1.find_all('div', class_ = 'gridpad')
                                    for div_gridpad in div_gridpads:
                                        h5s = div_gridpad.find_all ('h5')
                                        for h5 in h5s:
                                            if h5.text == 'Scholarly Interests/Research Topics':
                                                div_rwdwysiwygs = div_gridpad.find_all('div', class_ ='rwdwysiwyg' )
                                                for div_rwdwysiwyg in div_rwdwysiwygs:
                                                    p_s = div_rwdwysiwyg.find_all('p')
                                                    for p in p_s:
                                                        p_research= p.text
#                                                         print ('\t',p_research)

                                                        '''
                                                        insert into research table
                                                        '''
                                                        sql_insert_statement = "insert into research(p_name,p_research) values('{}','{}')".format(p_name,p_research)
                                                        try:
                                                            cursor.execute(sql_insert_statement)
                                                        except:
                                                            pass
                                                        cursor.commit()

                                                    
                                                    uls = div_rwdwysiwyg.find_all('ul')
                                                    for ul in uls:
                                                        lis = ul.find_all('li')
                                                        for li in lis:
                                                            p_research = li.text
#                                                             print ('\t',p_research)
                                                            '''
                                                            insert into research table
                                                            '''
                                                            sql_insert_statement = "insert into research(p_name,p_research) values('{}','{}')".format(p_name,p_research)
                                                            try:
                                                                cursor.execute(sql_insert_statement)
                                                            except:
                                                                pass
                                                            cursor.commit()


cursor.close()
conn.close()
