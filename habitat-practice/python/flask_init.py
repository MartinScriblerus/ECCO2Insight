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
import math
import string
from crud import Session
import mechanicalsoup
import pyphen
import pronouncing
from langdetect import detect
import itertools as _itertools
from datetime import date, datetime
from itertools import cycle
from config import API_KEY

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, euclidean_distances, jaccard_score

from tsfresh.examples import load_robot_execution_failures
from tsfresh.transformers import RelevantFeatureAugmenter
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import extract_features
from tsfresh.feature_extraction import settings

from nltk.collocations import *
from nltk.text import Text
# these two unused imports are referenced in collocations.doctest
from nltk.metrics import (
    BigramAssocMeasures,
    ContingencyMeasures,
    QuadgramAssocMeasures,
    TrigramAssocMeasures,
)
from nltk.metrics.spearman import ranks_from_scores, spearman_correlation
from nltk.probability import FreqDist
from nltk.util import ngrams


from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk import Nonterminal, nonterminals, Production, CFG
import pickle
import subprocess
import sys

from google_trans_new import google_translator
from langdetect import detect_langs, DetectorFactory


import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

s = Session()

initial_text = {}

DetectorFactory.seed = 0

app = Flask(__name__)
CORS(app)

full_list = []

@app.route('/')
def hello():
    # print(f'book dict before post {book_arr}')
    count = 0
    multiplier = 100 * (count + 1)
    books = s.query(Book).limit(multiplier).all()
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
    for a in h:
        if a.text == "View entire text":
            print(f'Text in html: {text_in_html}')

            return json.dumps(text_in_html)
        
        ########################################################################
        ########################################################################
        ################################ NLTK ##################################
        ########################################################################
        ########################################################################

        else:
            # ------------------------------------------------------------
            # PREPARE IMPORTS AND VARIABLES
            # ------------------------------------------------------------

            import nltk

            # Sample corpus.
            from nltk.corpus import inaugural
            from nltk.tokenize import RegexpTokenizer,sent_tokenize
            from nltk.stem import WordNetLemmatizer
            from nltk.corpus import stopwords
            
            stop_words = set(stopwords.words('english'))
            not_words = [">>","<<","[unnumbered]","unnumbered","page","Page","previous","Previous","Next","section","cite","bookbag","next","table","Table","contents","add","|","how","or","cite"]

            lemmatizer = WordNetLemmatizer()   
            nltk.download('wordnet','names','stopwords','averaged_perceptron_tagger','vader_lexicon','punkt')

            tokenizer = RegexpTokenizer(r'\w+')
            #corpus = inaugural.raw('1789-Washington.txt')
            
            pyphen.language_fallback('nl_NL_variant1')
            'nl_NL' in pyphen.LANGUAGES
            dic = pyphen.Pyphen(lang='nl_NL')
            
            keyList =[
                "title_url",
                "entities",
                "spacy_entities",
                "sentence_id", 
                "lines_per_sentence", 
                "sentences",
                "sentence_sentiment_compound",
                "sentence_sentiment_neg",
                "sentence_sentiment_neu",
                "sentence_sentiment_pos",
                "spacy_tokens",
                "avg_tokens_sentence",
                "unique_words",
                "last_word_per_line",
                "common_bigrams",
                "most_common_words",
                "poetic_form",
                "perc_poetry_syllables",
                "perc_poetry_rhymes",
                "perc_drama",
                "places",
                "orgs",
                "summary",
                "lemmatized_words",
                "internal_rhyme_most_recent",
                "internal_rhyme_second_most_recent",
                ]
            fullKeyList =[
                "title_url",
                "entities",
                "spacy_entities",
                "sentence_id", 
                "lines_per_sentence", 
                "sentences",
                "sentence_sentiment_compound",
                "sentence_sentiment_neg",
                "sentence_sentiment_neu",
                "sentence_sentiment_pos",
                "spacy_tokens",
                "avg_tokens_sentence",
                "unique_words",
                "last_word_per_line",
                "common_bigrams",
                "most_common_words",
                "poetic_form",
                "perc_poetry_syllables",
                "perc_poetry_rhymes",
                "perc_drama",
                "places",
                "orgs",
                "summary",
                "lemmatized_words",
                "internal_rhyme_most_recent",
                "internal_rhyme_second_most_recent",
                "old_df_vectorized_features",
                "old_df_vectorized_vocab",
                "old_df_vectorized_tfidf",
                "old_df_euclidean_distance_since_last_self"
                ]

            old_df= {key: None for key in keyList}
            global initial_text 
            initial_text = {key: None for key in fullKeyList}
           
            old_df_entities = []
            old_df['title_url'] = r['titleUrl']
            old_df_sentences = []
            old_df_unique = []
            old_df_places = []
            old_df_orgs = []
            old_df_spacy_ents = []
            old_df_sentences_grammars = []
            old_df_syllables_per_line = []
            old_df_last_word_per_line = []           
            old_df_poetic_form = []
            old_df_perc_drama = 0
            old_df_perc_poetry_syllables = 0
            old_df_perc_poetry_rhymes = 0
            old_df_spacy_tokens = []
            old_df_internal_rhyme_most_recent = []
            old_df_internal_rhyme_second_most_recent = []
            old_df_vectorized_features = []
            old_df_vectorized_vocab = []
            old_df_vectorized_tfidf = []
            old_df_euclidean_distance_since_last_self = []

            final_tokens = []
            
            #banned_words = ["[unnumbered]","previous", "next", "section", "page", "how","cite","bookbag", "|","<<",">>", "add"]
            word_frequencies = {}
            lines_per_sentence = []
            
            isPoeticLine = 0
            poetry_count = 0
            drama_count = 0
            summary = ''
            index = 0
            # sentences = []

            sentence_sentiment_compound = []
            sentence_sentiment_neg = []
            sentence_sentiment_pos = []
            sentence_sentiment_neu = []
            syllables_per_line = []
            last_line_internal = {"most_recent":[],"second_most_recent": []}
            last_line_internal_fodder = []
            lines_in_corpus = []
            # lemmatizer = WordNetLemmatizer()   
            #an instance of Word Net Lemmatizer
            lemmatized_words = []
            from nltk.tree import Tree
            from sklearn.feature_extraction.text import CountVectorizer
            from sklearn.metrics.pairwise import euclidean_distances
            from sklearn.feature_extraction.text import TfidfVectorizer

            # ------------------------------------------------------------
            # GET DATA / CLEAN WHOLE TEXT / TOKENIZED LIST OF ALL WORDS
            # ------------------------------------------------------------
            
            text_in_html = browser.page.find('div',class_="maincontent").text
            corpus = text_in_html
            print("\n" in corpus) 
            # initial clean of whole text
            cleaned_corpus1= re.sub("[^a-zA-Z,;:.\n]+", " ", corpus)
            pattern_corpus = r"\b(?=[MDCLXVIΙ])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?"
            corpus = re.sub(pattern_corpus, '', cleaned_corpus1)
            # print("\n" in corpus) 
            
            
            for m in not_words:
                try:
                    corpus = corpus.replace(m,'')
                except:
                    print(f"NO SIGN OF {m}")
            for r in not_words:
                if r in corpus:
                    print("WHAT THE FUCK? ", r)
                    corpus = corpus.replace(r,'')
                    if r in corpus:
                        print("AGGGGGGGGG")
                else:
                    print("GOOOOOD!")
            if "Page" in corpus:
                    print("ERRRR???")
            else:
                print('ok cool')
            split_corpus = corpus.split("\n")
            almost_lines_in_corpus = []
            for c in split_corpus:
                almost_lines_in_corpus.append(c)
            all_lines = []
            for i in almost_lines_in_corpus:
                querywords = i.split()
                resultwords  = [word for word in querywords if word.lower() not in not_words]
                line = ' '.join(resultwords)
                all_lines.append(line)
            lines_in_corpus = all_lines
     
            words = tokenizer.tokenize(corpus)

            words = [word.lower() for word in words]
            words_no_blanks = list(filter(None, words))

            unique_tokens = list(words_no_blanks)
            print("The number of unique tokens is", len(unique_tokens))
            old_df_unique.append(unique_tokens)
            
            for each_word in words_no_blanks:
                if each_word not in stop_words:
                    if each_word not in not_words:
                        final_tokens.append(each_word)
 
            final_tokens = [lemmatizer.lemmatize(word) for word in final_tokens]

            countable_words = []
            for e_w in final_tokens:
                z = e_w
                for letter in z:
                    if letter.isalpha() is False:
                        z.replace(letter,'')
                countable_words.append(z)
            
            final_tokens_as_single_string = ' '.join(final_tokens)
          
            print(f"HERE IS THE CORPUS: {final_tokens_as_single_string}")

            old_df['most_common_words'] = Counter(final_tokens).most_common(20)


            # ------------------------------------------------------------
            # LINE LEVEL FOCUS -> INIT ANALYSIS OF POETRY / DRAMA FEATURES
            # ------------------------------------------------------------

            ## Is it a drama?
            colons_in_text = final_tokens_as_single_string.count(":")
            old_df_perc_drama = (colons_in_text)/len(lines_in_corpus)
            
            clean_lines = []
            lines_in_corpus = list(filter(None, lines_in_corpus))
     
            for clean_l in lines_in_corpus:
                clean_l = re.sub("[^a-zA-Z.,;:\n]+", " ", clean_l)
                pattern_li = r"\b(?=[MDCLXVIΙ])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?"
                clean_l = re.sub(pattern_li, '', clean_l)
                clean_lines.append(clean_l)
            lines_in_corpus = clean_lines
                        
            ### loop through every line in array of lines
            
            ### Time to Analyze Poetic Characteristics...
            ## begin by looping through every line in the array of lines
            for li in lines_in_corpus:
                if li is None or li == '':
                    del li
                
                hyphenated = dic.inserted(li)
                hyphen_to_array = hyphenated.split('-')
                count = len(hyphen_to_array)
                
         
                old_df_syllables_per_line.append(count)
                tokens_in_line = tokenizer.tokenize(li)

                ### Loop through every word in line 
                ## find last word in each line
                ## make a bank of internal words for later rhyme analysis
                for w in tokens_in_line:
                    if w == tokens_in_line[-1]:
                        old_df_last_word_per_line.append(w)
                        print(f"check old df last word per line: {old_df_last_word_per_line}")
                    else: 
                        if len(w) > 3 and w.isalpha() is True:
                            last_line_internal_fodder.append(w)
                last_line_internal['most_recent'] = last_line_internal_fodder
            
                ### poetry check 
                for index, i in enumerate(old_df_last_word_per_line):
                    
                    #couplet check
                    isPoetic = False
                    if index > 1:
                        if old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1]):
                            print("PROBABLY A COUPLET! ", index)
                            print(f"couplet test 1: {old_df_last_word_per_line[index-1]}")
                            print(f"couplet test 2: {i}")
                        
                            old_df_poetic_form.append({index-1:"heroic_couplet"})
                            isPoetic = True
                    
                    #check for quatrains
                    if index > 2 and old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]):
                        isPoetic = True
                        if old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 1 ]):
                            print("PROBABLY AN INTERLOCKING QUATRAIN! ", index)
                            print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 2 ]}?")
                            old_df_poetic_form.append("interlocking_quatrain")

                    #check for tercets
                    if index > 2 and old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]):
                        isPoetic = True
                        if old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1 ]):
                            print("PROBABLY A TERCET! ", index)
                            print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 1 ]} and {old_df_last_word_per_line[index - 2 ]}?")
                            old_df_poetic_form.append("tercet")

                    last_rhyme_to_check = pronouncing.rhymes(old_df_last_word_per_line[index - 1])
    
                    for d in last_line_internal['most_recent']:
                        if d in last_rhyme_to_check and len(d) > 3:
                            old_df_internal_rhyme_most_recent.append({"index": index,"end_rhyme":old_df_last_word_per_line[index - 1],"internal_rhyme":d})
    
                    if isPoetic is True:
                        poetry_count = poetry_count+1
                        isPoetic = False
                    old_df_perc_poetry_rhymes = poetry_count/len(lines_in_corpus)

                res = []
                for i in old_df_internal_rhyme_most_recent:
                    if i not in res:    
                        res.append(i)
                    if i['internal_rhyme'] == i['end_rhyme']:
                        old_df_internal_rhyme_most_recent.remove(i)
                    if i['index'] == 0:
                        print('removing id=0 ', i)
                        old_df_internal_rhyme_most_recent.remove(i)
                        
                old_df['internal_rhyme_most_recent'] = res

            syllables_per_line = list(filter(None, syllables_per_line))

            ## loop through every syllable in the line 
            for u in old_df_syllables_per_line:
                if u < 14 and u > 4:
                    isPoeticLine = isPoeticLine + 1
                    percentage_poetry_by_syllable = isPoeticLine / len(lines_in_corpus)
                    print(f"PERC POETRY {percentage_poetry_by_syllable}")
                    old_df_perc_poetry_syllables = percentage_poetry_by_syllable
            
   
            ### ------------------------------------------------------------
            ### Analysis of sentence-level stuff
            ### ------------------------------------------------------------
            
            sents = nltk.sent_tokenize(corpus)

            line_division = len(lines_in_corpus)/len(sents)
            lines_per_sentence.append(line_division)
  
            print("The number of sentences is", len(sents))
            average_tokens = round(len(words_no_blanks)/len(sents))
            print("The average number of tokens per sentence is",average_tokens)
            old_df['avg_tokens_sentence'] = average_tokens

            idx_array = []

            ### loop through the array of sentences 
            for idx,s in enumerate(sents):
   
                s_tok = tokenizer.tokenize(s)

                ## loop through each token in this single sentence 
                # (this cleanup should be done by now...)
                for each in s_tok:
                    if each.lower() in not_words or each.lower() in stop_words:
                        try:
                            s_tok.remove(each)
                            print(f"why are we here: {each}")
                        except:
                            print(f"s_tok: {s_tok}")
                    if each.isalpha() is False:
                        try:
                            s_tok.remove(each)
                            print(f"why are we here in alpha: {each}")
                        except:
                            print(f"s_tok: {s_tok}")
                    if each.lower() == "page" or each.lower() == "previous" or each.lower() == "section" or each.lower() == "cite" or each.lower() == "bookbag" or each.lower == "next" or each == "<<" or each == ">>":
                        try:
                            s_tok.remove(each)
                            print(f"why are we here in stopwords: {s_tok}")
                        except:
                            print(f"s_tok: {s_tok}")
                s = " ".join(s_tok)

                words = s

                ### lemmatize the words in each sentence
                # (this may not be necessary)
                if words and lemmatized_words == []:
                    #prints the lemmatized words

                    lemmatized_words_pos = [lemmatizer.lemmatize(s, pos = "v") for s in sents]

                    ## print("Length of lemmatized words using a POS tag: ", lemmatized_words_pos) 
                    #prints POS tagged lemmatized words
                    tagged_lems = nltk.pos_tag(lemmatized_words_pos)
                    ## print(f"TAGGED LEMS {tagged_lems}")
                    string_lems = []
                    for i in tagged_lems:
                        string_lems.append(i[0])
                    string_lems = ' '.join(string_lems)

                    grammar = "NP: {<DT>?<JJ>*<NN>}"
                    cp = nltk.RegexpParser(grammar)
                    result = cp.parse(tagged_lems)
                    print(f"NLTK PARSER: {result[0]}")
                    
                    ## add grammars to the object
                    old_df_sentences_grammars.append(result)
                    print(f"LEMMA GRAMMAR LEN: {len(result)}")

                    print(f"tagged lems length: {len(tagged_lems)}")
                    lemmatized_words.append(tagged_lems)
 
                ## WHY DO WE NEED TO ADD LEMMATIZED WORDS FROM SENTENCES (& not corpus) -- is this a sentence-level thing?
                old_df['lemmatized_words'] = lemmatized_words
                
       

                ########################################################################
                ########################################################################
                ########################### ENTITY ANALYSIS ############################
                ########################################################################
                ########################################################################

                # for idx, s in enumerate(sents):
                idx_array.append(idx)
                
                ######### spacy entity recognition
                doc = nlp(s)
                     
                # # ## CVOULD DO GRAMMAR STUFF ON DOC LEVEL HERE (IF WE DON'T USEE NLTK MDLE ABOVE)
                # tokens = []
                # for token in doc:
                #     print(f'token text: {token.text} / token pos: {token.pos_} / token tag: {token.tag_}')

                # #     if token.pos_ == 'PUNCT':
                # #         del token                
                # #         #print(f'spacy analysis {token.text}, {token.lemma_}, {token.pos_}, {token.tag_}, {token.dep_}, {token.shape_}, {token.is_alpha}, {token.is_stop}')
                #     tokens.append(token)
                # old_df_spacy_tokens.append({"sentence_idx":idx,"token_text": [i.text for i in tokens],"token_pos": [i.pos_ for i in tokens],"token_tag":[i.tag_ for i in tokens]})

                ######## europeana data links  < = >  spacy
                api_key=API_KEY
                # cycle_ents = cycle(doc.ents)
                # last_X_text = ''
             
                for X in doc.ents:
                    
                    old_df_spacy_ents.append({idx:{X.text:X.label_}})
                         
                    if X.label_ == "LOC":
                        old_df_places.append(X.text)
                        print(f'DOCUMENT ENTITIES: {X.text}:{X.label_}')
                        
                    if X.label_ == "PERSON":
                        url = 'https://api.europeana.eu/entity/suggest' + api_key + '&type=agent&text=' + X.text + '"'
                        suggested_ents = requests.get(url, timeout=10.00)
                        print(f"X.text: {X.text}")
        
                        try:
                            print("ENTITY CHECK: ", json.loads(suggested_ents.text)['items'][0])
                            ## AGENTS
                            if(json.loads(suggested_ents.text)['items'] is not None):  
                                if json.loads(suggested_ents.text)['items'][0]['type'] == 'Agent':
                                    print(f"DOB: {json.loads(suggested_ents.text)['items'][0].keys()}")
                                    try:
                                        d1 = json.loads(suggested_ents.text)['items'][0]['dateOfBirth'] 
                                        if d1 is None:
                                            d1 = json.loads(suggested_ents.text)['items'][0]['dateOfEstablishment']
                                        if(d1):
                                            arr = d1.split('-')             
                                            # print(f'datetime test {datetime(int(arr[0]),int(arr[1]),int(arr[2]))}')
                                        try:
                                            if datetime(int(arr[0]),int(arr[1]),int(arr[2])) < datetime(1800,1,1):
                                                print(f"SUGGESTED ENTITIES::::::: {json.loads(suggested_ents.text)['items'][0]}")
                                                old_df_entities.append(json.loads(suggested_ents.text)['items'][0])
                                        except:
                                            print("can't retrieve agent")
                                    except:
                                        print('no DOB')
                                else:
                                    print(f"WHAT TYPE IS THIS???!@!! {json.loads(suggested_ents.text)['items'][0]['type']}")
                        except:
                            print('no items')                                


                ########################################################################
                ########################################################################
                ######################### SENTIMENT ANALYSIS ###########################
                ########################################################################
                ########################################################################
                
                n_instances = 100
                subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
                obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
                # len(subj_docs), len(obj_docs)
                train_subj_docs = subj_docs[:80]
                test_subj_docs = subj_docs[80:100]
                train_obj_docs = obj_docs[:80]
                test_obj_docs = obj_docs[80:100]
                training_docs = train_subj_docs+train_obj_docs
                testing_docs = test_subj_docs+test_obj_docs
                sentim_analyzer = SentimentAnalyzer()
                all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
                unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
                len(unigram_feats)
                sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
                training_set = sentim_analyzer.apply_features(training_docs)
                test_set = sentim_analyzer.apply_features(testing_docs)
                trainer = NaiveBayesClassifier.train
                classifier = sentim_analyzer.train(trainer, training_set)
                print(f'CLASSIFIER ACCURACY: {nltk.classify.accuracy(classifier, test_set)}')
                # for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
                    # print('{0}: {1}'.format(key, value))
                
                old_df_sentences.append(s)
        
                sid = SentimentIntensityAnalyzer()
                print(f"THE SENTENCE IS... {s}")
                # ss = sid.polarity_scores(s)
                ss = sid.polarity_scores(s)
                                
                for k in (sorted(ss)):

                    print('{0}: {1}, '.format(k, ss[k]), end='')

                    if k == "compound":
                        sentence_sentiment_compound.append({"compound":ss[k]})
                    if k == "neg":
                        sentence_sentiment_neg.append({"neg":ss[k]})
                    if k == "neu":
                        sentence_sentiment_neu.append({"neu":ss[k]})
                    if k == "pos":
                        sentence_sentiment_pos.append({"pos":ss[k]})
                                

                old_df["sentence_id"] = idx_array
                old_df['lines_per_sentence'] = lines_per_sentence
                old_df["sentence_sentiment_compound"] = sentence_sentiment_compound
                old_df["sentence_sentiment_neg"] = sentence_sentiment_neg
                old_df["sentence_sentiment_neu"] = sentence_sentiment_neu
                old_df["sentence_sentiment_pos"] = sentence_sentiment_pos   
                old_df["sentence_grammar"] = old_df_sentences_grammars 
                old_df["last_word_per_line"] = old_df_last_word_per_line
                old_df["syllables_per_line"] = old_df_syllables_per_line
                old_df['poetic_form'] = old_df_poetic_form
                old_df['perc_poetry_syllables'] = old_df_perc_poetry_syllables
                old_df['perc_poetry_rhymes'] = old_df_perc_poetry_rhymes
                old_df['perc_drama'] = old_df_perc_drama
                old_df['vectorized_features'] = old_df_vectorized_features

                old_df['vectorized_vocab'] = old_df_vectorized_vocab
                old_df['vectorized_tfidf'] = old_df_vectorized_tfidf
                old_df['euclidean_distance_since_last_self'] = old_df_euclidean_distance_since_last_self
                
            print()
            
            

            ########################################################################
            ########################################################################
            ############################# Summarize ################################
            ########################################################################
            ########################################################################

            old_df_summary = []
            for index,word in enumerate(final_tokens):
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

                maximum_frequncy = max(word_frequencies.values())
             
                for word in word_frequencies.keys():
                    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

                if(index == len(final_tokens)-1):    
                    sentence_scores = {}
                    for sent in sents:
                        for word in nltk.word_tokenize(sent.lower()):
                            if word in word_frequencies.keys():
                                if len(sent.split(' ')) < 30:
                                    if sent not in sentence_scores.keys():
                                        sentence_scores[sent] = word_frequencies[word]
                                    else:
                                        sentence_scores[sent] += word_frequencies[word]
                    import heapq
                    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
                  
                    summary = ' '.join(summary_sentences)
                    # cleaned_summary = []
                    # for i in summary_sentences:
                    #     if i.isalpha() is True:
                    #         cleaned_summary.append(i)
                   
                    print(f"SUMMARY! {summary}")
                    regex = re.compile('[^a-zA-Z]')
                    cleaned_summary1 = re.sub("[^a-zA-Z.]+", " ", summary)
                    pattern = r"\b(?=[MDCLXVIΙ])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?"
                    cleaned_summary = re.sub(pattern, '', cleaned_summary1)
                    print(f"CLEANED SUMMARY ANY BETTER? {cleaned_summary}")
                    
                    old_df_summary.append(' '.join(summary_sentences))
                 
            old_df['summary'] = old_df_summary[0]            
            old_df['spacy_entities'] = old_df_spacy_ents
            old_df["sentences"] = old_df_sentences
            old_df["entities"] = old_df_entities
            old_df["unique_words"] = old_df_unique
            old_df['places'] = old_df_places
            old_df['orgs'] = old_df_orgs
            # old_df['spacy_tokens'] = old_df_spacy_tokens

            for k,v in old_df.items():
                print(f"wHAT TYPE IS THIS??? {k}: {type(v)}")

            pre_lemma_tokens = []
            post_lemma_tokens = []
            for y in final_tokens:
                x = [lemmatizer.lemmatize(y)] 
                post_lemma_tokens.append(x) 
            for z in post_lemma_tokens:
                if z != ".":
                    post_lem_token_string = ' '.join(z)
                else:
                    post_lem_token_string = ''.join(z)
            
            bigram_measures = nltk.collocations.BigramAssocMeasures() # measures
       
            finder = BigramCollocationFinder.from_words(post_lem_token_string)
            finder.apply_freq_filter(2) # filter on bigram min frequencies 
            
            # finder.apply_freq_filter(2)
            #bigram_measures = nltk.collocations.BigramAssocMeasures()
            finder_new = finder.nbest(bigram_measures.pmi, 10)
            old_df['common_bigrams'] = finder_new
            print(f"BIGRAM FINDER {finder_new}")

            ### =================================================
            
            index = index + 1

            print("The number of total tokens after removing stopwords are", len((final_tokens)))


            ########################################################################
            ########################################################################
            ######################### FEATURE ANALYSIS #############################
            ########################################################################
            ########################################################################


            from sklearn.feature_extraction.text import TfidfVectorizer
            
            text_df = pd.DataFrame.from_dict(old_df, orient='index')
            text_df = text_df.transpose()
            
            tfidf = TfidfVectorizer(stop_words="english")
            df_abstracts_tfidf = tfidf.fit_transform(text_df)    
            print("DF ABSTRACTS TFIDF SCIKIT", df_abstracts_tfidf)


            for idx, s in enumerate(sents):
                ### vectorize features in array of sentences
                vectorizer = CountVectorizer()
                features = vectorizer.fit_transform(sents).todense() 
                #features2 = vectorizer.fit_transform(list("This is test sentence")).todense()
                print(f"VECTORIZED VOCAB: {vectorizer.vocabulary_}")
                print(f"FEATURES!@ COUNT VECTORIZER {features}")
                old_df_vectorized_features.append(features)
                old_df_vectorized_vocab.append(vectorizer.vocabulary_)

                tfidf = TfidfVectorizer()
                y = tfidf.fit_transform([s])
                # y.toarray()
                tfidf.get_feature_names()
                df_feat = pd.DataFrame(y.toarray(), columns = tfidf.get_feature_names()).to_json()
                print(f"df feat TFIDF!!!! {type(df_feat)}")

                old_df_vectorized_tfidf.append(df_feat)

                ## WE'll want to bring this back!!!
                for i, f in enumerate(features):
                    print(f"EUCLIDEAN DIST: {euclidean_distances(f, features[i-1])}")
                    old_df_euclidean_distance_since_last_self.append(euclidean_distances(f,features[i-1]))
                



            df = pd.DataFrame({"id": [i for i in old_df['sentence_id']], "temperature": [f for f in old_df['sentence_sentiment_neg']], "pressure": [g for g in old_df['sentence_sentiment_pos']]})
            print(f"TUUUUST: {df}")
            settings_minimal = settings.MinimalFCParameters() 
            # print(f"MIN SEETT TUUST: {settings_minimal}")

            settings.ComprehensiveFCParameters, settings.EfficientFCParameters, settings.MinimalFCParameters
            print(f"DF COLS:::: ", df.columns)
            # X_tsfresh = extract_features(df, column_id='id', default_fc_parameters=settings_minimal)
            # X_tsfresh.head()
            # fc_parameters_pressure = {"length": None, 
            #                         "sum_values": None}

            # fc_parameters_temperature = {"maximum": None, 
            #                             "minimum": None}

            # kind_to_fc_parameters = {
            #     "temperature": fc_parameters_temperature,
            #     "pressure": fc_parameters_pressure
            # }

            # print(kind_to_fc_parameters)



            # display dataset structure with the pandas .info() method
            # print(text_df.info())

            # # show first 5 rows
            # print(text_df.head(5))

            # # display some statistics
            # print(text_df.describe())

            from sklearn.preprocessing import StandardScaler as SS # z-score standardization 
            from sklearn.cluster import KMeans, DBSCAN # clustering algorithms
            from sklearn.decomposition import PCA # dimensionality reduction
            from sklearn.metrics import silhouette_score # used as a metric to evaluate the cohesion in a cluster
            from sklearn.neighbors import NearestNeighbors # for selecting the optimal eps value when using DBSCAN
            import numpy as np

            # plotting libraries
            import matplotlib.pyplot as plt
            import seaborn as sns
            from yellowbrick.cluster import SilhouetteVisualizer
            def silhouettePlot(range_, data):
                '''
                we will use this function to plot a silhouette plot that helps us to evaluate the cohesion in clusters (k-means only)
                '''
                half_length = int(len(range_)/2)
                range_list = list(range_)
                fig, ax = plt.subplots(half_length, 2, figsize=(15,8))
                for _ in range_:
                    kmeans = KMeans(n_clusters=_, random_state=42)
                    q, mod = divmod(_ - range_list[0], 2)
                    sv = SilhouetteVisualizer(kmeans, colors="yellowbrick", ax=ax[q][mod])
                    ax[q][mod].set_title("Silhouette Plot with n={} Cluster".format(_))
                    sv.fit(data)
                fig.tight_layout()
                fig.show()
                fig.savefig("silhouette_plot.png")

            def elbowPlot(range_, data, figsize=(10,10)):
                '''
                the elbow plot function helps to figure out the right amount of clusters for a dataset
                '''
                inertia_list = []
                for n in range_:
                    kmeans = KMeans(n_clusters=n, random_state=42)
                    kmeans.fit(data)
                    inertia_list.append(kmeans.inertia_)
                    
                # plotting
                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(111)
                sns.lineplot(y=inertia_list, x=range_, ax=ax)
                ax.set_xlabel("Cluster")
                ax.set_ylabel("Inertia")
                ax.set_xticks(list(range_))
                fig.show()
                fig.savefig("elbow_plot.png")

            def findOptimalEps(n_neighbors, data):
                '''
                function to find optimal eps distance when using DBSCAN; based on this article: https://towardsdatascience.com/machine-learning-clustering-dbscan-determine-the-optimal-value-for-epsilon-eps-python-example-3100091cfbc
                '''
                neigh = NearestNeighbors(n_neighbors=n_neighbors)
                nbrs = neigh.fit(data)
                distances, indices = nbrs.kneighbors(data)
                distances = np.sort(distances, axis=0)
                distances = distances[:,1]
                plt.plot(distances)

            def progressiveFeatureSelection(df, n_clusters=3, max_features=4,):
                '''
                very basic implementation of an algorithm for feature selection (unsupervised clustering); inspired by this post: https://datascience.stackexchange.com/questions/67040/how-to-do-feature-selection-for-clustering-and-implement-it-in-python
                '''
                feature_list = list(df.columns)
                selected_features = list()
                # select starting feature
                initial_feature = ""
                high_score = 0
                for feature in feature_list:
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                    data_ = df[feature]
                    labels = kmeans.fit_predict(data_.to_frame())
                    score_ = silhouette_score(data_.to_frame(), labels)
                    print("Proposed new feature {} with score {}". format(feature, score_))
                    if score_ >= high_score:
                        initial_feature = feature
                        high_score = score_
                print("The initial feature is {} with a silhouette score of {}.".format(initial_feature, high_score))
                feature_list.remove(initial_feature)
                selected_features.append(initial_feature)
                for _ in range(max_features-1):
                    high_score = 0
                    selected_feature = ""
                    print("Starting selection {}...".format(_))
                    for feature in feature_list:
                        selection_ = selected_features.copy()
                        selection_.append(feature)
                        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                        data_ = df[selection_]
                        labels = kmeans.fit_predict(data_)
                        score_ = silhouette_score(data_, labels)
                        print("Proposed new feature {} with score {}". format(feature, score_))
                        if score_ > high_score:
                            selected_feature = feature
                            high_score = score_
                    selected_features.append(selected_feature)
                    feature_list.remove(selected_feature)
                    print("Selected new feature {} with score {}". format(selected_feature, high_score))
                return selected_features

            scaler = SS()
            for (columnName, columnData) in text_df.iteritems():
                if type(columnData) is list and type(columnData[0]) is float: 
                    print(f"AWESOME!!! {columnName}")
                    print(f"AWESOME BUT WTF IS THIS? {text_df['sentence_id'][0]}")
                    DNP_text_standardized = scaler.fit_transform(text_df['sentence_id'][0], text_df[columnName])
                    df_text_standardized = pd.DataFrame(DNP_text_standardized, index_col=columnName)
                    df_text_standardized = df_text_standardized.set_index(text_df.index)

                    print(df_text_standardized.info())

                    # show first 5 rows
                    print(df_text_standardized.head(5))

                    # display some statistics
                    print(df_text_standardized.describe())

                    selected_features = progressiveFeatureSelection(df_text_standardized, max_features=3, n_clusters=3)
                    optimal_features = optimal_features(df_text_standardized)
                    print("SELECTED FEATURES: ", selected_features)
                    df_standardized_sliced = df_text_standardized[selected_features]

                    print( df_standardized_sliced.info())

                    # show first 5 rows
                    print( df_standardized_sliced.head(5))

                    # display some statistics
                    print( df_standardized_sliced.describe())

                    elbowPlot(range(1,11), df_standardized_sliced)
                    silhouettePlot(range(3,9), df_standardized_sliced)
                    
                    
                    kmeans = KMeans(n_clusters=5, random_state=42)
                    cluster_labels = kmeans.fit_predict(df_standardized_sliced)
                    df_standardized_sliced["clusters"] = cluster_labels

                    # using PCA to reduce the dimensionality
                    pca = PCA(n_components=2, whiten=False, random_state=42)
                    authors_standardized_pca = pca.fit_transform(df_standardized_sliced)
                    df_authors_standardized_pca = pd.DataFrame(data=authors_standardized_pca, columns=["pc_1", "pc_2"])
                    df_authors_standardized_pca["clusters"] = cluster_labels

                    # plotting the clusters with seaborn
                    sns.scatterplot(x="pc_1", y="pc_2", hue="clusters", data=df_authors_standardized_pca)
            
            initial_text = old_df

            old_df.pop('vectorized_features',None)
            old_df.pop('vectorized_vocab',None)
            old_df.pop('vectorized_tfidf',None)
            old_df.pop('euclidean_distance_since_last_self', None)

            return old_df 

@app.route('/testing', methods=['POST'])
def res_t():
    print(f"initiialllll {initial_text}")
    text_df_test = pd.DataFrame.from_dict(initial_text, orient='index')
    text_df_test = text_df_test.transpose()
    print( "Yasaaa", text_df_test.info())

    # show first 5 rows
    print( "ytsss", text_df_test.head(5))

    # display some statistics
    print( "wooohooo", text_df_test.describe())
    return {'keys':"hi"}