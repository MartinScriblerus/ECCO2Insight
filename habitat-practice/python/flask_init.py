from select import select
from tokenize import Number
from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from mimetypes import init
from flask import Flask,request,Response
from flask_cors import CORS
from flask_sock import Sock
from matplotlib.pyplot import title
# from cli import book_arr
import pandas as pd
import json 
from flask import jsonify
import requests
from models import Book
from sqlalchemy import delete
from sqlalchemy import func 
from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import union
from sqlalchemy.sql import text
import re


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
# print('what is sock??? ', sock)
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
    multiplier = 20 * (count + 1)
    ## TODO: better strategy for minimizing load times...
    # books = s.query(Book).limit(multiplier).all()
    
   # books = s.query(Book).filter(Book.author=="Shakespeare, William" and Book.author=="Pope, Alexander")
    
    ###########
    # shakespeare = s.query(Book).filter(Book.title == "Poems: vvritten by Wil. Shake-speare. Gent").first()
    # pope = s.query(Book).filter(Book.title == "The Dunciad: With notes variorum, and the prolegomena of Scriblerus. Written in the year, 1727.").first()
    books = s.query(Book).filter(
        or_(
            Book.title == "Poems: vvritten by Wil. Shake-speare. Gent",
            Book.title == "The Dunciad: With notes variorum, and the prolegomena of Scriblerus. Written in the year, 1727."
        )
    ).all()
    
    # and Book.title="The Dunciad: With notes variorum, and the prolegomena of Scriblerus. Written in the year, 1727."))
    ######
    # books = union(
    #     Book.select(where(Book.c.title == "Poems: vvritten by Wil. Shake-speare. Gent")),
    #     Book.select(where(Book.c.title == "The Dunciad: With notes variorum, and the prolegomena of Scriblerus. Written in the year, 1727."))
    #     .order_by(Book.c.title)
    # )
    #pope = s.query(Book).filter_by(author="Pope, Alexander")
    

    # austen = s.query(Book).filter_by(author="Austen, Jane").first()
    # behn = s.query(Book).filter_by(author="Behn, Aphra").first()
    # equiano = s.query(Book).filter_by(author="Equiano, Olaudah").first()
    # smart = s.query(Book).filter_by(author="Smart, Christopher").first()
    # leapor = s.query(Book).filter_by(author="Leapor, Mary").first()
    # marlowe = s.query(Book).filter_by(author="Marlowe, Christopher").first()
    # franklin s.query(Book).filter_by(author="Franklin, Ben").first()
    # swift = s.query(Book).filter_by(author="Swift, Jonathan").first()
    # sterne = s.query(Book).filter_by(author="Sterne, Laurence").first()
    # donne = s.query(Book).filter_by(author="Donne, John").first()
    # johnson = s.query(Book).filter_by(author="Johnson, Samuel").first()
    # bacon = s.query(Book).filter_by(author="Francis Bacon").first()
    # locke = s.query(Book).filter_by(author="Locke, John").first()
    # milton = s.query(Book).filter_by(author="Milton, John").first()
    # chatterton = s.query(Book).filter_by(author="Chatteron, Thomas").first()
    # paine = s.query(Book).filter_by(author="Leapor, Mary").first()
    # augustine = s.query(Book).filter_by(author="Augstine, Saint", title="Digitus dei or God appearing in his wonderfull works For the conuiction of nullifidians.").first()
    # radcliffe = s.query(Book).filter_by(author="Radcliffe, Ann").first()
    #paracelsus = s.query(Book).filter_by(author="Paracelsus").first()
    # wheatley = s.query(Book).filter_by(author="Wheatley, Phillis").first()
 
    

    # books = s.query(Book)
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
       
        book_json = json.loads(json.dumps(book_dict))

        if book_json in book_arr:
            print('no dupes')
        else:
            book_arr.append(book_json) 
        
        count = count + 1 
       
    return json.dumps(book_arr, indent=4, separators=(',', ': '))

current_url = ''  
all_letter_urls=[]  
started = False

