import requests
import tweepy
import pandas as pd
import re
import emoji
import nltk
import pythainlp
from langdetect import detect as detect_lang

import spacy
import collections
import operator

import time as time
from datetime import datetime as datetime
import pythainlp
from nltk.sentiment import SentimentIntensityAnalyzer

class NLP:
    def __init__(self):
        self.aiforthai_apikey = "****** You-API-Key ******"
        spacy.load('en_core_web_sm')
        
    def senti_th(self,text):
        #print("senti_th")
        try:
            url = "https://api.aiforthai.in.th/ssense"
            params = {'text': str(text)}
            headers = {
                'Apikey': self.aiforthai_apikey
                }
            response = requests.get(url, headers=headers, params=params)
            output = response.json()
            #print(response.json())
            try:
                if output["sentiment"]["polarity"] == "":
                    return "neutral"
                else:
                    return(output["sentiment"]["polarity"])
            except:
                return "neutral"
        except:
            print("Senti Thai Error")
            return "neutral"
        
    def senti_en(self,text):
        #print("senti_en")
        sia = SentimentIntensityAnalyzer()
        output = sia.polarity_scores(text)

        if output["compound"] == 0:
            return "neutral"
        elif output["compound"] > 0:
            return "positive"
        elif output["compound"] < 0:
            return "negative"
        #return(output["compound"])
        
    def clean_text(self,text):
        #print("clear_text")
        
        datas = text

        mention_pattern = r'@'
        hashtag_pattern = r"#"
        web_pattern = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
        enter_pattern = r'[\n\t]'
        punctuations = r'[\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ\“\”\—\ı\İ\+\’\,\.\,\.\–\'\£\.\,\']'
        #emoji_pattern = r'([^\u0E00-\u0E7Fa-zA-Z])'
        del_ment = re.sub(mention_pattern, '', datas)
        del_tags = re.sub(hashtag_pattern, '', del_ment)
        del_web = re.sub(web_pattern, '', del_tags)
        del_enter = re.sub(enter_pattern, '', del_web)
        del_punct = re.sub(punctuations, '', del_enter)
        
        del_emoji = emoji.get_emoji_regexp().sub(u'',del_punct)
        result = " ".join(del_emoji.split())
        #del_all = " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "",del_punct).split())
        return result 
        
        return clear_text
    
    def clean_text_ver1(self,text):
        #print("clear_text")
        
        datas = text

        # ตัด #
        pattern  = re.compile(r"(#+[a-zA-Z0-9(_)|ก-๙(_)0-9]{1,})")
        out_str_hashtags = pattern.sub("", datas)

        # ตัด @
        pattern  = re.compile(r"(@+[a-zA-Z0-9(_)|ก-๙(_)0-9]{1,})")
        out_str_add = pattern.sub("", out_str_hashtags)

        # ตัด emoji
        str_output = emoji.get_emoji_regexp().sub(u'',out_str_add)

        # ตัด link
        pattern  = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
        out_str_link = pattern.sub("", str_output)  

        # ตัด ตัดอักษร+ตัวเลข
        pattern  = re.compile(r"([A-Za-z-_]+[\d]+[\w]*|[\d]+[A-Za-z-_]+[\w]*)")
        out_str_number = pattern.sub("", out_str_link)  

        # ตัด ตัวเลข
        pattern  = re.compile(r"([๑-๙(_)0-9]{1,})")
        out_str_ = pattern.sub("", out_str_number)

        clear_text = out_str_.replace('\n', ' ')
        
        return clear_text
    
    def text_intercept(self, text):
        all_emoji = emoji.UNICODE_EMOJI
        for i in text:
            if i in all_emoji:
                text = text.replace(i, '')
        mention_pattern = r'(?:@[\w_]+)'
        hashtag_pattern = r"(?:\#+[\w\ก-๙_]+[\w\ก-๙\'_\-]*[\w\ก-๙_]+)"
        web_pattern = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
        enter_pattern = r'[\n\t]'
        punctuations = r'[\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ\+\ı]'
        del_ment = re.sub(mention_pattern, '', text)
        del_tags = re.sub(hashtag_pattern, '', del_ment)
        del_web = re.sub(web_pattern, '', del_tags)
        del_enter = re.sub(enter_pattern, '', del_web)
        del_punct = re.sub(punctuations, '', del_enter)
        return del_punct
    
    def tokenize(self,lang,text):
        if lang == "th":
            return pythainlp.word_tokenize(text, keep_whitespace=False)
        elif lang == "en":
            return nltk.word_tokenize(text)
        else:
            #print("tokenize error")
            return pythainlp.word_tokenize(text, keep_whitespace=False)
        

    def detectlang(self,text):
        try:
            lang = str(detect_lang(text))
        except:
            lang = "unknown"
        return lang
    
    def nlp(self,keyword,text):
        stopword_en = list(spacy.lang.en.stop_words.STOP_WORDS) # 362 words
        stopword_th = list(pythainlp.corpus.thai_stopwords()) # 1030 words
        process = pythainlp.word_tokenize(text,engine="newmm",keep_whitespace=False) # list type
        #process = nltk.word_tokenize(text)
        result = []
        for word in process:
            if(word in stopword_th or word in stopword_en or word.lower() == keyword.lower() or word.isdigit()):
                continue
            else:
                result.append(word)
        return result
    
    def frequency_word(self, text_list):
        frequency = dict(collections.Counter(text_list))
        try:
            frequency.pop(' ')
        except:
            pass

        try:
            ranking = dict(sorted(frequency.items(), key=operator.itemgetter(1), reverse=True)[:100])
        except:
            pass
        return ranking

if __name__ == "__main__":
    sentiment = NLP()
    #print(sentiment.senti_th('สาขานี้พนักงานน่ารักให้บริการดี'))
    #print(sentiment.senti_en('Wow, NLTK is really powerful!'))
    print(sentiment.clean_text('น้องมาวันอาทิตย์ ไปสุ่มกันได้นะจ๊ะ " a""__-- ,น้องมาวันอาทิตย์ ไปสุ่มกันได้นะจ๊ะ🥠 #JibBNK48 https://t.co/2bh9J4V3RX,JibBNK48'))
    print(sentiment.text_intercept('น้องมาวันอาทิตย์ ไปสุ่มกันได้นะจ๊ะ " a""__-- ,น้องมาวันอาทิตย์ ไปสุ่มกันได้นะจ๊ะ🥠 #JibBNK48 https://t.co/2bh9J4V3RX,JibBNK48'))
    #x = sentiment.clean_text('น้องมาวันอาทิตย์ ไปสุ่มกันได้นะจ๊ะ  ,น้องมาวันอาทิตย์ ไปสุ่มกันได้นะจ๊ะ🥠 #JibBNK48 https://t.co/2bh9J4V3RX,JibBNK48')
    
    #y = sentiment.tokenize("th","Billboard Hot Trending Songs Last 24 Hrs 15 LALISA +3 18 MONEY +2 Please bring both songs up Keep going and do it correctly Add 3 words and not just copy amp paste Separate LALISA and MONEY in different tweets LISA LALISA MONEY")
    #print(y)
    
    x = sentiment.nlp([],[])
    print(x)
    
    y = sentiment.frequency_word(x)
    print(y)