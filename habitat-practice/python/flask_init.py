from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from mimetypes import init
from flask import Flask, request
from matplotlib.pyplot import title
# from cli import book_arr
import pandas as pd
import json 
from flask import Flask,request,Response
from flask_cors import CORS
import requests
from models import Book
import re

from flask_sock import Sock
from crud import Session
import mechanicalsoup

from config import API_KEY
from datetime import date, datetime
from nltk_analysis import nltk_analysis
from machine_learning import machine_learning
# from ast import While
# import asyncio
import asyncio
from datetime import date,datetime

import os
import subprocess
import sys
import time

import sys, json
import datetime
# print(sys.path)

## SQL ALCHEMY SESSION VARIABLE  
## this global object allows for database queries from anywhere in code
## also see crud.py and models.py for SQL Alchemy setup
## -------------------------------------------------------------------
s = Session()

## FLASK APPLICATION wrapped in WEBSOCKET
## -------------------------------------------------------------------
app = Flask(__name__)
sock = Sock(app)
CORS(app, support_credentials=True)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
# create handler for each connection
## TODO: use gunicorn to thread -> make sure simultaneous users isn't an issue

## WEBSOCKETS ROUTE CONNECTED TO FLASK ENDPOINT
## -------------------------------------------------------------------
@sock.route('/ws')
def echo(ws):
    global soct
    soct = ws

    while True:
        data = ws.receive()

## TODO: ... is this left over from edit? check whether this can go!
## -------------------------------------------------------------------
def application(environ, start_response):
  if environ['REQUEST_METHOD'] == 'OPTIONS':
    start_response(
      '200 OK',
      [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
        ('Access-Control-Allow-Methods', 'POST'),
      ]
    )
    return ''

full_list = []
initial_text_obj = {}
comp_texts_array = []


@app.route('/')
def hello():

    count = 0
    multiplier = 100 * (count + 1)
    ## TODO: better strategy for minimizing load times...
    # books = s.query(Book).limit(multiplier).all()
    books = s.query(Book)
    book_arr = []
    book_dict = {}
    
    ## TODO: compare to models.py and crud.py when refining database
    ## TODO: add a legitimate book id    
    for count, u in enumerate(books):
        book_dict['id'] = u.__dict__['id']
        book_dict['title'] = u.__dict__['title']
        book_dict['title_url'] = u.__dict__['title_url']
        book_dict['author'] = u.__dict__['author']
        book_dict['published'] = u.__dict__['published'].isoformat()
        # book_dict['price'] = u.__dict__['price']
        book_dict['pages'] = u.__dict__['pages']  
        book_json = json.loads(json.dumps(book_dict))
    
        if book_json in book_arr:
            print('no dupes')
        else:
            book_arr.append(book_json) 
        
        count = count + 1 
    return json.dumps(book_arr, indent=4, separators=(',', ': '))
    
## This route scrapes metadata from all the texts in ECCO2. 
## It is gathering data that will be used for gathering full texts...
@app.route('/scraper', methods = ['POST'])
def scraper():
    filters = request.get_json()

    global count
    global full_list
    count = 0
    browser = mechanicalsoup.StatefulBrowser()
   
    ## navigate to ECCO with a stateful browser (works in the background)
    browser.open('https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=ecco&c=ecco')

    list_ready = False

    all_texts_by_alphabet = browser.page.select('tr', class_='browselistitem')
    ## TODO: rename letterObject. What is this?
    letter_object = {}

    ## Loop through all texts in ECCO2 ... navigate to each letter & collect data
    for index, text in enumerate(all_texts_by_alphabet):
        just_text = text.find('td')
        if just_text is None:
            list_ready = True
        else:
            if just_text.text is None:
                print('')
            else:
                if len(just_text.text.split("/")) < 2 and list_ready == True:
                  
                    next = browser.page.find_all("td", {"class": "browsenav_r1"})
                    for n in next:
                        if n.find("a") is None:
                            browser.close()
                        else:
                            subsequent_letter(n.find("a")["href"])
                elif len(just_text.text.split("/")) < 2:
                    print("catch => not important")
                else: 
                    parsed_year = str(just_text.text.split("/")[1])
                    regex_num_year = re.findall('[0-9]+', parsed_year)[:4]
                    letter_object['author'] = just_text.text.split("/")[0]
                    letter_object['id'] = count + 5
                    count = count + 1
                    letter_object['published'] = date(int(regex_num_year[0]), 6, 6)            

                    link_text = text.find('a', href=True)
                    if link_text is None:
                        print('Link text is none ^^')
                    else:
                        letter_object['title'] = link_text.text
                        if link_text is None:
                            print('Link text is none ##')
                        else:
                            letter_object['title_url'] = link_text["href"]
                            full_list.append(letter_object.copy())
                            book = Book(title=letter_object['title'], author=letter_object['author'], published=letter_object['published'], title_url=letter_object['title_url'],price=1) 
                            r = s.query(Book).filter_by(title=letter_object['title']).first()
                            # print("r: {r}")
                            if r is None:
                                s.add(book)
                                s.commit()
                            else:
                                print("proof it is already there {book}")                
    # texts_df = pd.DataFrame()
    return request.get_json(force=True)

