print("Hello you are in feed_file_generator file")

from datetime import datetime
import pandas as pd
import re

#filter the warning messages
import warnings
warnings.filterwarnings('ignore')

import requests
from bs4 import BeautifulSoup

def pull_data(url):
    response = requests.get(url)
    response.raise_for_status()

    content = response.content#resp.content.decode('utf8')
    #print(content)
    return content

def pull_blog_data(pageContent, df):
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      title_text = item.findChildren('title')[0].getText()
      link_text = item.findChildren('link')[0].getText()
      date = item.findChildren('pubDate')[0].getText()
      date = datetime.strptime(item.findChildren('pubDate')[0].getText(), "%a, %d %b %Y %H:%M:%S %Z")
      date = datetime.strftime(date.date(), "%m/%d/%Y")
      image_content = item.findChildren('content:encoded')[0].getText()
      image_parsed = BeautifulSoup(image_content, 'html.parser')
      image_src = image_parsed.img['src']
      df.loc[len(df)] = [date, title_text, link_text, image_src]
      #print(f"-----------Card values {ind}-----------------")
      #print(date, "\n", title_text, "\n", link_text, "\n", image_src)
    return df

def pull_hackernews_data(pageContent, df):
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """
    webpage_parsed = BeautifulSoup(pageContent, 'html.parser')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll("div", {"class": "body-post"})):
      if ind == 15:
        break
      title_text = item.findChildren('h2', {"class": "home-title"})[0].getText()
      title_text = item.a['href']
      link_text = item.h2.getText()
      date = item.findAll("div", {"class": "item-label"})[0].getText()
      date = re.sub('[^A-Za-z0-9]+', ' ', date)
      date = date[0:[d.start() for d in re.finditer(r" ", date)][3]].strip()
      # date format July 22 2022 want July 01, 2022
      datetime.strptime(date, "%B %d %Y").strftime("%B %d, %Y")
      image_src = item.img['data-src']
      df.loc[len(df)] = [date, title_text, link_text, image_src]
      #print(f"-----------Card values {ind}-----------------")
      #print(date, "\n", title_text, "\n", link_text, "\n", image_src)
    return df

def pull_hackernews_data_old(pageContent, df):
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      if ind == 15:
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

def pull_cybernews_data(pageContent, df):
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """
    webpage_parsed = BeautifulSoup(pageContent, 'html.parser')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    #index = len(df)
    image_list, titles_list, url_list, date_list = [], [], [], []

    # image carousel news
    for item in webpage_parsed.findAll('div'):
      div_heading = item['class'][0]

      if div_heading == 'focus-articles__image':
        image_src = item['style']
        image_src = image_src[(image_src.find("'"))+1:-3:]
        image_list.append(image_src)
      
      if div_heading == 'cells__item':
        if item.a is not None:
          link_text = item.a['href']
          if item.img is not None:
            image_src = item.img['data-src']
            image_list.append(image_src)
            url_list.append(link_text)
        if item.time is not None:
          date = item.time.getText().replace('\n',"").strip()
          date = datetime.strptime(date, "%d %B %Y").strftime("%B %d, %Y")
          date_list.append(date)
      
      if div_heading == 'focus-articles__info':
        link_text = item.a['href']
        url_list.append(link_text)

      if div_heading == 'heading':
        title_text = item.getText()
        titles_list.append(title_text)
        
      if div_heading == 'focus-articles__meta':
        date = item.getText().replace('\n',"").strip()
        date = datetime.strptime(date, "%d %B %Y").strftime("%B %d, %Y")
        date_list.append(date)

    for item in webpage_parsed.findAll('h3'):
      h3_class = item['class'][0]
      if h3_class == 'heading':
        title_text = item.getText()
        titles_list.append(title_text)
      

    print(len(image_list), len(titles_list), len(url_list), len(date_list))
    for index in range(10):
      df.loc[len(df)] = [date_list[index], titles_list[index], url_list[index], image_list[index]]
    
    return df

def pull_threatpost_data(pageContent, df):
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      if ind == 15:
        break
      title_text = item.findChildren('title')[0].getText()
      link_text = item.findChildren('link')[0].getText()
      date = item.findChildren('pubDate')[0].getText()
      # date format Thu, 30 Jun 2022 17:20:30 +0000 want July 01, 2022
      # trim the PDT and then convert
      date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime("%B %d, %Y")
      #date = datetime.strptime(item.findChildren('pubDate')[0].getText(), "%a, %d %b %Y %h:%M:%S %Z")
      #date = datetime.strftime(date.date(), "%m/%d/%Y")
      image_content = item.findChildren('media:content')[0]
      image_src = image_content.get('url')
      df.loc[len(df)] = [date, title_text, link_text, image_src]
      #print(f"-----------Card values {ind}-----------------")
      #print(date, "\n", title_text, "\n", link_text, "\n", image_src)
    return df

