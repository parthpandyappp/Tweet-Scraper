import requests
from bs4 import BeautifulSoup
from config import TWITTER_URL
import re

CONTENT_CLASS_NAME = "dir-ltr"
CONTENT_CONTAINER_TAGS = ["div"]
EMPTY_ITEMS = [None, "", "None", "\n"]
AGENTS= 'Nokia5310XpressMusic_CMCC/2.0 (10.10) Profile/MIDP-2.1 '\
'Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; '\
'Nokia5310XpressMusic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile'


def get_elements(twitter_handle):
  url = TWITTER_URL + twitter_handle
  response = requests.get(url)
  html = response.content
  
  soup = BeautifulSoup(html, features="html.parser")
  
  return soup.find_all(
    CONTENT_CONTAINER_TAGS, 
    attrs={"class": CONTENT_CLASS_NAME})
    
def get_user_tweets(twitter_handle):
  elements = get_elements(twitter_handle)
  
  tweets = []
  
  for post in elements:
    for text in post.contents:
      if text.string not in EMPTY_ITEMS:
        tweets.append(text.string)
        
  return tweets


def clean_tweets_data(tweets):
  emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
  
  url_patterns = re.compile(r"http\S+", re.DOTALL)
  mentions_patterns = re.compile(r"@\S+", re.DOTALL)
  
  cleaned_tweets = []
  
  for tweet in tweets:
    txt_without_mentions = mentions_patterns.sub(r"",tweet)
    txt_without_urls = url_patterns.sub(r"",txt_without_mentions)
    txt_without_emojis = emoji_pattern.sub(r"",txt_without_urls)
    
    cleaned_tweets.append(txt_without_emojis)
    
  return cleaned_tweets  