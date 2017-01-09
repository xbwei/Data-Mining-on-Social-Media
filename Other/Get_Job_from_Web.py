'''
Created on Jan 26, 2016

@author: xuebin wei
get job info from website
www.lbsocial.net
'''

# import json
import sys
import logging
import traceback

from bs4 import BeautifulSoup
import urllib2,urllib
import psycopg2
import time

import csv
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import urllib2
# print twitter.api


'''
handle log
'''

# create logger with 'spam_application'
logger = logging.getLogger('GetJob')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('GetJob.log')
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





def scrape_url(url):
    '''
    get job info  from scrolling page
    '''
 
    # Load WebDriver and navigate to the page url.
    # This will open a browser window.
    driver = webdriver.Firefox()



    driver.get(url)

    try:
#         while ('No results' not in driver.find_element_by_class_name('empty-text').text):
        for i in range(0,50):
    
                                           
                                           
            elem = driver.find_element_by_tag_name('li')
            elem.send_keys(Keys.PAGE_DOWN)
         
        # Once the whole table has loaded, grab all the visible links.    
        visible_links = driver.find_elements_by_tag_name('li')
        for link in visible_links:
            if link.get_attribute('data-item-id') is not None:
                print visible_links
                

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        print url

         
    driver.quit()
           


def getRootByBS4(url):
    
    '''
    use beautiful soup to extract job info at root level
    from  http://scip.careerwebsite.com/jobseeker/search/results/
    '''
    try:
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
        print url
        jobs = urllib2.urlopen(url).read()
     

        soup = BeautifulSoup(jobs)

         
        # i=0
        for div in soup.find_all('div', attrs = {"class":"job-summary"}):
            
            job_title = div.a.span.string.strip()
            job_url = div.a.get('href').encode('UTF-8','ignore')
            job_pub_date =  None
            job_des = ''
            for p in div.find_all('p',attrs = {'class':'clearfix'}):
                job_des = p.string.strip().encode('UTF-8','ignore')

            job_company = div.strong.string
            if job_company is not None:
                job_company = job_company.strip()
            else:
                job_company = None
            job_loc = div.em.string.strip()
            
            print '\t job title:',job_title
            print '\t time:',job_pub_date
#             print '\t url:',job_url
#             print '\t company:',job_company
#             print '\t location:', job_location
#             print '\t job_describ:',job_describ
            try:
                cursor.execute('SELECT * FROM webjob WHERE job_url ='  +"'"+job_url+"'")
                test = cursor.fetchone()
#                 print test
                if (test):
                    print "duplicated job url: "+job_url
                else:
                    cursor.execute('INSERT INTO webjob (job_pub_date,job_loc,job_des,job_url,job_title,job_company)'
                                                    'VALUES(%s,%s,%s,%s,%s,%s)',
                                                    (job_pub_date,job_loc,job_des,job_url,job_title,job_company))
            except psycopg2.IntegrityError:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print "warning: duplicated job_url"  # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )
                pass
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )
                
            connection.commit()
        cursor.close()
        connection.close()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
            
url_default = 'http://scip.careerwebsite.com/jobseeker/search/results/'
url_10 = 'http://scip.careerwebsite.com/jobseeker/search/results/?keywords=&t735=&t3960=&t3961=46099&t737=&max=10&site_id=296&search='

# getByBS4(url_default)

def getscipe(key_url):
    '''
    get full info from scipe
    '''
    try:
        branch_url = 'http://scip.careerwebsite.com'+key_url
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
#         print branch_url
        branch_info = urllib.urlopen(branch_url).read()
     

        soup = BeautifulSoup(branch_info)
        full_desc = None
        full_requ = None
        full_othe = None
        for div in soup.find_all('div',attrs = {"class":"generic-details-text"}):

            
            con_text=''
            for p in div.pre.findAll('p'):
                if p.string is not None:
                    con_text= con_text+' '+p.string.strip().encode('UTF-8','ignore')
                if p.text is not None:
                    con_text= con_text+' '+p.text.strip().encode('UTF-8','ignore')
#                     print p.string.strip().encode('UTF-8','ignore')
            if div.pre.ul is not None:
                for li in div.pre.ul.findAll('li'):
                    if li.string is not None:
                        con_text= con_text +' '+li.string.strip().encode('UTF-8','ignore')
