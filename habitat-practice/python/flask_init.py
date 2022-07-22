from mimetypes import init
from flask import Flask, request
from matplotlib.pyplot import title
# from cli import book_arr
import pandas as pd
import json 
from flask import Flask
from flask_cors import CORS
import requests
from models import Book
import re

from crud import Session
import mechanicalsoup

from config import API_KEY

from nltk_analysis import nltk_analysis
from machine_learning import machine_learning

s = Session()

app = Flask(__name__)
CORS(app)

full_list = []

initial_text_obj = {}
comp_texts_array = []

@app.route('/')
def hello():
    # print(f'book dict before post {book_arr}')
    count = 0
    multiplier = 100 * (count + 1)
    # books = s.query(Book).limit(multiplier).all()
    books = s.query(Book)
    book_arr = []
    book_dict = {}
        
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
    

@app.route('/scraper', methods = ['POST'])

def result():
    filters = request.get_json()

    global count
    global full_list
    count = 0
    # full_list = []
    browser = mechanicalsoup.StatefulBrowser()
   
    browser.open('https://quod.lib.umich.edu/cgi/t/text/text-idx?page=browse&cc=ecco&c=ecco')

    list_ready = False

    all_texts_by_alphabet = browser.page.select('tr', class_='browselistitem')
    letter_object = {}

    for index, text in enumerate(all_texts_by_alphabet):
        just_text = text.find('td')
        if just_text is None:
            list_ready = True
        else:
            if just_text.text is None:
                print('')
            else:
                if len(just_text.text.split("/")) < 2 and list_ready == True:
                    print("===============================================")                    

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
                        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                    else:
                        letter_object['title'] = link_text.text
                        if link_text is None:
                            print('############################')
                        else:
                            letter_object['title_url'] = link_text["href"]
                            full_list.append(letter_object.copy())
                            book = Book(title=letter_object['title'], author=letter_object['author'], published=letter_object['published'], title_url=letter_object['title_url'],price=1) 
                            r = s.query(Book).filter_by(title=letter_object['title']).first()
                            print("r: {r}")
                            if r is None:
                                s.add(book)
                                s.commit()
                            else:
                                print("proof it ids already there {book}")                
    texts_df = pd.DataFrame()
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
                    print("===============================================")   
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
                        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                    else:
                        letter_object['title'] = str(link_text.text)
                    if link_text is None:
                        print('############################')
                    else:
                        letter_object['title_url'] = link_text["href"] 
                        letter_object['id'] = count
                        letter_object['pages'] = 100
                        letter_object['price'] = 1
                        full_list.append(letter_object.copy())
                        book = Book(title=letter_object['title'], author=letter_object['author'], published=letter_object['published'], title_url=letter_object['title_url'],price=1) 
                        
                        r = s.query(Book).filter_by(title=letter_object['title']).first()
                        print("r: {r}")
                        if r is None:
                            s.add(book)
                            s.commit()
                        else:
                            print("already in db: {book}")
                        
                        # s.add(book)
                        # s.commit()
                        
    texts_df = pd.DataFrame()

    # browser.close()

    return request.get_json(force=True)

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
    year_to_filter_begin = datetime(int(request.get_json()['yearBegin']),1,1)
    year_to_filter_end = datetime(int(request.get_json()['yearEnd']),1,1)
    print(year_to_filter_begin)
    print(year_to_filter_end)
    query_res_year = s.query(Book).filter(Book.published.between(year_to_filter_begin,year_to_filter_end)).all()
    resp_year = []
    if query_res_year is not None:
        for i in query_res_year:
            bk_year = json.dumps(i.as_dict(), indent=4, sort_keys=True, default=str)
            resp_year.append(bk_year)
        return json.dumps(resp_year)
    else:
        return {}    

@app.route('/scraper_get_toc', methods = ['POST'])
def res_toc():  
    r = request.get_json()
    print(f"check it out: {r}")
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    all_toc = browser.page.find("div", id="toclist")
    all_toc_list = []
    obj = {}
    print("about to find every link in doc  -----------------------------------------")
    for each in all_toc:
        link_text = each.find("a")
        if type(link_text) is not int:
            link_full = link_text.text
            link_href = link_text["href"]
            all_toc_list.append({"link_text": link_full, "link_href": link_href})
    return json.dumps(all_toc_list)
     
@app.route('/scraper_get_text', methods=['POST'])
def res_text():
    r = request.get_json()
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(r['titleUrl'])
    h=browser.page.select('a', class_="buttonlink")
    # print(f'H IS {h}')
    print("about to loop all the A in H -----------------------------------------")
    for a in h:
        if a.text == "View entire text":
            ######### WE'LL NEED TO ADD / DUPLICATE CODE FOR FULL TEXT HERE
            return json.dumps(text_in_html)        
        else:
            print(f"In the else / scrape html ----------------------------------")
            text_in_html = browser.page.find('div',class_="maincontent").text
            print(f"begin the nltk analysis methods")
            old_df, sents = nltk_analysis(r, text_in_html)
            mach_learning = machine_learning(old_df,sents)
            print(f"WHAT OH WHAT IS MACH LEARNING??? {mach_learning}")
            initial_text_obj = old_df
            return old_df 

@app.route('/get_comparison_texts', methods=['POST'])
def res_n():

    ## -------------------------- THIS WILL BE MOVED FURTHER DOWN INTO A MACH LEARNING STEP (but staying here for now)
    initial_df_training_data = pd.DataFrame.from_dict(initial_text_obj, orient='index')
    initial_df_training_data = initial_df_training_data.transpose()
    print( "GOT DF OF INITIAL TEXT", text_df_test.info())
    # show first 5 rows
    print( "ytsss", text_df_test.head(5))
    # display some statistics
    print( "wooohooo", text_df_test.describe())
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
    print( "GOT DF OF INITIAL TEXT", text_df_test.info())
    # show first 5 rows
    print( "ytsss", text_df_test.head(5))
    # display some statistics
    print( "wooohooo", text_df_test.describe())
    ## -------------------------- 
    
    
    return {'keys':"hi"}