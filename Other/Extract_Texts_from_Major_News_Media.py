'''
Created on Apr 3, 2017

@author: Xuebin Wei
www.lbsocial.net
Extract texts from major news media webpages 
Very rough extraction
'''
from bs4 import BeautifulSoup
import urllib.request
import re


'''
for any webpages, extract all the visible texts
'''
 
# html = urllib.request.urlopen('') # put the url here
# 
# soup = BeautifulSoup(html.read(), 'html.parser')
# texts = soup.findAll(text=True)

# def visible(element):
#     if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
#         return False
#     elif re.match('<!--.*-->', str(element)):
#         return False
#     elif re.match('[if * <![endif]', str(element)):
#         return False
#     return True
# 
# visible_texts = filter(visible, texts)
# 
# '''
# write the texts into a txt file
# '''
# with open('news.txt', 'bw') as outfile: #define the location of the output
#     for text in visible_texts:
#         try:
#             print(text.encode('utf-8'))
# 
#             outfile.write(text.encode('utf-8'))
#         except:
#             pass

'''
Extract text from JMU news
'''
# html = urllib.request.urlopen('https://www.jmu.edu/news/president/2017/03-mvs-preview-mary-ellen-callahan.shtml') # fill in the url
#  
# soup = BeautifulSoup(html.read(), 'html.parser')
# print (soup.title.text)
# for div_region in soup.find_all('div', id = 'defaultregion' ):
# #     print (div_region)
#     for div_gripdpad in div_region.find_all('div', class_ ='gridpad'):
# #         print (div_gripdpad)
#         for p in div_gripdpad.find_all('p'):
#             print (p.text)
            
            
'''
Extract text from fox news
'''
# html = urllib.request.urlopen('http://www.foxnews.com/politics/2017/04/04/'
#                               'susan-rice-claimed-ignorance-on-trump-team'
#                               '-surveillance-before-role-in-unmasking-revealed.html') # fill in the url
#   
# soup = BeautifulSoup(html.read(), 'html.parser')
# print (soup.title.text)
# for div_article_text in soup.find_all('div',class_ = 'article-text'):
# #     print (div_article_text)
#     for p in div_article_text.find_all('p'):
#         print (p.text)
        
'''
Extract text from cnn
'''
# html = urllib.request.urlopen('http://www.cnn.com/2017/04/04/middleeast/'
#                               'idlib-syria-attack/index.html') # fill in the url
#    
# soup = BeautifulSoup(html.read(), 'html.parser')
# print (soup.title.text)
# for div_body_paragraph in soup.find_all('div',class_ = 'zn-body__paragraph'):
#     print (div_body_paragraph.text)

'''
Extract text from new york time
'''
# import requests
# html = requests.get('https://www.nytimes.com/2017/04/03/us/'
#                               'justice-department-jeff-sessions-baltimore-police.html?_r=0') # fill in the url
#   
# soup = BeautifulSoup(html.content, 'html.parser')
# print (soup.title.text)
# for p_story_body_text in soup.find_all('p',class_ = 'story-body-text story-content'):
#     print (p_story_body_text.text)

'''
Extract text from huffingtonpost
'''
# html = urllib.request.urlopen('http://www.huffingtonpost.com/entry/gop-health-care-deal'
#                               '-pre-existing-conditions_us_58e39db7e4b03a26a365fdf6?') # fill in the url
#     
# soup = BeautifulSoup(html.read(), 'html.parser')
# print (soup.title.text)
# for div_text in soup.find_all('div',class_ = 'content-list-component bn-content-list-text text'):
#     for p in div_text.find_all('p'):
#         print (p.text.encode('utf-8'))
'''
Extract text from yahoo
'''

# html = urllib.request.urlopen('https://www.yahoo.com/news/devin-nunes-returns-'
#                               'home-to-protests-over-his-trump-ties-155939039.html') # fill in the url
#     
# soup = BeautifulSoup(html.read(), 'html.parser')
# print (soup.title.text)
# for article in soup.find_all('article'):
#     for div in article.find_all('div'):
#         for p in div.find_all('p'):
#             print (p.text)

'''
Extract text from nbcnews
'''

# html = urllib.request.urlopen('http://www.nbcnews.com/news/world/syria-chemical-attack-'
#                               'reportedly-kills-dozens-idlib-province-n742416') # fill in the url
#     
# soup = BeautifulSoup(html.read(), 'html.parser')
# print (soup.title.text)
# for div in soup.find_all('div', class_ = 'article-body'):
#     for p in div.find_all('p'):
#         print (p.text)

'''
Extract text from washingtonpost
'''

# html = urllib.request.urlopen('https://www.washingtonpost.com/world/national-security/blackwater-founder-held-secret-seychelles-meeting-to-establish-trump-putin-back-channel/2017/04/03/95908a08-1648-11e7-ada0-1489b735b3a3_story.html?hpid=hp_hp-top-table-main'
#                               '_seychelles-0438pm-1%3Ahomepage%2Fstory&utm_term=.b9f05806a056') # fill in the url
#     
# soup = BeautifulSoup(html.read(), 'html.parser')
# print (soup.title.text)
# for article in soup.find_all('article', itemprop = 'articleBody'):
#     for p in article.find_all('p'):
#         print (p.text.encode('utf-8'))