def subsequent_letter(url): 
    browser = mechanicalsoup.StatefulBrowser()
    global full_list
    global count
    browser.open(url)
    list_ready = False
    letter_object = {}
    all_texts_by_alphabet = browser.page.select('tr', class_='browselistitem')
    count = 0
    for index, text in enumerate(all_texts_by_alphabet):
        just_text = text.find('td')
        if just_text is None:
            list_ready = True
        else:
            if just_text.text is None:
                print('')
            else:
                if len(just_text.text.split("/")) < 2 and list_ready == True:
                    print('')   
                    next_letter = browser.page.find("td", {"class": "browsenav_r1"}).find("a")["href"]
                elif len(just_text.text.split("/")) < 2:
                    print("catch => not important")
                else: 
                    parsed_year = str(just_text.text.split("/")[1])
                    regex_num_year = re.findall('[0-9]+', parsed_year)[0:4]
                    letter_object['id'] = count + 5
                    count = count + 1
                    letter_object['author'] = just_text.text.split("/")[0]
                    letter_object['published'] = date(int(str(regex_num_year[0])[:4]), 1, 1)

                    link_text = text.find('a', href=True)
                    if link_text is None:
                        print('link text is none !!')
                    else:
                        letter_object['title'] = str(link_text.text)
                    if link_text is None:
                        print('link text !!##')
                    else:
                        letter_object['title_url'] = link_text['href'] 
                        letter_object['id'] = count
                        letter_object['pages'] = 100
                        letter_object['price'] = 1
                        full_list.append(letter_object.copy())
                        ## get rid of price here?? fix the database Book class
                        book = Book(title=letter_object['title'], author=letter_object['author'], published=letter_object['published'], title_url=letter_object['title_url'],price=1) 
                        
                        r = s.query(Book).filter_by(title=letter_object['title']).first()
                        # print("r: {r}")
                        if r is None:
                            s.add(book)
                            s.commit()
                        else:
                            print("already in db: {book}")
                        
                        # s.add(book)
                        # s.commit()
                        
    # texts_df = pd.DataFrame()

    # browser.close()

    return request.get_json(force=True)


## A few search endpoints / methods here... 
## TODO: Add one more using mechanical soup to use ECCO2's search input form
## --------------------------------------------------------------------------
@app.route('/scraper_letter_filter', methods = ['POST'])
def res():
    letter_to_filter = request.get_json()['letter']
    letter_to_filter_mode = request.get_json()['filter_mode']
    if letter_to_filter_mode == True:
        query_res = s.query(Book).filter(Book.author.startswith(letter_to_filter)).all()
    else:
        query_res = s.query(Book).filter(Book.title.startswith(letter_to_filter)).all()

    resp = []
    for i in query_res:
        bk = json.dumps(i.as_dict(), indent=4, sort_keys=True, default=str)
        resp.append(bk)
    return json.dumps(resp)

# ## begin---------------------------------------------------
@app.route('/http://localhost:5000/fulltext_filter', methods = ['POST'])
def full_text_search():
    # fulltext_to_filter = request.get_json()
    # print(f"HIT PYTHON ROUTE!!! {fulltext_to_filter}")
    return json.dumps({"hi!":"helllllo"})

# @app.route('/http://localhost:5000/scraper_fullText', methods = ['POST'])
# def scrape_full_text():
#     filters = request.get_json()

#     global count_full_text
#     global full_list_full_text
#     count = 0
#     browser = mechanicalsoup.StatefulBrowser()
   
#     ## navigate to ECCO with a stateful browser (works in the background)
#     browser.open('https://quod.lib.umich.edu/cgi/t/text/text-idx?cc=ecco&page=simple&c=ecco')

#     list_ready_fulltext = False

#     search_inputs = browser.page.select('input', class_='formfont')
#     ## TODO: rename letterObject. What is this?
#     fulltext_search_object = {}

#     ## Loop through all texts in ECCO2 ... navigate to each letter & collect data
#     for index, inp in enumerate(search_inputs):
#         print(f"this should be an input: {inp}")