def pull_krebs_data(pageContent, df):
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      if ind == 15:
        break
      title_text = item.findChildren('title')[0].getText()
      link_text = item.findChildren('link')[0].getText()
      date = item.findChildren('pubDate')[0].getText()
      # date format Wed, 22 Jun 2022 13:06:34 +0000 want July 01, 2022
      # trim the PDT and then convert
      date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime("%B %d, %Y")
      image_content = item.findChildren('content:encoded')[0].getText()
      image_content = image_content[image_content.find('<img')::]
      image_content = image_content[image_content.find('src=')+5::]
      image_src = image_content[:image_content.find(' ')-1:]
      df.loc[len(df)] = [date, title_text, link_text, image_src]
    return df

def pull_wired_data(pageContent, df):
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      if ind == 15:
        break
      title_text = item.findChildren('title')[0].getText()
      link_text = item.findChildren('link')[0].getText()
      date = item.findChildren('pubDate')[0].getText()
      # date format Fri, 01 Jul 2022 12:15:47 +0000 want July 01, 2022
      # trim the PDT and then convert
      date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime("%B %d, %Y")
      image_content = item.findChildren('media:thumbnail')[0]
      image_src = image_content.get('url')
      df.loc[len(df)] = [date, title_text, link_text, image_src]
    return df

def pull_nakedsec_data(pageContent, df):
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      if ind == 15:
        break
      title_text = item.findChildren('title')[0].getText()
      link_text = item.findChildren('link')[0].getText()
      date = item.findChildren('pubDate')[0].getText()
      # date format Fri, 01 Jul 2022 12:15:47 +0000 want July 01, 2022
      # trim the PDT and then convert
      date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime("%B %d, %Y")
      image_content = item.findChildren('media:content')[0]
      image_src = image_content.get('url')
      df.loc[len(df)] = [date, title_text, link_text, image_src]
    return df

def pull_welive_data(pageContent, df):
    webpage_parsed = BeautifulSoup(pageContent, 'lxml-xml')
    webpage_title = webpage_parsed.title
    print(webpage_title)
    
    for ind, item in enumerate(webpage_parsed.findAll('item')):
      if ind == 10:
        break
      title_text = item.findChildren('title')[0].getText()
      link_text = item.findChildren('link')[0].getText()
      date = item.findChildren('pubDate')[0].getText()
      # date format Fri, 01 Jul 2022 12:15:47 +0000 want July 01, 2022
      # trim the PDT and then convert
      date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime("%B %d, %Y")
      image_src = item.findChildren('image')[0].getText()
      df.loc[len(df)] = [date, title_text, link_text, image_src]
    return df

def gen_feed_file(file_name, blog_file):
    #create empty dataframe
    blog_df = pd.DataFrame(columns=['Date Created', 'Title', 'URL', 'Image'])

    URL = "https://medium.com/feed/@vinothu"
    URL = "https://blog.vinothv.com/feed"
    print(f"Pulling data from {URL}...")
    blog_df = pull_blog_data(pull_data(URL), blog_df)
    print(f"Done pulling data.")
    print(blog_df.shape)
    blog_df.to_excel(blog_file, index=False)
    
    #create empty dataframe
    news_df = pd.DataFrame(columns=['Date Created', 'Title', 'URL', 'Image'])

    URL = "https://thehackernews.com/feeds/posts/default"
    print(f"Pulling data from {URL}...")
    news_df = pull_hackernews_data(pull_data(URL), news_df)
    print(f"Done pulling data.")
    print(news_df.shape)

    URL = "https://threatpost.com/feed/"
    print(f"Pulling data from {URL}...")
    news_df = pull_threatpost_data(pull_data(URL), news_df)
    print(f"Done pulling data.")
    print(news_df.shape)
    
    URL = "https://krebsonsecurity.com/feed/"
    print(f"Pulling data from {URL}...")
    news_df = pull_krebs_data(pull_data(URL), news_df)
    print(f"Done pulling data.")
    print(news_df.shape)
    
    URL = "https://www.wired.com/feed/category/security/latest/rss"
    print(f"Pulling data from {URL}...")
    news_df = pull_wired_data(pull_data(URL), news_df)
    print(f"Done pulling data.")
    print(news_df.shape)
    
    URL = "https://nakedsecurity.sophos.com/feed/"
    print(f"Pulling data from {URL}...")
    news_df = pull_nakedsec_data(pull_data(URL), news_df)
    print(f"Done pulling data.")
    print(news_df.shape)
    
    #URL = "https://www.welivesecurity.com/feed/"
    #print(f"Pulling data from {URL}...")
    #news_df = pull_welive_data(pull_data(URL), news_df)
    #print(f"Done pulling data.")
    #print(news_df.shape)
        
    #URL = "https://cybernews.com/news/"
    #print(f"Pulling data from {URL}...")
    #news_df = pull_cybernews_data(pull_data(URL), news_df)
    #print(f"Done pulling data.")
    #print(news_df.shape)

    print(f"Saving the file {file_name}")
    news_df.to_excel(file_name, index=False)
    print(f"Saved the file {file_name}")
    
    print(f"Exiting gen_feed_file method..")
    
    return blog_df, news_df