######################
@app.route('/tryWikiImg', methods=['POST'])
def try_wiki_img():
    resp = request.get_json()
    url = resp['wikiString']
    first_name = resp['first_name']
    last_name = resp['last_name']
    title = resp['title']
    book_id = resp['book_id']
    publication_year = resp['published'] 
    browser = mechanicalsoup.StatefulBrowser()
    
    browser.open(url)
    # form_field = browser.page.find("form")
    # browser.select_form(form_field)
    # ##form_field.set_input({"searchInput": title + ' ' + first_name + ' ' + last_name + ' ' + publication_year})
    # browser['search'] = first_name + ' ' + last_name + ' ' + publication_year + ' ' + title
    # browser.submit_selected()
    
    # time.sleep(5)
    # browser.launch_browser()
    
    # new_links = browser.page.find_all('img')
    new_links = browser.page.select('td.infobox-image > a > img')

    testArr = []
    if n['src']:
            testArr.append(n['src'])            

    possible_img = ''

    # browser.open(url)

    # possible_img = browser.page.find_all('img')

    return json.dumps({'img_possible':testArr, 'book_id':book_id})
################################################

## This route scrapes metadata from all the texts in ECCO2. 
## It is gathering data that will be used for gathering full texts...
@app.route('/scraper', methods = ['POST'])
def scraper():
    filters = request.get_json()
    global count
    global full_list
    count = 0
    browser = mechanicalsoup.StatefulBrowser()
    
    book1 = Book(title="A worthy panegyrick upon monarchy; written anno MDCLVIII. / By a learned and truly loyal gentleman, for information of the miserably mis-led Commonwealths-Men (falsely so called) of that deluded age; and now revived by one that honours the author, and the established government of these nations.", 
        author="A learned and truly loyal gentleman", 
        id=1, 
        published=date(1680,6,6), 
        origin="eebo", 
        title_url="https://quod.lib.umich.edu/e/eebo/B06712.0001.001?view=toc" 
        )
    book2 = Book(title="An elegy on that illustrious and high-born Prince Rupert, who dyed on Wednesday November the 29th.", 
        author="A person of quality", 
        id=2, 
        published=date(1682,6,6), 
        origin="eebo", 
        title_url="https://quod.lib.umich.edu/e/eebo/B06712.0001.001?view=toc" 
        )
    
    if s.query(func.max(Book.id)).scalar_subquery() is None:
        s.add(book1)
        s.add(book2)
        s.commit()
        print('committed initial books')


    def get_EAI_basic_data(url):
        global full_list
        letter_eai = {}        
        if url is not None:
            browser.open(url)
        else:
            print("eai returning existing url: ",url)
            return
        cells = []
        cells1 = browser.page.select('tr.browselistitem')
        for c in cells1:
            cells.append(c)
        cells2 = browser.page.select('tr.browselistitem2')
        for c in cells2:
            cells.append(c)
        get_id=s.query(func.max(Book.id)).scalar_subquery()

        for f in cells:            
            if f.select('td.browsecell') is not None and len(f.select('td.browsecell')) > 0 and '/' in str(f.select('td.browsecell')[0].text):
                parsed_year = f.select('td.browsecell')[0].text.split('/')[1]

                if len(re.findall('[0-9]+', parsed_year)[:4]) > 0:
                    string_year = re.findall('[0-9]+', parsed_year)[:4][0]
                    pub_date = date(int(string_year), 6, 6) 
                    letter_eai['published'] = pub_date
                parsed_author = str(f.select('td.browsecell')[0].text.split('/')[0])
                parsed_author = list([val for val in parsed_author if val.isalpha() or val == ',' or val == ' '])

                parsed_author = ''.join(parsed_author).strip()
                while parsed_author[-1].isalpha() is False:
                    parsed_author = parsed_author[:-1]
                letter_eai['id'] = get_id + 1
                letter_eai['author'] = parsed_author
                letter_eai['origin'] = 'eai'
                letter_eai['title'] = f.select('td.browsecell')[1].text.replace("\n","")
                relevant_link = f.select('td.browsecell')[1].find('a') 
                letter_eai['title_url'] = relevant_link['href']

                if letter_eai not in full_list:

                    full_list.append(letter_eai.copy())
                    book = Book(title=letter_eai['title'], author=letter_eai['author'], id=letter_eai['id'], published=letter_eai['published'], origin=letter_eai['origin'], title_url=letter_eai['title_url']) 
                    r = s.query(Book).filter_by(title=letter_eai['title']).first()
                    
                    if r is None:
                        try:
                            s.add(book)
                            s.commit()
                        except Exception:
                            print('eai problem book: ', book)
                            continue
                        print(f"EAI added ------------------------ {book}")
                    else:
                        print(f"eai proof it is already there {book}") 
                    if book.author == 'Zenger, John Peter':
                        return
            
    def get_ECCO_basic_data(url):
        global full_list
        letter_ecco = {}

        if url is not None :
            browser.open(url)

        cells = []
        cells1 = browser.page.select('tr.browselistitem')
        for c in cells1:
            cells.append(c)
        cells2 = browser.page.select('tr.browselistitem2')
        for c in cells2:
            cells.append(c)
        
        for f in cells:
    
            if f.select('td.browsecell') is not None and len(f.select('td.browsecell')) > 0 and '/' in str(f.select('td.browsecell')[0].text):
                parsed_year = f.select('td.browsecell')[0].text.split('/')[1]

                if len(re.findall('[0-9]+', parsed_year)[:4]) > 0:
                    string_year = re.findall('[0-9]+', parsed_year)[:4][0]
                    pub_date = date(int(string_year), 6, 6) 
                    letter_ecco['published'] = pub_date
                parsed_author = str(f.select('td.browsecell')[0].text.split('/')[0])
                parsed_author = list([val for val in parsed_author if val.isalpha() or val == ',' or val == ' '])

                parsed_author = ''.join(parsed_author).strip()
                while parsed_author[-1].isalpha() is False:
                    parsed_author = parsed_author[:-1]
            
                letter_ecco['id'] = s.query(func.max(Book.id)).scalar_subquery() + 1
                letter_ecco['author'] = parsed_author
                letter_ecco['origin'] = 'ecco'
                letter_ecco['title'] = f.select('td.browsecell')[1].text.replace("\n","")
                relevant_link = f.select('td.browsecell')[1].find('a') 
                letter_ecco['title_url'] = relevant_link['href']
                if letter_ecco not in full_list:

                    full_list.append(letter_ecco.copy())

                    book = Book(title=letter_ecco['title'], author=letter_ecco['author'], id=letter_ecco['id'], published=letter_ecco['published'], origin=letter_ecco['origin'], title_url=letter_ecco['title_url']) 
                    r = s.query(Book).filter_by(title=letter_ecco['title']).first()
                   
                    if r is None:
                        s.add(book)
                        s.commit()
                        print(f"ecco added ----------------------- {book}")
                    else:
                        print(f"ecco proof it is already there {book}") 

                if parsed_author == 'Wright, Mrs.':
                    return
            
        
    def get_EEBO_basic_data(url):
        global full_list
        letter_eebo = {}

        if url is not None and browser is not None:
            try:
                browser.open(url)
                print("opened browser")
            except Exception:
                print("exception raised")
                raise
        else:
            return
        cells = []
        cells1 = browser.page.select('tr.browselistitem')
        for c in cells1:
            cells.append(c)
        cells2 = browser.page.select('tr.browselistitem2')
        for c in cells2:
            cells.append(c)

        for f in cells:
    
            if f.select('td.browsecell') is not None and len(f.select('td.browsecell')) > 0 and '/' in str(f.select('td.browsecell')[0].text):
                parsed_year = f.select('td.browsecell')[0].text.split('/')[1]

                if len(re.findall('[0-9]+', parsed_year)[:4]) > 0:
                    string_year = re.findall('[0-9]+', parsed_year)[:4][0]
                    
                    if len(string_year) > 4:
                        string_year = string_year[1:]
                    try:
                        pub_date = date(int(string_year), 6, 6) 
                        letter_eebo['published'] = pub_date
                    except:
                        letter_eebo['published'] = pub_date
                else:
                    letter_eebo['published'] = pub_date       
                parsed_author = str(f.select('td.browsecell')[0].text.split('/')[0])
                parsed_author = list([val for val in parsed_author if val.isalpha() or val == ',' or val == ' '])

                parsed_author = ''.join(parsed_author).strip()
                while parsed_author[-1].isalpha() is False:
                    parsed_author = parsed_author[:-1]
                current_count = s.query(func.max(Book.id)).scalar()
                letter_eebo['id'] = current_count + 1
                letter_eebo['author'] = parsed_author
                letter_eebo['origin'] = 'eebo'
                letter_eebo['title'] = f.select('td.browsecell')[1].text.replace("\n","")

                relevant_link = f.select('td.browsecell')[1].find('a') 
                letter_eebo['title_url'] = relevant_link['href']
                if letter_eebo not in full_list:
                    full_list.append(letter_eebo.copy())
                    book = Book(id=letter_eebo['id'],title=letter_eebo['title'], author=letter_eebo['author'], published=letter_eebo['published'], origin=letter_eebo['origin'], title_url=letter_eebo['title_url']) 
                    r = s.query(Book).filter_by(title=letter_eebo['title']).first()
                    
                    if r is None:
                        try:
                            s.add(book)
                            s.commit()
                            print(f"eebo added -----------------------------------: {book}")
                        except Exception:
                            print('problem book: ', book)
                            continue
                    else:
                        print(f"eebo proof it is already there {book}")             
        else:
            print('length of cells: ', len(cells))

    ## -------------------------------------------------------------------------------------- 
    ## navigate to Early English Book Online with a stateful browser (works in the background)
    if browser is not None:
        browser.open('https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=eebo&c=eebo')

        new_try_all_letters_eebo = browser.page.select('a.browsenav_r1')
        new_try_all_subletters_eebo = []
    
        for i in new_try_all_letters_eebo:
            browser.open(i['href'])
            if browser.page:
                new_try_subletters1 = browser.page.select('a.browsenav_r2')
                new_try_subletters2 = browser.page.select('a.browsenav_r2_selected')
                for k in new_try_subletters1: 
                    new_try_all_subletters_eebo.append(k['href'])
                for j in new_try_subletters2:
                    new_try_all_subletters_eebo.append(j['href'])
        for index, href in enumerate(new_try_all_subletters_eebo):
            if href is not None:    
                get_EEBO_basic_data(href)
            if href == "https://quod.lib.umich.edu/e/eebo/A15877.0001.001?view=toc":
                return
    else:
        return   
    
    
    ## -------------------------------------------------------------------------------------- 
    ## navigate to Early English Book Online 2 with a stateful browser (works in the background)
    if browser is not None:
        browser.open('https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=eebo2&c=eebo2')
        print('IN EEBO2 -----------------------------------------------------')
        new_try_all_letters_eebo2 = browser.page.select('a.browsenav_r1')
        new_try_all_subletters_eebo2 = []
    
        for i in new_try_all_letters_eebo2:
            browser.open(i['href'])
            if browser.page:
                new_try_subletters1 = browser.page.select('a.browsenav_r2')
                new_try_subletters2 = browser.page.select('a.browsenav_r2_selected')
                for k in new_try_subletters1: 
                    new_try_all_subletters_eebo2.append(k['href'])
                for j in new_try_subletters2:
                    new_try_all_subletters_eebo2.append(j['href'])

        for index, href in enumerate(new_try_all_subletters_eebo2):
            try:
                if href is not None:
                    get_EEBO_basic_data(href)
                    if href == 'https://quod.lib.umich.edu/e/eebo2/B08235.0001.001?view=toc':
                        return
                else:
                    print('no href? ', href)
            except Exception:
                print('why exception in eebo2?')
                continue    

   
    ## -------------------------------------------------------------------------------------- 
    # ## navigate to ECCO with a stateful browser (works in the background)
    if browser is not None:
        print('IN ECCO -----------------------------------------------------')
        browser.open('https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=ecco&c=ecco')
       
        new_try_subletters1 = browser.page.select('a.browsenav_r1')
        new_try_subletters2 = browser.page.select('a.browsenav_r1_selected')
        new_try_all_letters_ecco = []
        for k in new_try_subletters1: 
            new_try_all_letters_ecco.append(k['href'])
        for j in new_try_subletters2:
            new_try_all_letters_ecco.append(j['href'])

        for index, href in enumerate(new_try_all_letters_ecco):
            try:
                if href is not None:
                    get_ECCO_basic_data(href)
                if href == 'https://quod.lib.umich.edu/e/ecco/004823293.0001.000?view=toc':
                    return
            except Exception:
                continue    


    ## --------------------------------------------------------------------------------------       
    ## navigate to Early American Imprints with a stateful browser (works in the background)
    if browser is not None:
        print('IN EAI -----------------------------------------------------')
        browser.open('https://quod.lib.umich.edu/e/evans?cginame=text-idx;id=navbarbrowselink;key=author;page=browse;value=a')

        new_try_all_letters = browser.page.select('a.browsenav_r1')
        new_try_all_subletters = []
   
        for i in new_try_all_letters:
            browser.open(i['href'])
            if browser.page:
                new_try_subletters1 = browser.page.select('a.browsenav_r2')
                new_try_subletters2 = browser.page.select('a.browsenav_r2_selected')
                for k in new_try_subletters1: 
                    new_try_all_subletters.append(k['href'])
                for j in new_try_subletters2:
                    new_try_all_subletters.append(j['href'])

        for index, href in enumerate(new_try_all_subletters):
            # try:

            get_EAI_basic_data(href)
            if href == "https://quod.lib.umich.edu/e/evans/N03372.0001.001?view=toc":
                return
            # except Exception:
            #     continue
        
