print("Hello you are in feed_file_generator file")

from datetime import datetime
import pandas as pd

import requests
from bs4 import BeautifulSoup

def pull_data:
    response = requests.get(url)
    response.raise_for_status()

    content = response.content#resp.content.decode('utf8')
    #print(content)
    return content

def pull_hackernews_data(pageContent, df):
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      if ind == 10:
        break
      title_text = item.findChildren('title')[0].getText()
      link_text = item.findChildren('link')[0].getText()
      date = item.findChildren('pubDate')[0].getText()
      # date format Fri, 01 Jul 2022 03:03:44 PDT want July 01, 2022
      # trim the PDT and then convert
      date = datetime.strptime(date[0:-4:], "%a, %d %b %Y %H:%M:%S").strftime("%B %d, %Y")
      #date = datetime.strptime(item.findChildren('pubDate')[0].getText(), "%a, %d %b %Y %h:%M:%S %Z")
      #date = datetime.strftime(date.date(), "%m/%d/%Y")
      image_content = item.findChildren('media:thumbnail')[0]
      image_src = image_content.get('url')
      df.loc[len(df)] = [date, title_text, link_text, image_src]
      #print(f"-----------Card values {ind}-----------------")
      #print(date, "\n", title_text, "\n", link_text, "\n", image_src)
    return df