#                         print li.string.strip().encode('UTF-8','ignore')
#             print '--------'
            if div.h5.string == 'Description':

                full_desc = con_text
#                 print 'desc',full_desc
            elif div.h5.string == 'Requirements':
                full_requ = con_text
#                 print 'requ', full_requ
            else:
                full_othe = con_text
        try:
            cursor.execute('update webjob set full_desc=%s, full_requ=%s, full_othe=%s, job_sour=%s where job_url =%s ',(full_desc,full_requ,full_othe,'scipe',key_url))
               
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )    
        
        connection.commit()
        full_loc = None
        full_post = None
        full_titl = None
        full_comp = None
        full_func = None
        full_entr = None
        full_type = None
        full_educ = None
        full_expe = None
        full_trav = None     
        for div in soup.find_all('div',attrs = {"class":"job-data-basics clearfix"}):
#             print '--------'
#             print div.h5.string
            if div.ul is not None:
                for li in div.ul.findAll('li'):

                    for label in li.findAll('label'):
                        for span in li.findAll('span'):
                            full_info = span.string.strip().encode('UTF-8','ignore')
                        if label.string.strip().encode('UTF-8','ignore') == 'Location:':
                            full_loc = full_info
                        elif label.string.strip().encode('UTF-8','ignore') == 'Posted:':
                            full_post = full_info

                        elif label.string.strip().encode('UTF-8','ignore') == 'Position Title:':
                            full_titl = full_info
                            
                        elif label.string.strip().encode('UTF-8','ignore') == 'Company Name:':
                            full_comp = full_info
                            
                        elif label.string.strip().encode('UTF-8','ignore') == 'Job Function:':
                            full_func = full_info
                            
                        elif label.string.strip().encode('UTF-8','ignore') == 'Entry Level:':
                            full_entr = full_info
                            
                        elif label.string.strip().encode('UTF-8','ignore') == 'Job Type:':
                            full_type = full_info
                            
                        elif label.string.strip().encode('UTF-8','ignore') == 'Min Education:':
                            full_educ = full_info
                            
                        elif label.string.strip().encode('UTF-8','ignore') == 'Min Experience:':
                            full_expe = full_info
                            
                        elif label.string.strip().encode('UTF-8','ignore') == 'Required Travel:':
                            full_trav = full_info

        try:
            cursor.execute('update webjob set full_loc=%s, full_post=%s, full_titl=%s, full_trav=%s, full_comp=%s, full_func=%s, full_entr=%s, full_type=%s, full_educ=%s, full_expe=%s  where job_url =%s '
                                            ,(full_loc,    full_post,    full_titl,   full_trav,   full_comp,   full_func,   full_entr,   full_type,   full_educ,   full_expe,         key_url))
               
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)  # Log it or whatever here
            logger.info(''.join('!! ' + line for line in lines) )    
        
        connection.commit()

        cursor.close()
        connection.close()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )

# getscipe('http://scip.careerwebsite.com/jobseeker/job/26821645/Market%20Intelligence%20Professional/thyssenkrupp%20Management%20Consulting%20GmbH/?vnet=0&str=1&max=25&long=1')