## ------ FINAL RETURN    
    # texts_df = pd.DataFrame()
    return request.get_json(force=True)
## ------ FINAL RETURN


@app.route('/scraper_fulltext_search_new', methods = ['POST'])
def f_t_search():
    fulltext_search_input = request.get_json()['fullTextSearchInput']
    print('WORKS!! ', fulltext_search_input)
    browser = mechanicalsoup.StatefulBrowser()
    
    urls = ['https://quod.lib.umich.edu/cgi/t/text/text-idx?page=simple;g=eebogroup']
    browser.open(urls[0])
    
    input_field = browser.page.find("form", id="search")
    browser.select_form(input_field)
    form = browser.get_current_form()

    browser['q1'] = "monkeys"
    # form.set_input({"q1": fulltext_search_input})
    # btn = browser.page.find('input')
    # for a in btn:
    #     if a.value == "Search":
    #         a.click()
    check = browser.submit_selected()

    browser.launch_browser()

    time.sleep(4)
    form_field = browser.page.find("form", id="sort")
    form_sel = browser.select_form(form_field)

    form_sel.set_select({'sort':'freq'})
    
    time.sleep(4)

    full_search_test = []
    full_search_titles = []
    available_titles = browser.page.find('div', class_="itemcitation")

    for i in available_titles:
        full_search_titles.append(i)

    evidence = {} 

    evidence['titles'] = check.text.replace("\n","")
    evidence['search_term'] = fulltext_search_input

    return json.dumps({'evidenceArr':evidence})

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
    return json.dumps({"hello":"filter_fulltext"})
