from email import header
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk

import os
import sys

import ast

class BBC:
    def __init__(self, url:str):
        article = requests.get(url)
        self.url = url
        self.soup = BeautifulSoup(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_body(self) -> list:
        body = self.soup.find('article',attrs={'class': 'ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6'})
        if(body== None):
            #print("error",self.url)
            body = self.soup.find('article',attrs={'class': 'ssrcss-1s49f8x-StyledMediaItem elwf6ac5'})
        return [p.text for p in body.find_all("p")]
    
    def get_title(self) -> str:
        return self.soup.find('h1',attrs={'id': 'main-heading'}).text
    
    def get_link_list(self):
        elements = self.soup.find_all('a', href=True, attrs={'class': 'qa-heading-link lx-stream-post__header-link'})
        link_list = []
        for a in elements:
            print("https://www.bbc.com"+a['href'])
            link_list.append("https://www.bbc.com"+a['href'])
            
        return link_list
    
class Dailymail:
    def __init__(self, url:str):
        article = requests.get(url)
        self.url = url
        self.soup = BeautifulSoup(article.content, "html.parser")
        #print(self.soup.prettify())
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_body(self) -> list:
        body = self.soup.find_all('p',attrs={"class":"mol-para-with-font"})
        #print(body)
        list_body = []
        for i in body:
            list_body.append(i.text[:-1])
        return list_body
    
    def get_title(self) -> str:
        title = self.soup.find('div', id="js-article-text").h2.text
        return title
    
    def get_link_drill(self):
        body = self.soup.find_all(class_="ssrcss-7gqlvc-PromoLink e1f5wbog0")
        for x in body:
            print(x.get('href'))
        return body
    
class CNN:
    def __init__(self, url:str):
        article = requests.get(url)
        self.url = url
        self.soup = BeautifulSoup(article.content, "html.parser")
        #print(self.soup.prettify())
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_title(self) -> str:
        #title = self.soup.find_all('div', class="l-container").h1.text
        title = self.soup.find('h1',attrs={"class":"pg-headline"})
        return title.text
        
    def get_body(self) -> list:
        body = self.soup.find_all('div',attrs={"class":"zn-body__paragraph"})
        #print(body)
        list_body = []
        for i in body:
            list_body.append(i.text)
        return list_body
    
    def get_link_drill(self):
        body = self.soup.find_all(class_="ssrcss-7gqlvc-PromoLink e1f5wbog0")
        for x in body:
            print(x.get('href'))
        return body
    
class Prachachat:
    def __init__(self, url:str):
        article = requests.get(url)
        self.url = url
        self.soup = BeautifulSoup(article.content, "html.parser")
        #print(self.soup.prettify())
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_title(self) -> str:
        #title = self.soup.find_all('div', class="l-container").h1.text
        title = self.soup.find('h1',attrs={"class":"entry-title"})
        return title.text
        
    def get_body(self) -> list:
        body = self.soup.find_all('div',attrs={"class":"td-post-content"})
        #print(body)
        list_body = []
        for i in body:
            list_body.append(i.text)
        return list_body
    
    def get_link_drill(self):
        body = self.soup.find_all(class_="ssrcss-7gqlvc-PromoLink e1f5wbog0")
        for x in body:
            print(x.get('href'))
        return body
    
class Khaosod:
    def __init__(self, url:str):
        article = requests.get(url)
        self.url = url
        self.soup = BeautifulSoup(article.content, "html.parser")
        print(self.soup.prettify())
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_title(self) -> str:
        #title = self.soup.find_all('div', class="l-container").h1.text
        title = self.soup.find('h1',attrs={"class":"udsg__main-title"})
        print(title)
        x = title.text
        x = x.replace('\n', ' ').replace('\r', '').strip()
        return x
        
    def get_body(self) -> list:
        body = self.soup.find_all('div',attrs={"class":"udsg__content"})
        #print(body)
        list_body = []
        for i in body:
            x = i.text
            x = " ".join(x.split())
            #x = x.replace('\n', ' ').replace('\r', '').strip()
            list_body.append(x)
        return list_body
    
    def get_link_drill(self):
        body = self.soup.find_all(class_="ssrcss-7gqlvc-PromoLink e1f5wbog0")
        for x in body:
            print(x.get('href'))
        return body
    
class Sanook:
    def __init__(self, url:str):
        article = requests.get(url)
        self.url = url
        self.soup = BeautifulSoup(article.content, "html.parser")
        #print(self.soup.prettify())
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_title(self) -> str:
        #title = self.soup.find_all('div', class="l-container").h1.text
        title = self.soup.find('h1',attrs={"class":"jsx-2761676397 title"})
        #print(title)
        x = title.text
        x = x.replace('\n', ' ').replace('\r', '').strip()
        return x
        
    def get_body(self) -> list:
        body = self.soup.find_all('div',attrs={"class":"jsx-3647499928 jsx-3717305904 EntryReaderInner"})
        #print(body)
        list_body = []
        for i in body:
            x = i.text
            x = " ".join(x.split())
            #x = x.replace('\n', ' ').replace('\r', '').strip()
            list_body.append(x)
        return list_body
    
    def get_link_drill(self):
        body = self.soup.find_all(class_="ssrcss-7gqlvc-PromoLink e1f5wbog0")
        for x in body:
            print(x.get('href'))
        return body