
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup
import re
import collections
import json
import unicodecsv
import random
import praw
import pprint
from urlparse import urljoin


# In[2]:

###create a function to connect to reddit -- REMOVED
def redditConnect():
    user_agent = "Hannah's test 0.3"
    r = praw.Reddit(user_agent=user_agent)

redditConnect()


# In[3]:

###create a function to randomly select from a set of articles
def itemselect(dictx):
    keyx = random.choice(dictx.keys())
    print keyx
    print str(dictx[keyx])


# In[4]:

###create a function to connect to reddit get the top articles from a particlar subreddit and store their title and URL
def reddit(subred):
    #redditConnect()
    user_agent = "Hannah's test 0.3"
    r = praw.Reddit(user_agent=user_agent)
    subred_submissions=r.get_subreddit(subred).get_top(limit=15)
    subred_list = {}
    for thing in subred_submissions:
        subred_name = thing.title
        subred_list[subred_name] = thing.permalink
    itemselect(subred_list)



# In[5]:

###create a function to pull the featured article of the day from Wikipedia and print it out along with relevant links
def wikitfa():
    wiki = requests.get('https://en.wikipedia.org/wiki/Main_Page')
    wiki_soup = BeautifulSoup(wiki.text)
    wiki_tfa = wiki_soup.find("div", id="mp-tfa").text
    tfa_articles = {}
    print "Today's Featured Article from Wikipedia"
    print wiki_tfa
    print ("Read more:")
    for a in wiki_soup.select('#mp-tfa a'):
        base = "https://en.wikipedia.org/wiki/"
        tfa_article = a.text
        tfa_link = a.get('href')
        tfa_articles[tfa_article] = urljoin(base,tfa_link)
        print tfa_article
        print urljoin(base,tfa_link)


# In[6]:

def makesoup(url):
    page_content = requests.get(url)
    page_soup = BeautifulSoup(page_content.text)
    print page_soup
                    
###create a function to pull today's "did you know" items from Wikipedia and print one at random
def wikidyk():
    wiki = requests.get('https://en.wikipedia.org/wiki/Main_Page')
    wiki_soup = BeautifulSoup(wiki.text)
    ##makesoup('https://en.wikipedia.org/wiki/Main_Page')
    wiki_dyk = wiki_soup.select('#mp-dyk > ul > li')
    dyk_list = {}
    print "Did you know"
    for li in wiki_dyk:
        base = "https://en.wikipedia.org/wiki/"
        dyk_text = li.text
        dyk_link = li.b.a.text
        dyk_url = li.b.a.get('href')
        dyk_list[dyk_text] = urljoin(base,dyk_url)
    itemselect(dyk_list)



# In[7]:

###create a function to pull the news items from Wikipedia and print one at random
def wikiitn():
    wiki = requests.get('https://en.wikipedia.org/wiki/Main_Page')
    wiki_soup = BeautifulSoup(wiki.text)
    wiki_itn = wiki_soup.select('#mp-itn > ul > li')
    itn_list = {}
    print "In the news:"
    for li in wiki_itn:
        base = "https://en.wikipedia.org/wiki/"
        itn_text = li.text
        try:
            itn_link = li.b.a.text
        except:
            itn_link = li.b.text
        try:
            itn_url = li.b.a.get('href')
        except: 
            itn_url = li.a.b.get('href')
        itn_list[itn_text] = urljoin(base, itn_url)
    itemselect(itn_list)


# In[8]:

###create a function to pull the "on this day" items from Wikipedia and print one at random
def wikiotd():
    wiki = requests.get('https://en.wikipedia.org/wiki/Main_Page')
    wiki_soup = BeautifulSoup(wiki.text)
    wiki_otd = wiki_soup.select('#mp-otd > ul > li')
    otd_list = {}
    print "On this day:"
    for li in wiki_otd:
        base = "https://en.wikipedia.org/wiki/"
        otd_text = li.text
        try:
            otd_link = li.b.a.text
        except:
            otd_link = li.b.text
        try:
            otd_url = li.b.a.get('href')
        except: 
            otd_url = li.a.b.get('href')
        otd_list[otd_text] = urljoin(base, otd_url)
    itemselect(otd_list)