#   ## perhaps begin full text search here by scraping w/ form control

# ## end-----------------------------------------------------

@app.route('/scraper_author_filter', methods = ['POST'])
def resp():
    author_to_filter = request.get_json()['author_filter']
    query_res = s.query(Book).filter(Book.author.contains(str(author_to_filter))).all()
    test = s.query(Book).filter(Book.origin.contains(str("eai"))).all()
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

    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    try:
        all_toc = browser.page.find("div", id="toclist")
        all_toc_list = []
        obj = {}
    except:
        browser.close()
    while all_toc is None:
        all_toc = browser.page.find("div", id="toclist")
        all_toc_list = []
        obj = {}
        if all_toc is not None:
            break
    for each in all_toc:
        link_text = each.find("a")
        if type(link_text) is not int:
            link_full = link_text.text
            link_href = link_text["href"]
            all_toc_list.append({"link_text": link_full, "link_href": link_href})
    browser.close()
    return json.dumps(all_toc_list)



@app.route('/scraper_get_text', methods=['POST'])
def res_text():
    r = request.get_json()
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    h=browser.page.select('a', class_="buttonlink")

    for a in h:
        if a.text == "View entire text":
            ######### TODO:
            ######### I'LL NEED TO ADD CODE FOR SEARCH TOC TO 
            ######### APPLY TO THE FULL TEXT CLICK HERE
            ######### I DOUBT THIS WILL EVEN WORK IN ITS CURRENT STATE HERE...
            ######### WE'LL ALSO WANT TO PASS WEBSOCKET FOR THIS ONE TOO...
            return json.dumps(text_in_html)        
        else:

            text_in_html = browser.page.find('div',class_="maincontent").text
            
            old_df, sents = nltk_analysis(r, text_in_html)
   
            mach_learning = machine_learning(old_df,sents)
            #could move this (& whole socket) to nltk file...
            soct.send('fifteenth_msg')
            # print(f"WHAT OH WHAT IS MACH LEARNING??? {mach_learning}")
            # soct.send("fifteenth_msg")
            initial_text_obj = old_df
            # soct.send("second_msg")
            return old_df 


@app.route('/testing', methods=['POST'])
def res_t():

    ## -------------------------- THIS WILL BE MOVED FURTHER DOWN INTO A MACH LEARNING STEP (but staying here for now)
    initial_df_training_data = pd.DataFrame.from_dict(initial_text_obj, orient='index')
    initial_df_training_data = initial_df_training_data.transpose()
    # print( "df of initial text", text_df_test.info())
    # # show first 5 rows
    # print( "show 5 rows", text_df_test.head(5))
    # # display some statistics
    # print( "display stats", text_df_test.describe())
    ## -------------------------- 
    
    
    return {'keys':"hi"}




if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',use_reloader=True,debug=True)
    WSGIServer(('127.0.0.1', 5000), app).serve_forever()