#         ## perhaps begin full text search here

# ## end-----------------------------------------------------



@app.route('/scraper_author_filter', methods = ['POST'])
def resp():
    author_to_filter = request.get_json()['author_filter']
    query_res = s.query(Book).filter(Book.author.contains(str(author_to_filter))).all()
    resp1 = []
    if query_res is not None:
        for i in query_res:
            if str(i.as_dict()["published"].strftime("%Y"))[0] == "0":
                i.as_dict()["published"] = str(i.as_dict()["published"].strftime("%Y"))[1:] + str(i.as_dict()["published"].strftime("%M"))[:1]
            bk = json.dumps(i.as_dict(), indent=4, sort_keys=True, default=str)
            resp1.append(bk)
        return json.dumps(resp1)
    else:
        return {}  

@app.route('/scraper_title_filter', methods = ['POST'])
def resp_title():
    title_to_filter = request.get_json()['title_filter']
    query_res_title = s.query(Book).filter(Book.title.contains(str(title_to_filter))).all()
    resp_title = []
    if query_res_title is not None:
        for i in query_res_title:
            bk_title = json.dumps(i.as_dict(), indent=4, sort_keys=True, default=str)
            resp_title.append(bk_title)
        return json.dumps(resp_title)
    else:
        return {}  

@app.route('/scraper_year_filter', methods = ['POST'])
def resp_2():
    if int(request.get_json()['yearBegin']) > 1699:
        if int(request.get_json()['yearEnd']) > 1699:
            year_to_filter_begin = date(int(request.get_json()['yearBegin']),1,1)
            year_to_filter_end = date(int(request.get_json()['yearEnd']),1,1)
            query_res_year = s.query(Book).filter(Book.published.between(year_to_filter_begin,year_to_filter_end)).all()
            resp_year = []
            if query_res_year is not None:
                for i in query_res_year:
                    bk_year = json.dumps(i.as_dict(), indent=4, sort_keys=True, default=str)
                    resp_year.append(bk_year)
                return json.dumps(resp_year)
        else:
            return {}    
    else:
        return {}    

@app.route('/scraper_get_toc', methods = ['POST'])
def res_toc():  
    r = request.get_json()
    print(f'what is R? {r}')
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    print(f"browser? {browser}")
    all_toc = browser.page.find("div", id="toclist")
    all_toc_list = []
    obj = {}
    print("about to find every link in doc  -----------------------------------------")
    # if type(all_toc) != None:
    print("HERE IS ALL TOC: ", all_toc)
    for each in all_toc:
        link_text = each.find("a")
        print("Linkt Text")
        if type(link_text) is not int:
            link_full = link_text.text
            link_href = link_text["href"]
            all_toc_list.append({"link_text": link_full, "link_href": link_href})
    return json.dumps(all_toc_list)
    # else:
    #     print('what is the issue here?') 

@app.route('/scraper_get_second_text', methods=['POST'])
def second_res_text():
    r = request.json()
    browser = mechanicalsoup.StatefulBrowser() 
    browser.open(r['titleUrl'])
    h=browser.page.select('a', class_='buttonlink')
    for a in h:
        if a.text == 'View entire text':
            #TODO: add this in for full text scrape (see note below)
            return json.dumps(text_in_html)
        else:
            #print(f"In the else / scrape html ----------------------------------")
            text_in_html = browser.page.find('div',class_="maincontent").text
            #print(f"begin the nltk analysis methods")
            # soct.send("second_msg")
            old_df, sents = nltk_analysis(r, text_in_html)
       
            # print(f"OLD DF IS {old_df} //// SENTS IS ... {sents}")
        
            mach_learning = machine_learning(old_df,sents)
            soct.send('fifteenth_msg')
            # print(f"WHAT OH WHAT IS MACH LEARNING??? {mach_learning}")
            # soct.send("fifteenth_msg")
            initial_text_obj = old_df
            # soct.send("second_msg")
            print("SECOND ONE WORKS!!!")
            return old_df 




    r = request.get_json()
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    h=browser.page.select('a', class_="buttonlink")
    # print(f'H IS {h}')
    #print("about to loop all the A in H -----------------------------------------")
    for a in h:
        if a.text == "View entire text":
            ######### TODO:
            ######### I'LL NEED TO ADD CODE FOR SEARCH TOC TO 
            ######### APPLY TO THE FULL TEXT CLICK HERE
            ######### I DOUBT THIS WILL EVEN WORK IN ITS CURRENT STATE HERE...
            ######### WE'LL ALSO WANT TO PASS WEBSOCKET FOR THIS ONE TOO...
            return json.dumps(text_in_html)        
        else:
            #print(f"In the else / scrape html ----------------------------------")
            text_in_html = browser.page.find('div',class_="maincontent").text
            #print(f"begin the nltk analysis methods")
            # soct.send("second_msg")
            old_df, sents = nltk_analysis(r, text_in_html)
       
            # print(f"OLD DF IS {old_df} //// SENTS IS ... {sents}")
        
            mach_learning = machine_learning(old_df,sents)
            soct.send('fifteenth_msg')
            # print(f"WHAT OH WHAT IS MACH LEARNING??? {mach_learning}")
            # soct.send("fifteenth_msg")
            initial_text_obj = old_df
            # soct.send("second_msg")
            return old_df 