# In[9]:

###create a function to get a random trending paste from pastebin
def pastebin():
    pastebin = requests.get('http://pastebin.com/trends')
    pastebin_soup = BeautifulSoup(pastebin.text)
    paste_tr = pastebin_soup.table.find_all("tr")
    paste_list = {}
    for tr in paste_tr[1:len(paste_tr)]:
        base = "http://pastebin.com/"
        paste_name = tr.td.a.text
        paste_link = tr.td.a.get('href')
        paste_list[paste_name] = urljoin(base, paste_link)
    itemselect(paste_list)


# In[10]:

###create a function to randomly select an article source and call the appropriate function to get an article
def randompull():
    options = {"Today's Featured Article": wikitfa, "Did You Know": wikidyk, "Trending Paste": pastebin, "Random Subreddit": reddit}
    subreddits = ["AskReddit", "creepy", "NoSleep", "UnresolvedMysteries", "askscience", "WritingPrompts", "FanTheories", "100yearsago", "netflixbestof", ]
    source = random.choice(options.keys())
    if source == "Random Subreddit":
        sub_source = random.choice(subreddits)
        reddit(sub_source)
    else:
        options[source]()


# In[11]:

###create a function to let the user choose the article source -- REMOVED
###def wikiChoose():
    ##wikiSubsource = raw_input("Would you like to read Today's Featured Article, a 'Did You Know', or an article about a current event in the news or something that occurred on this day in history?")
    #return wikiSubsource

###def redditChoose():
    #userSubreddit = raw_input("Which Subreddit would you like to read from? Choose from AskReddit, creepy, NoSleep, UnresolvedMysteries, askscience, WritingPrompts, FanTheories, 100yearsago, or tell me another Subreddit you like.")
        


# In[15]:

def again():
    again = raw_input("Would you like another?")
    if again.lower() == "yes" or again.lower() == "y":
        ask()
    else:
        print ("Ok, goodbye!")
        
def userPull():
    userSource = raw_input("Ok, which source would you like to read from - Wikipedia, Reddit, or Pastebin?").lower()
    if userSource == "pastebin":
        pastebin()
    elif userSource == "wikipedia" or userSource == "wiki":
        while True:
            wikiSubsource = raw_input("Would you like to read Today's Featured Article, a 'Did You Know', or an article about a current event in the news or something that occurred on this day in history?").lower()
            if "featured" in wikiSubsource:
                wikitfa()
                break
            elif "did you know" in wikiSubsource or "dyk" in wikiSubsource:
                wikidyk()
                break
            elif "news" in wikiSubsource or "current" in wikiSubsource:
                wikiitn()
                break
            elif "history" in wikiSubsource or "historical" in wikiSubsource or "historic" in wikiSubsource or "this day" in wikiSubsource or "otd" in wikiSubsource:
                wikiotd()
                break
            else:
                print ("I'm sorry, I didn't quite understand. Can you tell me again?")
                True
    elif userSource == "reddit":
        userSubreddit = raw_input("Which Subreddit would you like to read from? Choose from AskReddit, creepy, NoSleep, UnresolvedMysteries, askscience, WritingPrompts, FanTheories, 100yearsago, or tell me another Subreddit you like.")
        reddit(userSubreddit)
    again()
    print


# In[16]:

def ask():
    choice = raw_input("Ok, " + userName + ", would you like to pick something to read or let me pick for you? Just say 'you pick' or 'I'll pick.'")
    print
    if choice.lower() == "you pick":
        print
        randompull()
    else:
        print
        userPull()
    print 
    print    


# In[17]:

userName = raw_input("Hello, what's your name?")
ask()

