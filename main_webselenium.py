from itertools import count
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

import os
import sys

import json
import collections
from datetime import date

import main_NLP

class web_manage:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        self.nlp = main_NLP.NLP()
    
    def save_rawdata(self,name_website,data_input):
        data_result = collections.defaultdict(list)
        
        index_count = 0
        
        for data in data_input:
            
            today = date.today()
            
            lang_text = self.nlp.detectlang(data[1])
            
            sentiment = ""
            #print(data_input[0]
            if lang_text  == "th":
                sentiment = self.nlp.senti_th(str(data[1]))
                #sentiment = "unknown"
            elif lang_text == "en":
                sentiment = self.nlp.senti_en(data[1])
            else:
                sentiment = "neutral"
                
            data_result[name_website].append(
                                        { 
                                            "index" : index_count,
                                            "link" : data[0],
                                            "crawler_at": today.strftime("%d-%m-%Y"),
                                            "create_at": today.strftime("%d-%m-%Y"),
                                            "lang" : lang_text,
                                            "header" : data[1],
                                            "content" : data[2],
                                            "sentiment" : sentiment,
                                            "href_link" : data[3]
                                        }
                                    )
            index_count +=1
        
        with open(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"+name_website+".json"), 'w', encoding='utf-8') as f:
            json.dump(dict(data_result), f, ensure_ascii=False, indent=4)
            
    def add_rawdata(self,name_website,data_input):
        print("Add Raw Data",data_input)
        if data_input == []:
            print("error to add none data")
            return
        with open(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"+name_website+".json"), encoding='utf-8') as f:
            data_result = json.load(f)
            
        #data_result = collections.defaultdict(list)
        
        index_count = 0
        
        for data in data_input:
            
            today = date.today()
            
            lang_text = self.nlp.detectlang(data[1])
            
            sentiment = ""
            #print(data_input[0]
            if lang_text  == "th":
                sentiment = self.nlp.senti_th(str(data[1]))
                #sentiment = "unknown"
            elif lang_text == "en":
                sentiment = self.nlp.senti_en(data[1])
            else:
                sentiment = "neutral"
                
            data_result[name_website].append(
                                        { 
                                            "index" : index_count,
                                            "link" : data[0],
                                            "crawler_at": today.strftime("%d-%m-%Y"),
                                            "create_at": today.strftime("%d-%m-%Y"),
                                            "lang" : lang_text,
                                            "header" : data[1],
                                            "content" : data[2],
                                            "sentiment" : sentiment,
                                            "href_link" : data[3]
                                        }
                                    )
            index_count +=1
        
        with open(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"+name_website+".json"), 'w', encoding='utf-8') as f:
            json.dump(dict(data_result), f, ensure_ascii=False, indent=4)

class webselenium_bbc:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        self.nlp = main_NLP.NLP()
        
    def read_link(self,page_num):
        self.link_list = []
        
        bbc_driver = webdriver.Chrome(self.path_driver)
        bbc_driver.get("https://www.bbc.com/news/business")
        
        print("Webdriver - Wait Popup")
        WebDriverWait(bbc_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tp-close"))).click()
        print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage BBC !")
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i,"!")
            time.sleep(1)

            bbc_driver.execute_script("window.scrollTo(0,6000)")
            element_link = bbc_driver.find_elements_by_class_name('qa-heading-link.lx-stream-post__header-link')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in self.link_list:
                    self.link_list.append(href_text)
            
            print("Webdriver - Next Page!")

            bbc_driver.find_element(By.CSS_SELECTOR, ".lx-pagination__nav:nth-child(3) .lx-pagination__controls:nth-child(3) > .lx-pagination__btn:nth-child(1)").click()
            
        print("Webdriver - Num Link :",len(self.link_list))
        print(self.link_list)
        bbc_driver.quit()
        return self.link_list

    def read_content(self,link_in):
        content_list = []
        bbc_driver = webdriver.Chrome(self.path_driver)
        bbc_driver.get("https://www.bbc.com/news/business")
        
        print("Webdriver - Wait Popup")
        WebDriverWait(bbc_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tp-close"))).click()
        print("Webdriver - Close Popup")
        
        for i in range(0,len(link_in)):
            try:
                print("Webdriver - Read Webpage Page :", i+1)
                bbc_driver.get(link_in[i])
                time.sleep(1)
                
                print("Webdriver - Read Heading")
                header_element = bbc_driver.find_element_by_id("main-heading")
                header_text = header_element.text
                print("Heading : ",header_text)
                
                print("Webdriver - Read Content")
                content_text = ""
                content_element = bbc_driver.find_elements_by_class_name('ssrcss-uf6wea-RichTextComponentWrapper.e1xue1i86')
                if content_element == []:
                    content_element = bbc_driver.find_elements_by_class_name('ssrcss-1q0x1qg-Paragraph.eq5iqo00')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                print("Content : ",content_text[0:15])
                
                print("Webdriver - Read href")
                href_list = []
                href_element = bbc_driver.find_elements_by_css_selector(".ssrcss-1gfaiii-InlineLink.e1no5rhv0")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and ("www.bbc.co.uk" in href_text) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
                
                content_list.append([link_in[i],header_text,content_text,href_list])
            except:
                pass
        bbc_driver.quit()
        return content_list
        
        
class webselenium_dailymail:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        dailymail_driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        dailymail_driver.get("https://www.dailymail.co.uk/money/markets/index.html")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(dailymail_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tp-close"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage Dailymail !")
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i,"!")
            time.sleep(2)

            #dailymail_driver.execute_script("window.scrollTo(0,6000)")
            element_link = dailymail_driver.find_elements_by_class_name('linkro-darkred a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in self.link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")

            #dailymail_driver.find_element(By.CSS_SELECTOR, ".lx-pagination__nav:nth-child(3) .lx-pagination__controls:nth-child(3) > .lx-pagination__btn:nth-child(1)").click()
            
        print("Webdriver - Num Link :",len(link_list))
        print(link_list)
        dailymail_driver.quit()
        return link_list

    def read_content(self,link_in):
        content_list = []
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        dailymail_driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        
        for i in link_in:
            if  "https://www.dailymail.co.uk/" not in i :
                continue
            try:
                print("Webdriver - Read Webpage Page :", i)
                dailymail_driver.get(i)
                time.sleep(0.5)
                
                print("Webdriver - Read Heading")
                header_element = dailymail_driver.find_element_by_css_selector("#js-article-text > h2")
                header_text = header_element.text
                print("Heading : ",header_text)
                
                print("Webdriver - Read Content")
                content_text = ""
                content_element = dailymail_driver.find_elements_by_class_name('mol-para-with-font')
                if content_element == []:
                    content_element = dailymail_driver.find_elements_by_class_name('mol-para-with-font')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                print("Content : ",content_text[0:15])
                
                print("Webdriver - Read href")
                href_list = []
                href_element = dailymail_driver.find_elements_by_class_name("rotator-panels.link-bogr1.linkro-ccox a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
                
                content_list.append([i,header_text,content_text,href_list])
            except:
                pass
        dailymail_driver.quit()
        return content_list
        
class webselenium_cnn:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://edition.cnn.com/business")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_css_selector('h3.cd__headline a[href]')

            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
        driver.quit()
        return link_list

    def read_content(self,link_in):
        content_list = []
        driver = webdriver.Chrome(self.path_driver)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try :
                print("Webdriver - Read Webpage Page :", i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_css_selector("body > div.pg-right-rail-tall.pg-wrapper > article > div.l-container > h1")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('zn-body__paragraph')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_body = driver.find_element_by_class_name('zn.zn-body-text.zn-body')
                href_element = href_body.find_elements_by_tag_name("a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list) and "https://" in href_text:
                        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
            except:
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_bangkokpost:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.bangkokpost.com/business/")
        
        print("Webdriver - Wait Popup")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('listnews-text h3 a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            driver.find_element_by_css_selector("#page-link > a").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        driver = webdriver.Chrome(self.path_driver)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1 , i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("article-headline")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('articl-content p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("ins-product-box.ins-element-link.ins-product-link")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)

                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_nbcnews:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.nbcnews.com/business")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('tease-card__headline.tease-card__title.tease-card__title--news.relative a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            #driver.find_element_by_css_selector("#page-link > a").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1)
                driver.get(i)
                time.sleep(0.75)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("article-hero-headline__htag.lh-none-print.black-print")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('article-body__content p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("related-item__link")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)

                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_foxbusiness:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.foxbusiness.com/category/cryptocurrency")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #morepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(0.75)

            element_link = driver.find_elements_by_class_name('collection.collection-river.content .title a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            driver.find_element_by_css_selector("#wrapper > div > div.page-content > main > div.item.item-pagination > ul > li.pagi-item.pagi-next").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            
            print("Webdriver - Read Webpage Page :", count_page+1)
            driver.get(i)
            time.sleep(0.5)

            print("Webdriver - Read Heading")
            header_element = driver.find_element_by_class_name("headline")
            header_text = header_element.text
            print("Heading : ",header_text)

            print("Webdriver - Read Content")
            content_text = ""
            content_element = driver.find_elements_by_class_name('article-body p')
            for content_raw in content_element:
                content_text = content_text + content_raw.text + " "
            content_text = content_text.replace("<br>", "")
            print("Content : ",content_text)

            print("Webdriver - Read href")
            href_list = []
            href_element = driver.find_elements_by_class_name("article-body p a")
            for href_raw in href_element:
                href_text = href_raw.get_attribute('href')
                if (href_text != None) and (href_text not in href_list):
                    href_list.append(href_text)
            print("href : ",href_list)
            
            content_list.append([i,header_text,content_text,href_list])
            count_page +=1
        
        driver.quit()
        
        return content_list
    


class webselenium_tbn:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.thailand-business-news.com/top-news/business")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #morepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('post-outer a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            #driver.find_element_by_css_selector("#wrapper > div > div.page-content > main > div.item.item-pagination > ul > li.pagi-item.pagi-next").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        #caps = DesiredCapabilities().CHROME
        #caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            if i == None or "top-news" in i or "author" in i:
                continue
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)
                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("entry-title")
                header_text = header_element.text
                print("Heading : ",header_text)
                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('entry-content p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)
                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("post-outer a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        return content_list
    
    
    
class webselenium_businesstoday:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.businesstoday.in/crypto")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #morepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('widget-listing-content-section h2 a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            driver.find_element_by_css_selector("#load_more").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(1)
                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("story-heading")
                header_text = header_element.text
                print("Heading : ",header_text)
                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('text-formatted.field.field--name-body.field--type-text-with-summary.field--label-hidden.field__item p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)
                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("BT_sl_title a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    

class webselenium_abcnews:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://abcnews.go.com/Business/")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('ContentRoll__Headline h2 a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            #driver.find_element_by_css_selector("#load_more").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)
                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("Article__Headline__Title")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('Article__Content.story p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("AnchorLink.News__Item.external.flex.News__Item--reverse.flex-row-reverse")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)

                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    

    
    
    
class webselenium_cbc:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.cbc.ca/news/business")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(0.5)

            element_link = driver.find_elements_by_class_name('card.cardDefault')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            #driver.find_element_by_css_selector("#load_more").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("detailHeadline")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('story p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)
            
                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("relatedLink")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_sanook:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.sanook.com/money")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_css_selector('a.jsx-485415509.EntryListImage')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            driver.find_element(By.CSS_SELECTOR, "#__next > div.fullLayout > div:nth-child(5) > div > div.jsx-2535913832.section.clearfix.bottom.SectionLatest > div > div > button").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(1)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_css_selector("#__next > div.fullLayout > div:nth-child(5) > div > div.jsx-608200476 > div.container > div > div.jsx-608200476.col-12.col-lg-8.EntryContent > article > div:nth-child(1) > div.jsx-2761676397.EntryHeading.clearfix > h1")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('jsx-3647499928.jsx-3717305904.EntryReaderInner')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_css_selector("span[class='jsx-2430232205 jsx-1621000947 text-color-money'] > a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                     href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_mrg:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://mgronline.com/tags/%E0%B8%84%E0%B8%A3%E0%B8%B4%E0%B8%9B%E0%B9%82%E0%B8%95")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#box-gdpr > div > a"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_css_selector('figure.article-item.article-item-l-xs.topic-m-sm.topic-l-md.pdd-t-xs-15.pdd-b-xs-15.bd-b-1 > div > a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            #driver.find_element(By.CSS_SELECTOR, "#__next > div.fullLayout > div:nth-child(5) > div > div.jsx-2535913832.section.clearfix.bottom.SectionLatest > div > div > button").click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("header-article h1")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('detail.m-c-font-article')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_css_selector(".article-item.article-item > div > a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page += 1
                pass
        
        driver.quit()
        
        return content_list
    
    

class webselenium_kaohoon:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.kaohoon.com/latest-news")
        
        print("Webdriver - Wait Popup")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('tie-col-md-11.tie-col-sm-10.tie-col-xs-10 a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            driver.find_element_by_class_name('the-next-page').click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(1)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("post-title.entry-title")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('dable-content-wrapper')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                #href_element = driver.find_elements_by_css_selector(".article-item.article-item > div > a")
                #for href_raw in href_element:
                #    href_text = href_raw.get_attribute('href')
                #    if (href_text != None) and (href_text not in href_list):
                #        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_cryptosiam:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://cryptosiam.com/market/")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('si_newsbox__body a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            driver.find_element_by_class_name('next.page-numbers').click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            if "/cryptocurrencies/" in i or "/exchange/" in i or "/market/" in i or "/investment/" in i or "/business/" in i:
                continue
            try:
                print("Webdriver - Read Webpage Page :", count_page+1,i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("si_heading.si_article__title")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('si_article__content p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("si_newsbox__link")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_thairath:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.thairath.co.th/business/investment")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('css-1t0sw8h.e1lqjqum2 a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            driver.find_element_by_class_name('linkmore').click()
            
        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1)
                driver.get(i)
                time.sleep(1)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_css_selector("#article-content > div.css-1hcj7bq.evs3ejl47 > div.css-1eiho0q.evs3ejl55 > h1")
                header_text = header_element.text
                print("Heading : ",header_text)
            
                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_css_selector('#article-content > div.css-1x6s6w6.evs3ejl1 > div:nth-child(2)')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("_tr-box-caption a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    

class webselenium_siambitcoin:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.siambitcoin.com/category/%e0%b8%82%e0%b9%88%e0%b8%b2%e0%b8%a7%e0%b8%aa%e0%b8%b2%e0%b8%a3-%e0%b8%84%e0%b8%a3%e0%b8%b4%e0%b8%9b%e0%b9%82%e0%b8%95/")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('entry-title.td-module-title.wp-dark-mode-ignore a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            try:
                driver.find_element_by_css_selector("[aria-label=next-page]").click()
            except:
                print("Webdriver - Wait Popup")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
                print("Webdriver - Close Popup")
                driver.find_element_by_css_selector("[aria-label=next-page]").click()

        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("tdb-title-text")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_css_selector('#tdi_65 > div > div.vc_column.tdi_68.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_single_content.tdi_78.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type > div')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("wp-dark-mode-ignore")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_amarin:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.amarintv.com/news/economic")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,page_num):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('inner')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            try:
                driver.find_element_by_css_selector("#wrapper > section > div > div.row > div.col-sm-12.text-center > button").click()
            except:
                print("Webdriver - Wait Popup")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
                print("Webdriver - Close Popup")
                driver.find_element_by_css_selector("#wrapper > section > div > div.row > div.col-sm-12.text-center > button").click()

        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_css_selector("div.head")
                header_text = header_element.text
                print("Heading : ",header_text)
                        
                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_css_selector('#_popIn_read_more_container > div > div > div > div.col-md-8 > div.news-detail > div.body')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)
            
                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("inner")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
            
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    


class webselenium_tnn:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.tnnthailand.com/news/wealth/business/")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('newscard--item__content h3 a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")

        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("container--left__header")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_css_selector('body > div.section--read > div.section--read__container > article > div.container--left__content.tnn--article > div.tnn--article__textwrap.fr-view > p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_css_selector("#below-container > ul > li > h3 >a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
                
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
    
class webselenium_khaosod:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://www.khaosod.co.th/economics")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('udblock__permalink')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list:
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            #try:
            #    driver.find_element_by_css_selector("body > main > div:nth-child(4) > div.udpg > ul > li:nth-last-child(1) > a").click()
            #except:
            ##    print("Webdriver - Wait Popup")
            #    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "iClose.closableContainer"))).click()
            #    print("Webdriver - Close Popup")
            #    driver.find_element_by_css_selector("body > main > div:nth-child(4) > div.udpg > ul > li:nth-last-child(1) > a").click()

        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("udsg__main-title")
                header_text = header_element.text
                print("Heading : ",header_text)
                            
                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('udsg__content p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)
                
                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("udblock__title a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
                
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list
    
    
class webselenium_true:
    def __init__(self):
        
        self.path_driver = os.path.join(os.path.dirname(sys.argv[0]), "./webdriver/chromedriver.exe")
        self.list_url = []
        self.link_list = []
        
    def read_link(self,page_num):
        link_list = []
        driver = webdriver.Chrome(self.path_driver)
        driver.get("https://news.trueid.net/economics")
        
        #print("Webdriver - Wait Popup")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))).click()
        #print("Webdriver - Close Popup")
        
        print("Webdriver - Start ScrapePage !")
        #onepage
        for i in range(0,1):
            print("Webdriver - Wait Loading Page",i+1,"!")
            time.sleep(1)

            element_link = driver.find_elements_by_class_name('mb-2 a')
            
            for link_raw in element_link:
                href_text = link_raw.get_attribute('href')
                if href_text not in link_list and href_text != "https://news.trueid.net/economics":
                    link_list.append(href_text)
            
            print("Webdriver - Next Page!")
            try:
                driver.find_element_by_css_selector("#__next > main > div.sc-bczRLJ.fgKgEF > div > div.sc-dkzDqf.eqTjky > section > button").click()
            except:
                print("Webdriver - Wait Popup")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
                print("Webdriver - Close Popup")
                driver.find_element_by_css_selector("#__next > main > div.sc-bczRLJ.fgKgEF > div > div.sc-dkzDqf.eqTjky > section > button").click()

        driver.quit()
        print("Webdriver - Num Link :",len(link_list))
        return link_list

    def read_content(self,link_in):
        content_list = []
        count_page = 0
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(self.path_driver,desired_capabilities=caps)
        #driver.get("https://www.bbc.com/news/business")
        
        for i in link_in:
            try:
                print("Webdriver - Read Webpage Page :", count_page+1, i)
                driver.get(i)
                time.sleep(0.5)

                print("Webdriver - Read Heading")
                header_element = driver.find_element_by_class_name("global__TitleArtileStyle-sc-10c7lju-12.SCyzb")
                header_text = header_element.text
                print("Heading : ",header_text)

                print("Webdriver - Read Content")
                content_text = ""
                content_element = driver.find_elements_by_class_name('style__ContentDetailBox-sc-150i3lj-0.style-sc-150i3lj-1.eXhzIR.hKsNBw p')
                for content_raw in content_element:
                    content_text = content_text + content_raw.text + " "
                content_text = content_text.replace("<br>", "")
                print("Content : ",content_text)

                print("Webdriver - Read href")
                href_list = []
                href_element = driver.find_elements_by_class_name("mb-2 a")
                for href_raw in href_element:
                    href_text = href_raw.get_attribute('href')
                    if (href_text != None) and (href_text not in href_list):
                        href_list.append(href_text)
                print("href : ",href_list)
                
                content_list.append([i,header_text,content_text,href_list])
                count_page +=1
            except:
                count_page +=1
                pass
        
        driver.quit()
        
        return content_list

            
if __name__ == "__main__":
    #test_selenium_bbc = webselenium_bbc()
    #x = test_selenium_bbc.BBC_readlink(1)
    #y = test_selenium_bbc.BBC_readcontent(x)
    #web_manage().save_rawdata("BBC",y)
    
    test_selenium = webselenium_dailymail()
    x = test_selenium.read_link(1)
    y = test_selenium.read_content(x)
    web_manage().save_rawdata("Dailymail",y)
    #true