def getsimplyhired(key_url):
    '''
    get full info from simplyhired
    '''
    try:
        branch_url = key_url
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
#         print branch_url
        branch_info = urllib.urlopen(branch_url).read()
     

        soup = BeautifulSoup(branch_info)
        full_desc = None
        full_requ = None
        full_othe = None
        full_loc = None
        full_post = None
        full_titl = None
        full_comp = None
        full_func = None
        full_entr = None
        full_type = None
        full_educ = None
        full_expe = None
        full_trav = None    
        
        for div in soup.find_all('div',attrs = {"class":"jp-header"}):
            for p_name in div.find_all('p',attrs = {"class":"jp-company-name"}):
                full_comp =  p_name.string.strip().encode('UTF-8','ignore')
            
            for h1_title in div.find_all('h1'):
                full_titl =  h1_title.text.strip().encode('UTF-8','ignore')
                
            for p_data in div.find_all('p',attrs = {"class":"jp-company-data"}):
                
                if p_data.strong.string == 'Job location:':
                    
                    full_loc = p_data.text.split(":")[1].strip().encode('UTF-8','ignore')
                
                elif p_data.strong.string == 'Date posted:':
                    
                    full_post = p_data.text.split(":")[1].strip().encode('UTF-8','ignore')

        for div in soup.find_all('div',attrs = {"class":"jp-description"}):
            full_desc_pre = ''
            full_desc_p = ''
            full_div = ''
            if div.text is not None:
                full_div = div.text.strip().encode('UTF-8','ignore')
            for pre_des in div.find_all('pre'):
                
                full_desc_pre = pre_des.string.strip().encode('UTF-8','ignore')
                
            for p in div.find_all('p'):
                full_desc_p = full_desc_p +' '+ p.text.strip().encode('UTF-8','ignore')
                
            full_desc = full_desc_pre +' '+full_desc_p+' '+full_div
            
        

            
        if (full_titl is not None) or (full_comp is not None) or (full_loc is not None) or (full_post is not None) or (full_desc is not None):               
            try:
                cursor.execute('update webjob set full_comp=%s, full_titl=%s, full_loc=%s,full_post=%s, full_desc=%s,  job_sour=%s where job_url =%s '
                                                 ,(full_comp,   full_titl,    full_loc,   full_post,   full_desc,   'simplyhired',    key_url))
                    
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )    
             
            connection.commit()
       
        
        else:
            getupdifined(key_url)

        cursor.close()
        connection.close()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )

# getsimplyhired('http://www.simplyhired.com/job/wubasuqmg7')


def getindeed(key_url):
    '''
    get full info from indeed
    '''
    try:
        branch_url = key_url
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
#         print branch_url
        branch_info = urllib.urlopen(branch_url).read()
     

        soup = BeautifulSoup(branch_info)
        full_desc = None
        full_requ = None
        full_othe = None
        full_loc = None
        full_post = None
        full_titl = None
        full_comp = None
        full_func = None
        full_entr = None
        full_type = None
        full_educ = None
        full_expe = None
        full_trav = None    
        
        for tbody in soup.find_all('table',attrs = {"id":"job-content"}):
#             print tbody
            for div in tbody.find_all('div',attrs = {"id":"job_header"}):
                
                for b_title in div.find_all('b',attrs = {"class":"jobtitle"}):
                    full_titl = b_title.string.strip().encode('UTF-8','ignore')
                    
                for span_comp in div.find_all('span',attrs = {"class":"company"}):
                    full_comp = span_comp.string.strip().encode('UTF-8','ignore')
                    
                for span_loc in div.find_all('span',attrs = {"class":"location"}):
                    full_loc = span_loc.string.strip().encode('UTF-8','ignore')
                    
            con_text=' '
            span_text = ''        
            for span_desc in tbody.find_all('span',attrs = {"id":"job_summary"}):
                if span_desc.text is not None:
                    span_text = span_desc.text.strip().encode('UTF-8','ignore')
                for p_desc in span_desc.find_all('p'):
                    con_text = con_text +'' +p_desc.text.strip().encode('UTF-8','ignore')
                
                full_desc = con_text +' '+span_text

                
#         print full_comp
#         print full_titl
#         print full_loc
#         print full_desc
        
        if (full_titl is not None) or (full_comp is not None) or (full_loc is not None) or (full_desc is not None):               

            try:
                cursor.execute('update webjob set full_comp=%s, full_titl=%s, full_loc=%s, full_desc=%s,  job_sour=%s where job_url =%s '
                                                 ,(full_comp,   full_titl,    full_loc,     full_desc,   'indeed',    key_url))
                    
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)  # Log it or whatever here
                logger.info(''.join('!! ' + line for line in lines) )    
             
            connection.commit()
            
            
        else:
            getupdifined(key_url)
            
            
        cursor.close()
        connection.close()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )


