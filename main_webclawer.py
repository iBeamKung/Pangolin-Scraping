from email import header
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk

import os
import sys
import shutil

import ast

import collections
from datetime import date, timedelta
from datetime import datetime as datetime
import json

import main_NLP
import structure_web
import main_webselenium

import eel

class webclawer:
    def __init__(self):
        self.list_url = []
        #f = open(os.path.join(os.path.dirname(sys.argv[0]), "./list_url.txt"), "r")
        #for i in f.readlines():
        #    #print(i.strip())
        #    self.list_url.append(i.strip())
        #print(self.list_url)
        self.list_url.append("https://www.bbc.com/news/business")
        self.list_url.append("https://www.dailymail.co.uk/money/markets/index.html")
        self.list_url.append("https://edition.cnn.com/business")
        
        self.list_url.append("https://www.sanook.com/money")
        
        self.filterwebsite = []
        
        self.nlp = main_NLP.NLP()
        self.web_manage = main_webselenium.web_manage()
        
        self.clawer_abcnews = main_webselenium.webselenium_abcnews()
        self.clawer_amarin = main_webselenium.webselenium_amarin()
        self.clawer_bangkokpost = main_webselenium.webselenium_bangkokpost()
        self.clawer_bbc = main_webselenium.webselenium_bbc()
        self.clawer_businesstoday = main_webselenium.webselenium_businesstoday()
        
        self.clawer_cbc = main_webselenium.webselenium_cbc()
        self.clawer_cnn = main_webselenium.webselenium_cnn()
        self.clawer_dailymail = main_webselenium.webselenium_dailymail()
        self.clawer_foxbusiness = main_webselenium.webselenium_foxbusiness()
        self.clawer_kaohoon = main_webselenium.webselenium_kaohoon()
        
        self.clawer_khaosod = main_webselenium.webselenium_khaosod()
        self.clawer_mrg = main_webselenium.webselenium_mrg()
        self.clawer_nbcnews = main_webselenium.webselenium_nbcnews()
        self.clawer_sanook = main_webselenium.webselenium_sanook()
        self.clawer_siambitcoin = main_webselenium.webselenium_siambitcoin()
        
        self.clawer_tbn = main_webselenium.webselenium_tbn()
        self.clawer_thairath = main_webselenium.webselenium_thairath()
        self.clawer_tnn = main_webselenium.webselenium_tnn()
        self.clawer_trueid = main_webselenium.webselenium_true()
        self.clawer_cryptosiam = main_webselenium.webselenium_cryptosiam()
    
    def get_website_database(self):
        list_data = []
        
        list_database = os.listdir(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"))
        
        datajson = {"total_website":0,"total_webpage":0,"website":{}}
        
        for website_data in list_database:
            with open(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"+website_data), encoding='utf-8') as f:
                data = json.load(f)
            datajson["total_website"] += 1
            datajson["website"][website_data[0:-5]] = {}
            datajson["website"][website_data[0:-5]]["total_page"] = len(data[website_data[0:-5]])
                
        for database in list_database:
            list_data.append([database[0:-5], datajson["website"][database[0:-5]]["total_page"]])
        return list_data
    
    def get_website_filter(self,website):
        if website in self.filterwebsite:
            return 1
        else:
            return 0
        
    def set_website_filter(self,website,state):
        if(state == 0):
            if website in self.filterwebsite:
                self.filterwebsite.remove(website)
        else:
            if website not in self.filterwebsite:
                self.filterwebsite.append(website)
        print(self.filterwebsite)
    
    def web_deletewebsite(self,keyword):
        list_database = os.listdir(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"))
        if keyword in list_database:
            shutil.rmtree(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"+keyword+".json"))
            #os.rmdir(os.path.join(os.path.dirname(sys.argv[0]), "./database/twitter/"+keyword))
        print(self.filterwebsite)
        
    def get_website_page(self,website):
        list_have_data = []
        list_date = []
        
        sentiment = []
        count_all = 0
        count_pos = 0
        count_neg = 0
        count_neu = 0
        
        list_text = []
        list_href = []
        
        related_words = []
        related_links = []
        
        index_count = 0
            
        progress = 0
        progress = 0
        #eel.set_progress_text("Loading - "+ keyword)
        #eel.set_progress(len(list_datefile),progress)
        with open(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"+website+".json"), encoding='utf-8') as f:
            data = json.load(f)
        
        for i in range(0,len(data[website])):
            progress +=1
            eel.set_progress_text("Loading Webpage - " + website + " - " + str(progress) +"/" + str(len(data[website])))
            eel.set_progress(len(data[website]),progress)
            #re-format date XXXX-XX-XX -> xx/xx/xxxx
            date_raw = data[website][i]["crawler_at"]
            x = date_raw.split("-")
            date_convert = x[2]+"/"+x[1]+"/"+x[0]
            
            
            list_have_data.append(
                                    {
                                        "index" : index_count,
                                        "link" : data[website][i]["link"],
                                        "crawler_at" : date_convert,
                                        "create_at" : date_convert,
                                        "lang": data[website][i]["lang"],
                                        "header" : data[website][i]["header"],
                                        "content" : data[website][i]["content"],
                                        "sentiment" : data[website][i]["sentiment"],
                                        "href_link" : data[website][i]["href_link"],
                                    }
                                )
            
            if data[website][i]["sentiment"] == "positive":
                count_pos += 1
            elif data[website][i]["sentiment"] == "negative":
                count_neg += 1
            elif data[website][i]["sentiment"] == "neutral":
                count_neu += 1
            count_all +=1
            
            if isinstance(data[website][i]["content"], list):
                y = self.nlp.clean_text(' '.join(data[website][i]["content"]))
                list_text.extend(self.nlp.nlp(website,y))
            else:
                y = self.nlp.clean_text(data[website][i]["content"])
                list_text.extend(self.nlp.nlp(website,y))
                
            list_href.extend(data[website][i]["href_link"])
                
            index_count += 1
        
        try:
            sentiment = [str(int(count_pos/count_all * 100))+"%",str(int(count_neg/count_all * 100))+"%",str(int(count_neu/count_all * 100))+"%"]
        except:
            sentiment = [0,0,0]
        
        print(list_href)
        frq_word = self.nlp.frequency_word(list_text)
        frq_href = self.nlp.frequency_word(list_href)
        
        for key in frq_word:
            related_words.append({"count" : frq_word[key], "word": key})
            
        for key in frq_href:
            related_links.append({"count" : frq_href[key], "link": key})
            
        eel.set_progress_text("Loading Webpage - " + website + " - " + "Success!")
            
        return [list_have_data,sentiment,related_words,related_links]
    
    
    def search_web(self,keyword):
        
        print("Searching Web -","Keyword :",keyword)
        
        list_have_data = []
        index_count = 0
        header_have = 0
        
        sentiment = []
        count_all = 0
        count_pos = 0
        count_neg = 0
        count_neu = 0
        
        list_text = []
        list_link = []
        related_words = []
        related_links = []
        
        
        
        list_file = os.listdir(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"))
        
        print("folder read :",list_file)
        print("filter read :",self.filterwebsite)
        for i in self.filterwebsite:
            if i+".json" in list_file:
                print(i+".json")
                list_file.remove(i+".json")
        print("folder clean :",list_file)
        
        progress = 0
        eel.set_progress(len(list_file),0)
        
        for web in list_file:
            print("Searching",web)
            progress += 1
            eel.set_progress(len(list_file),progress)
            eel.set_progress_text("Searching - " + web[0:-5])
            
            with open(os.path.join(os.path.dirname(sys.argv[0]), "./database/web/"+web), encoding='utf-8') as f:
                data = json.load(f)
                
            for i in range(0,len(data[web[0:-5]])):
                header_have = 0
                get_words = self.nlp.tokenize(data[web[0:-5]][i]["lang"],data[web[0:-5]][i]["header"])
                for j in get_words:
                    if j.lower() == keyword.lower():
                        list_have_data.append(
                                                {
                                                    "index" : index_count,
                                                    "link" : data[web[0:-5]][i]["link"],
                                                    "crawler_at": data[web[0:-5]][i]["crawler_at"],
                                                    "create_at": data[web[0:-5]][i]["create_at"],
                                                    "lang" : data[web[0:-5]][i]["lang"],
                                                    "header" : data[web[0:-5]][i]["header"],
                                                    "content" : data[web[0:-5]][i]["content"],
                                                    "sentiment" : data[web[0:-5]][i]["sentiment"],
                                                    "href_link" : data[web[0:-5]][i]["href_link"]
                                                }
                                            )
                        if data[web[0:-5]][i]["sentiment"] == "positive":
                            count_pos += 1
                        elif data[web[0:-5]][i]["sentiment"] == "negative":
                            count_neg += 1
                        elif data[web[0:-5]][i]["sentiment"] == "neutral":
                            count_neu += 1
                        count_all +=1
                        
                        clean_content = self.nlp.clean_text(data[web[0:-5]][i]["header"]+data[web[0:-5]][i]["content"])
                        
                        list_text.extend(self.nlp.nlp(keyword,clean_content))
                        list_link.extend(data[web[0:-5]][i]["href_link"])
                        
                        index_count += 1
                        header_have = 1
                        break
                if header_have == 1:
                    break
                get_words = self.nlp.tokenize(data[web[0:-5]][i]["lang"],data[web[0:-5]][i]["content"])
                for l in get_words:
                    if l.lower() == keyword.lower():
                        list_have_data.append(
                                                {
                                                    "index" : index_count,
                                                    "link" : data[web[0:-5]][i]["link"],
                                                    "crawler_at": data[web[0:-5]][i]["crawler_at"],
                                                    "create_at": data[web[0:-5]][i]["create_at"],
                                                    "lang" : data[web[0:-5]][i]["lang"],
                                                    "header" : data[web[0:-5]][i]["header"],
                                                    "content" : data[web[0:-5]][i]["content"],
                                                    "sentiment" : data[web[0:-5]][i]["sentiment"],
                                                    "href_link" : data[web[0:-5]][i]["href_link"]
                                                }
                                            )
                        if data[web[0:-5]][i]["sentiment"] == "positive":
                            count_pos += 1
                        elif data[web[0:-5]][i]["sentiment"] == "negative":
                            count_neg += 1
                        elif data[web[0:-5]][i]["sentiment"] == "neutral":
                            count_neu += 1
                        count_all +=1
                        
                        clean_content = self.nlp.clean_text(data[web[0:-5]][i]["header"]+data[web[0:-5]][i]["content"])
                        
                        list_text.extend(self.nlp.nlp(keyword,clean_content))
                        list_link.extend(data[web[0:-5]][i]["href_link"])
                        
                        index_count += 1
                        break
                    
        eel.set_progress_text("Searching - Done!")
        
        try:
            sentiment = [str(int(count_pos/count_all * 100))+"%",str(int(count_neg/count_all * 100))+"%",str(int(count_neu/count_all * 100))+"%"]
        except:
            sentiment = [0,0,0]
        
        frq_word = self.nlp.frequency_word(list_text)
        for key in frq_word:
            related_words.append({"count" : frq_word[key], "word": key})
            
        frq_link = self.nlp.frequency_word(list_link)
        for key in frq_link:
            related_links.append({"count" : frq_link[key], "link": key})
                
        if list_have_data == []:
            print("No Data In Database")
            return []
        else:
            return [[list_have_data,sentiment,related_words,related_links]]
        
    def addwebsite(self,name,website):
        if name == "abcnew":
            result = self.clawer_abcnews.read_content([website])
            self.web_manage.add_rawdata("ABCNews",result)
        if name == "amarin":
            result = self.clawer_amarin.read_content([website])
            self.web_manage.add_rawdata("Amarin",result)
        if name == "bangkokpost":
            result = self.clawer_bangkokpost.read_content([website])
            self.web_manage.add_rawdata("BangkokPost",result)
        if name == "bbc":
            result = self.clawer_bbc.read_content([website])
            self.web_manage.add_rawdata("BBC",result)
        if name == "businesstoday":
            result = self.clawer_businesstoday.read_content([website])
            self.web_manage.add_rawdata("Businesstoday",result)
            
        if name == "cbc":
            result = self.clawer_cbc.read_content([website])
            self.web_manage.add_rawdata("CBC",result)
        if name == "cnn":
            result = self.clawer_cnn.read_content([website])
            self.web_manage.add_rawdata("CNN",result)
        if name == "dailymail":
            result = self.clawer_dailymail.read_content([website])
            self.web_manage.add_rawdata("Dailymail",result)
        if name == "foxbusiness":
            result = self.clawer_foxbusiness.read_content([website])
            self.web_manage.add_rawdata("Dailymail",result)
        if name == "kaohoon":
            result = self.clawer_kaohoon.read_content([website])
            self.web_manage.add_rawdata("Kaohoon",result)
            
        if name == "khaosod":
            result = self.clawer_khaosod.read_content([website])
            self.web_manage.add_rawdata("Khaosod",result)
        if name == "mrg":
            result = self.clawer_mrg.read_content([website])
            self.web_manage.add_rawdata("MRGOnline",result)
        if name == "nbcnews":
            result = self.clawer_nbcnews.read_content([website])
            self.web_manage.add_rawdata("NBCNews",result)
        if name == "sanook":
            result = self.clawer_sanook.read_content([website])
            self.web_manage.add_rawdata("Sanook",result)
        if name == "siambitcoin":
            result = self.clawer_siambitcoin.read_content([website])
            self.web_manage.add_rawdata("Siambitcoin",result)
            
        if name == "tbn":
            result = self.clawer_tbn.read_content([website])
            self.web_manage.add_rawdata("TBN",result)
        if name == "thairath":
            result = self.clawer_thairath.read_content([website])
            self.web_manage.add_rawdata("Thairath",result)
        if name == "tnn":
            result = self.clawer_tnn.read_content([website])
            self.web_manage.add_rawdata("TNN",result)
        if name == "trueid":
            result = self.clawer_trueid.read_content([website])
            self.web_manage.add_rawdata("trueID",result)
        if name == "cryptosiam":
            result = self.clawer_cryptosiam.read_content([website])
            self.web_manage.add_rawdata("CryptoSiam",result)
            
    def clawer_data(self):
        print("Start Clawer All Website")
        return 0
        read = self.clawer_abcnews.read_link(1)
        result = self.clawer_abcnews.read_content(read)
        self.web_manage.add_rawdata("ABCNews",result)

        read = self.clawer_amarin.read_link(1)
        result = self.clawer_amarin.read_content(read)
        self.web_manage.add_rawdata("Amarin",result)

        read = self.clawer_bangkokpost.read_link(1)
        result = self.clawer_bangkokpost.read_content(read)
        self.web_manage.add_rawdata("BangkokPost",result)

        read = self.clawer_bbc.read_link(1)
        result = self.clawer_bbc.read_content(read)
        self.web_manage.add_rawdata("BBC",result)

        read = self.clawer_businesstoday.read_link(1)
        result = self.clawer_businesstoday.read_content(read)
        self.web_manage.add_rawdata("Businesstoday",result)
            

        read = self.clawer_cbc.read_link(1)
        result = self.clawer_cbc.read_content(read)
        self.web_manage.add_rawdata("CBC",result)

        read = self.clawer_cnn.read_link(1)
        result = self.clawer_cnn.read_content(read)
        self.web_manage.add_rawdata("CNN",result)

        read = self.clawer_dailymail.read_link(1)
        result = self.clawer_dailymail.read_content(read)
        self.web_manage.add_rawdata("Dailymail",result)

        read = self.clawer_foxbusiness.read_link(1)
        result = self.clawer_foxbusiness.read_content(read)
        self.web_manage.add_rawdata("Dailymail",result)

        read = self.clawer_kaohoon.read_link(1)
        result = self.clawer_kaohoon.read_content(read)
        self.web_manage.add_rawdata("Kaohoon",result)
        

        read = self.clawer_khaosod.read_link(1)
        result = self.clawer_khaosod.read_content(read)
        self.web_manage.add_rawdata("Khaosod",result)

        read = self.clawer_mrg.read_link(1)
        result = self.clawer_mrg.read_content(read)
        self.web_manage.add_rawdata("MRGOnline",result)

        read = self.clawer_nbcnews.read_link(1)
        result = self.clawer_nbcnews.read_content(read)
        self.web_manage.add_rawdata("NBCNews",result)

        read = self.clawer_sanook.read_link(1)
        result = self.clawer_sanook.read_content(read)
        self.web_manage.add_rawdata("Sanook",result)

        read = self.clawer_siambitcoin.read_link(1)
        result = self.clawer_siambitcoin.read_content(read)
        self.web_manage.add_rawdata("Siambitcoin",result)


        read = self.clawer_tbn.read_link(1)
        result = self.clawer_tbn.read_content(read)
        self.web_manage.add_rawdata("TBN",result)

        read = self.clawer_thairath.read_link(1)
        result = self.clawer_thairath.read_content(read)
        self.web_manage.add_rawdata("Thairath",result)

        read = self.clawer_tnn.read_link(1)
        result = self.clawer_tnn.read_content(read)
        self.web_manage.add_rawdata("TNN",result)

        read = self.clawer_trueid.read_link(1)
        result = self.clawer_trueid.read_content(read)

        read = self.clawer_cryptosiam.read_link(1)
        result = self.clawer_cryptosiam.read_content(read)
        self.web_manage.add_rawdata("CryptoSiam",result)

if __name__ == "__main__":
    testclawer = webclawer()
    #testclawer.clawer()
    #testclawer.clawer_json()
    print(testclawer.get_web_database())
    #testclawer.search_web_json("kevin")
    #x = get_all_link().get_sanook("https://www.sanook.com/money/")
    #print(x)
    #data = structure_web.Sanook("https://www.sanook.com/money/866399/")
    #print(data.title)
    #print(data.body)
    #print(x)
    #print(testclawer.search_web("kevin"))
    #print(testclawer.load_csv())
    
    