@app.route('/scraper_get_text', methods=['POST'])
def res_text():
    r = request.get_json()
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    h=browser.page.select('a', class_="buttonlink")
    # print(f'H IS {h}')
    #print("about to loop all the A in H -----------------------------------------")
    for a in h:
        if a.text == "View entire text":
            ######### TODO:
            ######### I'LL NEED TO ADD CODE FOR SEARCH TOC TO 
            ######### APPLY TO THE FULL TEXT CLICK HERE
            ######### I DOUBT THIS WILL EVEN WORK IN ITS CURRENT STATE HERE...
            ######### WE'LL ALSO WANT TO PASS WEBSOCKET FOR THIS ONE TOO...
            return json.dumps(text_in_html)        
        else:
            #print(f"In the else / scrape html ----------------------------------")
            text_in_html = browser.page.find('div',class_="maincontent").text
            #print(f"begin the nltk analysis methods")
            # soct.send("second_msg")
            old_df, sents = nltk_analysis(r, text_in_html)
       
            # print(f"OLD DF IS {old_df} //// SENTS IS ... {sents}")
        
            mach_learning = machine_learning(old_df,sents)
            soct.send('fifteenth_msg')
            # print(f"WHAT OH WHAT IS MACH LEARNING??? {mach_learning}")
            # soct.send("fifteenth_msg")
            initial_text_obj = old_df
            # soct.send("second_msg")
            return old_df 

@app.route('/get_comparison_texts', methods=['POST'])
def res_n():

    ## -------------------------- THIS WILL BE MOVED FURTHER DOWN INTO A MACH LEARNING STEP (but staying here for now)
    initial_df_training_data = pd.DataFrame.from_dict(initial_text_obj, orient='index')
    initial_df_training_data = initial_df_training_data.transpose()
    # print( "GOT DF OF INITIAL TEXT", text_df_test.info())
    # # show first 5 rows
    # print( "ytsss", text_df_test.head(5))
    # # display some statistics
    # print( "wooohooo", text_df_test.describe())
    ## -------------------------- 

    r = request.get_json()
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    h=browser.page.select('a', class_="buttonlink")
    # print(f'H IS {h}')
    print("about to loop all the A in H -----------------------------------------")
    for a in h:
        if a.text == "View entire text":
            ######### WE'LL NEED TO ADD / DUPLICATE CODE FOR FULL TEXT HERE
            text_in_html = '' ## THIS IS A SAMPLE TO BLOCK WARNING UNTIL THIS IS READY
            return json.dumps(text_in_html)        

        else:
            print(f"In the else / scrape html ----------------------------------")
            text_in_html_comp = browser.page.find('div',class_="maincontent").text
            print(f"begin the nltk analysis methods for each new text")
            old_comp_df, sents = nltk_analysis(r, text_in_html_comp)
            mach_learning = machine_learning(old_comp_df,sents)
            print(f"WHAT OH WHAT IS MACH LEARNING FOR NEW TEXTS??? {mach_learning}")
            comp_texts_array.append(old_comp_df)
            return old_comp_df 
        print(f"HERE IS AN ARRAY OF COMP TEXTS... {comp_texts_array}")

@app.route('/testing', methods=['POST'])
def res_t():

    ## -------------------------- THIS WILL BE MOVED FURTHER DOWN INTO A MACH LEARNING STEP (but staying here for now)
    initial_df_training_data = pd.DataFrame.from_dict(initial_text_obj, orient='index')
    initial_df_training_data = initial_df_training_data.transpose()
    # print( "GOT DF OF INITIAL TEXT", text_df_test.info())
    # # show first 5 rows
    # print( "ytsss", text_df_test.head(5))
    # # display some statistics
    # print( "wooohooo", text_df_test.describe())
    ## -------------------------- 
    
    
    return {'keys':"hi"}




if __name__ == '__main__':
    WSGIServer(('127.0.0.1', 5000), app).serve_forever()