# getindeed('http://www.indeed.com/pagead/clk?mo=r&ad=-6NYlbfkN0Aw1efAMzldDzpoIJt3dh-Ws43S30drXQ6jFQqkIis_u1mFnn__mvNu4rzoHGezSZ0B-L7m3GDeJZ11nQPoXh60erTeumvoNc6sWGxjmzxdUFrnt_JFmtkbg47qZLPQzzJk2CuFH8sa0j-CKbB_laLdKR7tMN2oC32C9fAMOZ3V6Vjw1xevkAAroxlnTOygt9aDVQCq3yZ4sW4IqDu7VUTXMx7llvBohsVGndfdXmwMJ6QJq3PwSXjhGZ7BLm06zWLwSNK8sg4v9N2h4PQ-Q1bjWh4nwvOE5DVkIZWrb6BPdi4OCZ6zuyzlbKcydbJ6uGCpvqfhBn1WisWtWQ9UCPCVgmhJpcFczX1cKKNZhzBPXXPywo7AXF1HBBImGf2oA2eKDG_Kv44fMxTQ8_-ZVzGFDK_I_0zzXve2OzrUu1c_4nOYhdW8vLD_gHn_V613Nw4R0bkUrNNXHY5OEARAz7SSjlV25Y9AKIaUOZZWhcrOpV4KJ440x2o6kokuMv6Hbv9dEjH4Nb3Wuz3M9T9GFXeoA4ZWZi1OIXXABsIvh2GzB__rG9Tqf0j0KMLBu7Tl5Md6Gq6jQAyqgI9SeHfQHAqY1X-xzDko4M4oZoDuTJ1K7lSpD8kSFIPkviq646Q6eLZTspb-VFRTLYf9dDt6X7cTn22jMiuuBsDl2xvrbI7QakHcEOzDut7cAuVVynmRDTC9YCj3bkoTLveZkc44ZPb0qUr3i3jJRyV3PSTq4qpuObb_XQOPcp__DlM0Z7PUACwhiz-DFpPI6YufIup0n_SgWIuViltHsIgNde_kOBFkyeazKLS6eduXyHiJRUpHcVPQP7J2y2nFfIXumwcmtdB7ICtOdSKY3a4QkO4DKJL6ET4Y_r6TC-FejqHyunNqKm1-USKGqJksQDDMcFWkeesUtH7KF-szcMMvgUzIh9d6TZeR0_QKiPdm_Kpf3rxkDPD5q3cmZH1ZoOcadMZmW7t2EZ8SnI4D49bs_1SMqKUAiWGPwyiCWLSW0F1qotPARb2AbfbYPs_lTiEdZYy56bYpF7QKnaC_5mD-_4bFTupE-QRDgFHA5WUAOCw-oWxnKPC76389EUqbkTNKLxVsaCIpHTaT8uGroJcu5xy7H6LcVZO-46Z8Ja1IinFoZatbgsq_nui_cxS5hemZYhZ3uwzsWUkSwxCkq1FmRtwu9MDq9NBIhIp0JwlNvw8yjuyMSmJh8bDK4pI9Pvkfbt00nH3b&p=10&rjs=1&atk=1ae3kqdl1af0lc9q')


def getupdifined(key_url):
    '''
    handle undifined url
    '''
    try:

        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
        

        cursor.execute('update webjob set  job_sour=%s where job_url =%s '
                                             ,('undefined',    key_url))
        connection.commit()

        cursor.close()
        connection.close()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )
        
        
def getBranchInfo():
    
    '''
    get job info from individual web page
    '''
    try:
        connection = psycopg2.connect(dbname = '', user = '',password='')
        cursor = connection.cursor()
        
        cursor.execute('select job_url from webjob where oid >=2603')
        records = cursor.fetchall()
        for record in records:
#             print record
            if 'http://' in record[0]:
                company_web_title = record[0].split('/')[2]
                if 'api.simplyhired.com' in record[0]:
                    print 'get info from simplyhired'
                    branch_url = record[0]
                    getsimplyhired(branch_url)

                elif 'www.indeed.com/pagead/' in record[0]:
                    print 'get info from indeed '
                    branch_url = record[0]
#                     print branch_url
                    getindeed(branch_url)
                else:
                    print 'unedfined website:',company_web_title
                    branch_url = record[0]
                    getupdifined(branch_url)

            else:
                print 'get info from scipe'
                branch_url =  record[0]
                getscipe(branch_url)
                
        cursor.close()
        connection.close()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )

getBranchInfo()

def batch():

    page_number = 26
    getRootByBS4(url_default)
#     print url_default
    for i in range(1,60):
    
        url = url_default + '?vnet=0&max=25&str='+str(page_number)+'&long=1'
        page_number = page_number+25
        i = i+1
#         print url
        getRootByBS4(url)
# batch()
