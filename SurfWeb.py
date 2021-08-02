#!/usr/bin/env python
# coding: utf-8

# # Surf CDM

# #### Tsu Erh Lin
# ###### Feb 15  2021

# In[1]:


from urllib.request import urlopen
from html.parser import HTMLParser
from urllib.parse import urljoin
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import operator


# In[2]:


url = 'https://law.depaul.edu/'


# In[3]:


AllData = set()
class Collector(HTMLParser):
    'Collects hyperlink URLs'
    
    def __init__(self, url):
        'Initializes parser, the url, tags, and lists'
        
        HTMLParser.__init__(self)   # Inheriant the initialize setting of HTMLParser
        self.url = url              # Set url as the inserted url
        self.tags = None            # Assign a none value to tags
        self.links = []             # Assign a empty list to links
        
    def handle_starttag(self, tag, attrs):
        'Collects hyperlink URLs in their absolute format'
        self.tags = tag             # Let the tags as the tag that has been collect
        if tag == 'a':              # If tag equals to 'a', the href link tag
            for attr in attrs:      # If the attribute in the set of attributes
                if attr[0] == 'href':                      # If the first index of attribute is 'href'
                    absolute = urljoin(self.url, attr[1])  # Construct absolute URL
                    if absolute[:4] == 'http':             # Collect HTTP URLs
                        self.links.append(absolute)        # Append the absolute URL to the links list
        
                        
    def getLinks(self):
        'returns hyperlinks URLs in their absolute format'
        return self.links
    
    def handle_data(self, data):
        'Collect the data from the site'
        global AllData
        allTags = ['p','li','h1','h2','h3','h4','h5','h6']   # Prepare a list of tags that may appears in the content
        if self.tags in allTags:                             # If tags appears in the all tags list, collect the data
            AllData.add(data)
    
    def getData(self):
        'Return collected data'
        global AllData
        return AllData        


# In[4]:


def wordTokenize(content):
    'Return clean content'
    
    content = list(content)                   # Conver the set() type value into list
    lemmatizer = WordNetLemmatizer()          # Use the WordNetLemmatizer function
    cleanCon = []                             # Assign a empty list
    for i in content:                         # For each content in content list
        i = i.lower()                         # Convert all words into lower case
        tokens = nltk.word_tokenize(i)        # Use nltk word tokenize function to do tokenization
        for n in tokens:                      # For each word in tokens
            lemCon = lemmatizer.lemmatize(n)  # Lemmatize each word
            cleanCon.append(lemCon)           # Append the clean word ino cleanCon list
            
    return cleanCon


# In[5]:


def DelStopwords(file, cleanCon):
    'Delet the stopwords'
    
    infile = open(file, 'r')                    # Open the stopwords txt
    stopwords = infile.read()                   # Read the stopwords file into stopwords
    infile.close()                              # Clost the file
    stopwords = stopwords.strip().split('\n')   # Strip and split the file
    
    filtered = []                               # Assign a empty list to filtered
    for word in cleanCon:                       # For index in cleanCon list
        if word not in stopwords:               # For those words are not in stopwords, append to the filtered list
            filtered.append(word)
    return filtered


# In[6]:


visited = set()   # Initialize visited to an empty set

def crawl(url):
    '''a recursive web crawler that calls analyze() on every visited web page'''
    
    global visited
    links = analyze(url)                        # analyze() returns a list of hyperlink URLs in web page url

    for link in links:                                                 # For each link in links 
        if link not in visited:                                        # If the link is not in the visited set
            if ('/law.depaul.edu/' in link) and (len(visited) < 600):   # If the link include '/law.depaul.edu/'
                try:
                    visited.add(link)       # Visited set add the link
                    crawl(link)             # recursively continue crawl from every link in links
                except:
                    pass


# In[7]:


CollectData = set()   # Initialize Collect Data to an empty set
def analyze(url):
    'returns list of http links in url, in absolute format'
    
    global CollectData
    print('\n\nVisiting', url)
    
    # obtain links in the web page
    content = urlopen(url).read().decode()         # Open, read and decode the content of inserted url
    collector = Collector(url)                     # Use the Collector function
    collector.feed(content)                        # Feed content to the function
    index = collector.getData()                    # Use the getData fucntion of the collector and assign the data to index
    urls = collector.getLinks()                    # Use the getLinks function in the collector and assign those urls to urls
    
    cleanCon = wordTokenize(index)
    fil = DelStopwords('stopwords.txt', cleanCon)
    for i in fil:
        CollectData.add(i)
    
    return urls
    


# In[8]:


def frequency(CollectData):
    'Count the word frequency and return top 25'

    dic = {}                              # Assign a empty dictionary to dic
    Data = list(CollectData)              # Convert the CollectData set to a list
    for word in Data:                     # For each word in Data
        if word not in dic:               # If the word not in the dictionary
            dic[word] = 1                 # Add the word in the dictionary and frequency as 1
        else:                             # If the word is in the dictionary
            dic[word] = dic[word] + 1     # The frequency +1
    
    sortDic = sorted(dic.items(), key = operator.itemgetter(1), reverse = True)   # Sort the dictionary
    Top25 = sortDic[:26]                  # Select the top 25 in the dictionary
    return Top25


# In[ ]:




