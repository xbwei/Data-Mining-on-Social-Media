'''
Created on Apr 3, 2017

@author: Xuebin Wei
www.lbsocial.net
Extract texts from any webpages 
'''
from bs4 import BeautifulSoup
import urllib.request
import re 
html = urllib.request.urlopen('') # fill in the url
soup = BeautifulSoup(html.read(), 'html.parser')
texts = soup.findAll(text=True)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    elif re.match('[if * <![endif]', str(element)):
        return False

    return True

visible_texts = filter(visible, texts)
with open('news.txt', 'bw') as outfile: #define the location of the output
    for text in visible_texts:
        try:
            print(text.encode('utf-8'))

            outfile.write(text.encode('utf-8'))
        except:
            pass
