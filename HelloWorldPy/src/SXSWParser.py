'''
Created on Apr 10, 2017

@author: samba_000
'''
import urllib2
import unicodedata
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter

films = defaultdict(dict)

def hello(myInput):
    return "Hello World: " + myInput

def printDict(d):
    for key,value in d.items():
        print key + "->" + value
    
#Finds and prints text section in soup
def findText(pText,soup):
    tag = soup.find(text=pText)
    if tag is not None and tag.parent is not None:
        pTag = tag.parent.parent
        
        print("\n---FOUND TEXT---")
        for sibling in pTag.findAll(text=True):
            print(sibling.string)
        print("---END----")
    
'''
ParseLink will open the URL (of the SXSW Film) and populate the following database:
films Dict: {'Beyonce': {info}}

info Dict: {'pfName': 'John', \
            'pfMail': 'me@gmail.com', \
            'pfNumber': '123-456-7890', \
            'pName':   'AppleSeed',\
            'pfMail': 'me2@gmail.com', \
            'pfNumber': ''}
'''
def parseLink(web_url):
    info = {}
    print "\nParsing "  + web_url.geturl()
    soup = BeautifulSoup(web_url.read(), "html.parser")
    #Get Film Name
    tag = soup.find('h1', class_="event-name")
    if tag is not None:
        title = tag.string.strip()
        print("FILM: " + title)
    #findText("Credits", soup)
    #Get Contact Info
    tag = soup.find(text="Public Film Contact")
    if tag is not None and tag.parent is not None:
        pTag = tag.parent.parent
        
        print("\n---PUBLIC FILM CONTACT---")
        #Skip "Public Film Contact" Title
        pTag = pTag.find_next(text=True)
        if pTag:
            pfName = pTag.find_next(text=True).strip()
            info['pfName'] = pfName 
            print("Name  : " + pfName)
        pTag = pTag.find_next(text=re.compile("@"))
        if pTag: 
            pfMail = pTag.string.strip()
            info['pfMail'] = pfMail
            print("Email : " + pfMail)
        pTag = pTag.find_next(text=re.compile("[0-9]"))
        if pTag:
            pfNum = pTag.string.strip() 
            info['pfNum'] = pfNum
            print("Number: " + pfNum)
        
        print("---END----")
 
#    for sibling in tag.next_siblings:
#        print(sibling.string)
    tag = soup.find(text="Publicity Contact")
    if tag is not None and tag.parent is not None:
        pTag = tag.parent.parent
        
        print("\n---PUBLICITY CONTACT---")
        pTag = pTag.find_next(text=True)
        if pTag:
            pName = pTag.find_next(text=True).strip()
            info['pName'] = pName 
            print("Name  : " + pName)
        pTag = pTag.find_next(text=re.compile("@"))
        if pTag: 
            pMail = pTag.string.strip()
            info['pMail'] = pMail
            print("Email : " + pMail)
        pTag = pTag.find_next(text=re.compile("[0-9]"))
        if pTag:
            pNum = pTag.string.strip() 
            info['pNum'] = pNum
            print("Number: " + pNum)
        
        print("---END----")
        films[title.strip()] = info
        print("info Dict: ")
        printDict(info)
        print(json.dumps(films, indent=4))
     
    
#myInput = raw_input("Please enter name:")
#print(hello(myInput))

try :
    web_page = urllib2.urlopen("http://schedule.sxsw.com/2017/films/section/Music%20Video%20Competition").read()
    soup = BeautifulSoup(web_page, "html.parser")
except urllib2.HTTPError :
    print("HTTPERROR!!")
except urllib2.URLError :
    print("URLERROR!")
        
#print(soup.prettify())
#Traverse site and get all music links
L = []
for link in soup.find_all('a', href=re.compile("films\/65916")):
    dir_link = "http://schedule.sxsw.com" + link.get('href')
#    print(link.get('href'))
    L.append(dir_link)

#For each link, traverse site and Map Contact info    
for item in L:
    try :
        web_url = urllib2.urlopen(item)
        parseLink(web_url)
    except urllib2.HTTPError :
        print("HTTPERROR!!")
    except urllib2.URLError :
        print("URLERROR!")    
        