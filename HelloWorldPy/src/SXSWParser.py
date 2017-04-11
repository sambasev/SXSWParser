'''
Created on Apr 10, 2017

@author: samba_000
'''
import urllib2
import re
from bs4 import BeautifulSoup
from operator import itemgetter

def hello(myInput):
    return "Hello World: " + myInput

#Finds and prints text section in soup
def findText(pText,soup):
    tag = soup.find(text=pText)
    if tag is not None and tag.parent is not None:
        pTag = tag.parent.parent
        
        print("\n---FOUND TEXT---")
        for sibling in pTag.findAll(text=True):
            print(sibling.string)
        print("---END----")
    

def parseLink(web_url):
    print "\nParsing "  + web_url.geturl()
    soup = BeautifulSoup(web_url.read(), "html.parser")
    
    tag = soup.find(text="Public Film Contact")
    if tag is not None and tag.parent is not None:
        pTag = tag.parent.parent
        
        print("\n---PUBLIC FILM CONTACT---")
        pTag = pTag.find_next(text=True)
        if pTag: print("Name  : " + pTag.find_next(text=True))
        pTag = pTag.find_next(text=re.compile("@"))
        if pTag: print("Email : " + pTag.string)
        pTag = pTag.find_next(text=re.compile("[0-9]"))
        if pTag: print("Number: " + pTag.string)
        
        print("---END----")

#    for sibling in tag.next_siblings:
#        print(sibling.string)
    tag = soup.find(text="Publicity Contact")
    if tag is not None and tag.parent is not None:
        pTag = tag.parent.parent
        
        print("\n---PUBLICITY CONTACT---")
        pTag = pTag.find_next(text=True)
        if pTag: print("Name  : " + pTag.find_next(text=True))
        pTag = pTag.find_next(text=re.compile("@"))
        if pTag: print("Email : " + pTag.string)
        pTag = pTag.find_next(text=re.compile("[0-9]"))
        if pTag: print("Number: " + pTag.string)
        
        print("---END----")
      
    
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
        