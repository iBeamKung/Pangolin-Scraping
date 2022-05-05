from cgi import test
from tracemalloc import start
from numpy import diff
import tweepy
import pandas as pd
import re
import emoji
import nltk
import pythainlp
from langdetect import detect as detect_lang
import time as time
from datetime import datetime as datetime
import pythainlp
import os
import sys

from datetime import date, timedelta

from threading import Thread

import main_NLP

def checkday(since,until) :
    list_file = os.listdir(os.path.join(os.path.dirname(sys.argv[0]), "./database/twitter/"))
        #list_file = os.listdir(os.path.join(os.path.dirname(sys.argv[0]), "../database/twitter/"))
        
    have_days = []
    for file in list_file:
        #df = pd.read_csv(os.path.join(os.path.dirname(sys.argv[0]), "../database/twitter/"+file))
        df = pd.read_csv(os.path.join(os.path.dirname(sys.argv[0]), "./database/twitter/"+file))
        a= df['create_at'].drop_duplicates().to_list()
        print("A:",a)
        have_days.append(a)
    print("have Day :",have_days)

    day_input = ['2022-04-10', '2022-03-30' , '2022-04-09']

    def Diff(li1, li2):
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif

    result = Diff(day_input,have_days)
    print("result :",result)

    


if __name__ == "__main__":
    checkday(0,0)