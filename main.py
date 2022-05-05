from unittest import result
import eel
import os
import sys
import pandas as pd

from datetime import date, timedelta
from datetime import datetime as datetime

import main_NLP
import main_twitter
import main_webclawer

Twitter = main_twitter.Twitter_API()
Webclawer = main_webclawer.webclawer()

################ Twitter

@eel.expose
def get_twittertrend():
  return Twitter.get_twitter_trend()

@eel.expose
def get_twitterdatabase():
  return Twitter.get_twitter_database()

@eel.expose
def get_twittercalendardate():
  return Twitter.get_twitter_calendardate()

@eel.expose
def get_twitterfilterkeyword(keyword):
  print(keyword)
  return Twitter.get_twitter_filterkeyword(keyword)

@eel.expose
def get_twitterdatekeyword(keyword):
  print("get_twitterdatekeyword :",keyword)
  return Twitter.get_twitter_date(keyword)

@eel.expose
def set_twitterfilterkeyword(keyword,state):
  print(keyword,state)
  return Twitter.set_twitter_filterkeyword(keyword,state)

@eel.expose
def twitter_deletekeyword(keyword):
  print(keyword)
  return Twitter.twitter_deletekeyword(keyword)

@eel.expose
def twitter_deletedate(keyword,date):
  print(keyword)
  return Twitter.twitter_deletedate(keyword,date)

@eel.expose
def twitter_printkeyword(keyword):
  print(keyword)
  out = Twitter.get_twitter_tweet(keyword)
  eel.print_tweetdata(out)


@eel.expose
def searchTweet(data_input):
  print("Data in :",data_input)
  
  if(data_input[0] == ""):
    eel.showalert_nulltext()
    pass
  else:
    out = Twitter.search(data_input[0].split(","),data_input[1])
    if out == []:
      print("No Data in Data!!!!!!!!")
      eel.showalert_nulldata()
      eel.showalert_searchdata()
      for date in data_input[1]:
        if datetime.strptime(date, '%Y-%m-%d').date() < datetime.today().date() - timedelta(days=7):
          continue
        Twitter.twitter_clawer("#"+data_input[0],date,700)
      out = Twitter.search(data_input[0].split(","),data_input[1])
      eel.print_tweetdata(out)
      eel.refresh_twitter()
    else:
      print("Clawer +++++")
      for listdata in out[1]:
        if datetime.strptime(listdata[1], '%Y-%m-%d').date() < datetime.today().date() - timedelta(days=7):
          continue
        Twitter.twitter_clawer(listdata[0],listdata[1],500)
      
      out = Twitter.search(data_input[0].split(","),data_input[1])
      
      print("Have Data")
      eel.print_tweetdata(out[0])
      eel.showalert_successdata()

@eel.expose
def confrim_craw(x):
  print("")

@eel.expose
def crawlerTweet(data_input):
  print("Data in Crawler :",data_input)
    
  if(data_input[0] == ""):
    eel.showalert_nulltext()
    pass
  else:
    for date in data_input[1]:
        if datetime.strptime(date, '%Y-%m-%d').date() < datetime.today().date() - timedelta(days=7):
          continue
        Twitter.twitter_clawer("#"+data_input[0],date,700)
    eel.refresh_twitter()
    eel.showalert_successcrawler()

################ Web Scraping

@eel.expose
def searchWeb(x):
  print("Data in :",x)
  if(x== ""):
    eel.showalert_nulltext()
    pass
  else:
    out = Webclawer.search_web(x)
    print("Succ")
    if out == []:
      print("No Data in Data!!!!!!")
      eel.showalert_nulldata()
    else:
      print("Suc222c")
      print(out)
      eel.print_webdata(out[0])
      eel.showalert_successdata()
      
@eel.expose
def get_websitedatabase():
  print("Webclawer - Get Website Database")
  return Webclawer.get_website_database()

@eel.expose
def set_websitefilter(website,state):
  print("Webclawer - Set Filter :",website,state)
  return Webclawer.set_website_filter(website,state)

@eel.expose
def get_websitefilter(website):
  result = Webclawer.get_website_filter(website)
  print("Webclawer - Get Filter :",website,result)
  return result

@eel.expose
def website_printdata(website):
  print("Webclawer - Get Data :",website)
  result = Webclawer.get_website_page(website)
  eel.print_webdata(result)
  
@eel.expose
def add_website(name,website):
  print("Webclawer - Add website :",name,website)
  return Webclawer.addwebsite(name,website)

@eel.expose
def crawler_web():
  print("Webclawer !!!!!!")
  result = Webclawer.clawer_data()


if __name__ == "__main__":
  eel.init("web")
  eel.start("webscraping.html", block=False, size=(1600, 900))
  #eel.start("twitter.html", block=False, size=(1600, 900))

  print("Start")
  #Twitter = main_twitter.Twitter_API()
  #print(Twitter.get_twitter_trend())
  
  #eel.twittertrend_show(Twitter.get_twitter_trend())
  #eel.print_list2(Twitter.search_tweet("lisa"))
  
  while True:
    eel.sleep(1.0)