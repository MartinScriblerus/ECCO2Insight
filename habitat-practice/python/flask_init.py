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
import itertools as _itertools
from datetime import date, datetime
from itertools import cycle
from config import API_KEY




from nltk.collocations import *
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
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

s = Session()



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
            # text_loc = a["href"].split('?')[0] + '?rgn=main;view=fulltext'
            # browser.open(text_loc)
            # text_in_html = browser.page.find('div',class_="maincontent").text
            # print(f'Text in html: {text_in_html}')
            # # ## NLTK PROCESSING
            # # ## =================================
            
            # import nltk

            # # Sample corpus.
            # from nltk.corpus import inaugural
            # #corpus = inaugural.raw('1789-Washington.txt')
            # corpus = text_in_html
            # corpus_lc = [entry.lower() for entry in corpus]
   
            # from nltk.tokenize import RegexpTokenizer,sent_tokenize
            # from nltk import pos_tag

            # tokenizer = RegexpTokenizer(r'\w+')
            # sents = nltk.sent_tokenize(corpus)
            
            # print("The number of sentences is", len(sents))
            # words = tokenizer.tokenize(corpus)
            # words_no_blanks = list(filter(None, words))
            # print(f"words no blanks: {words_no_blanks}")
            # print("The number of tokens is", len(words))
            # average_tokens = round(len(words)/len(sents))
            # print("The average number of tokens per sentence is",average_tokens)
            # unique_tokens = set(words)
            # print("The number of unique tokens are", len(unique_tokens))
            # from nltk.corpus import stopwords
            # stop_words = set(stopwords.words('english'))
            # final_tokens = []
            # for each in words:
            #     if each not in stop_words:
            #         final_tokens.append(each)
            # print("The number of total tokens after removing stopwords are", len((final_tokens)))


            # from nltk.stem import PorterStemmer
            # from nltk.stem import SnowballStemmer 
            # # Snowball Stemmer has language as a parameter.
            # words = final_tokens
            # #Create instances of both stemmers, and stem the words using them.
            # stemmer_ps = PorterStemmer()  
            # #an instance of Porter Stemmer
            # stemmed_words_ps = [stemmer_ps.stem(word) for word in words]
            # print("Porter stemmed words: ", len(stemmed_words_ps))
            # stemmer_ss = SnowballStemmer("english")   
            # #an instance of Snowball Stemmer
            # stemmed_words_ss = [stemmer_ss.stem(word) for word in words]
            # print("Snowball stemmed words: ", len(stemmed_words_ss))

            # from nltk.stem import WordNetLemmatizer
            # nltk.download('wordnet')

            # words = final_tokens
            # lemmatizer = WordNetLemmatizer()   
            # #an instance of Word Net Lemmatizer
            # lemmatized_words = [lemmatizer.lemmatize(word) for word in words] 
            # print("The lemmatized words: ", lemmatized_words) 
            # #prints the lemmatized words
            # lemmatized_words_pos = [lemmatizer.lemmatize(word, pos = "v") for word in words]
            # print("The lemmatized words using a POS tag: ", lemmatized_words_pos) 
            # print(f"what is this {type(lemmatized_words_pos)}")
            # tagged_lems = nltk.pos_tag(list(lemmatized_words_pos))
            # print(f"HERE ARE TAGGED LEMS: {tagged_lems}")
            # #prints POS tagged lemmatized words
            
            # stem_sentence=[]
            # for s in sents:
            #     token_words=tokenizer.tokenize(s) #we need to tokenize the sentence or else stemming will return the entire sentence as is.
            #     for word in token_words:
            #         stem_sentence.append(stemmer_ps.stem(word))
            #         stem_sentence.append(" ") #adding a space so that we can join all the words at the end to form the sentence again.
            #     "".join(stem_sentence)
            #     lemma_sentence=[]
            #     for word in token_words:
            #         lemma_sentence.append(lemmatizer.lemmatize(word))
            #         lemma_sentence.append(" ")
            #     return "".join(lemma_sentence)
            # print(f"stemmed sentence: {stem_sentence.remove(' ')}")

            return json.dumps(text_in_html)
        
        
        else:
            text_in_html = browser.page.find('div',class_="maincontent").text
            # ## NLTK PROCESSING
            # ## =================================
            text_df = pd.DataFrame(columns=["title_url","unique_tokens","sentences","sentiment_per_sentence","avg_tokens_per_sentence","document_entities","suggested_entities","most_common_words", "tagged_lems","suggested_price","suggested_publisher"])
            if len(text_df) !=  0:
                text_df['indicator'] = text_df.apply(assign_indicator, axis=1)
            text_df['title_url'] = r['titleUrl']
            import nltk

            # Sample corpus.
            from nltk.corpus import inaugural
            #corpus = inaugural.raw('1789-Washington.txt')
            corpus = text_in_html
            corpus_lc = [entry.lower() for entry in corpus]
            
            ### Pre-Processing Text w NLTK
            ### =================================================
            from nltk.tokenize import RegexpTokenizer,sent_tokenize
            tokenizer = RegexpTokenizer(r'\w+')
            words = tokenizer.tokenize(corpus)
            words_no_blanks = list(filter(None, words))
            for item in words_no_blanks:
                if item.lower() == "page":
                    words_no_blanks.remove(item)
                if item.lower() == "[unnumbered]":
                    words_no_blanks.remove(item)
                if item.lower() == "previous":
                    words_no_blanks.remove(item)
                if item.lower() == "section":
                    words_no_blanks.remove(item)
                if item.lower() == "next":
                    words_no_blanks.remove(item)
                if item.lower() == "<<":
                    words_no_blanks.remove(item)
                if item.lower() == "bookbag":
                    words_no_blanks.remove(item)
                if item == "<<":
                    words_no_blanks.remove(item)
                if item == ">>":
                    words_no_blanks.remove(item)
                            # if item.isdigit and len(item) != 4:
                            #     tagged_lems.remove(item) 
                           # print(f"noo nums tagged lems: {no_nums_tagged_lems}")
                            # return no_nums_tagged_lems
            # print(f"words no blanks: {words_no_blanks}")
            print("The number of tokens is", len(words_no_blanks))

            unique_tokens = set(words_no_blanks)
            print("The number of unique tokens are", len(unique_tokens))
            text_df['unique_tokens'] = pd.Series([unique_tokens])
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            final_tokens = []
            for each in words_no_blanks:
                if each not in stop_words:
                    final_tokens.append(each)
            sents = nltk.sent_tokenize(corpus)
            print(f"SENTS===::: {sents}")
            text_df['sentences'] = pd.Series(sents)
            print("The number of sentences is", len(sents))
            average_tokens = round(len(words_no_blanks)/len(sents))
            print("The average number of tokens per sentence is",average_tokens)
            text_df["avg_tokens_per_sentence"] = int(average_tokens)

            from nltk.stem import WordNetLemmatizer
            nltk.download('wordnet','names','stopwords','averaged_perceptron_tagger','vader_lexicon','punkt')

            words = final_tokens
            lemmatizer = WordNetLemmatizer()   
            #an instance of Word Net Lemmatizer
            lemmatized_words = [lemmatizer.lemmatize(word) for word in words] 
            print("Lemmatized word length: ", len(lemmatized_words)) 
            #prints the lemmatized words
            lemmatized_words_pos = [lemmatizer.lemmatize(word, pos = "v") for word in words]
            print("Length of lemmatized words using a POS tag: ", len(lemmatized_words_pos)) 
            #prints POS tagged lemmatized words
            tagged_lems = nltk.pos_tag(lemmatized_words_pos)
            print(f"tagged lems length: {len(tagged_lems)}")

            lemma_sentence=[]
            for s in sents:
                token_words=tokenizer.tokenize(s) 

                for word in token_words:
                    lemma_sentence.append(lemmatizer.lemmatize(word))
                    lemma_sentence.append(" ")
                "".join(lemma_sentence)
            ### =================================================

            ### Sentiment Analysis w/ NLTK Naive Bayesian Classification
            ### =================================================
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
            for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
                print('{0}: {1}'.format(key, value))
            sentim_per_sent = []
            for sentence in sents:
                sid = SentimentIntensityAnalyzer()
                print(sentence)
                ss = sid.polarity_scores(sentence)
                if ss:
                    sentim_per_sent.append(ss)
                for k in sorted(ss):
                    print('{0}: {1}, '.format(k, ss[k]), end='')
                    
                text_df['sentiment_per_sentence'] = pd.Series(sentim_per_sent)
                print()
            ### =================================================

######### spacy entity recognition
            doc = nlp(corpus)
            for X in doc.ents:
                print(f'DOCUMENT ENTITIES: {X.text}:{X.label_}')
                # text_df["document_entities"].append({X.label_ :X.text}).copy()
            #print(f'NAMES AND LABELS: {[(X.text, X.label_) for X in doc.ents]}')
            
            for token in doc:
                print(f'token text: {token.text} / token pos: {token.pos_} / token tag: {token.tag_}')
                if token.pos_ == 'PUNCT':
                    del token                
               
                    #print(f'spacy analysis {token.text}, {token.lemma_}, {token.pos_}, {token.tag_}, {token.dep_}, {token.shape_}, {token.is_alpha}, {token.is_stop}')
    #### europeana data links
            # api_key='?wskey=orperesbula'
            api_key=API_KEY
            cycle_ents = cycle(doc.ents)
            last_X_text = ''

            for X in doc.ents:
                ##print(f"SPACY text {X.text} // SPACY label {X.label_}")


                europeana_suggestions = []
                europeana_sugg_object = {}
                
                if X.label_ != "CARDINAL" and X.label_ != "DATE":
                    # if X.label_ == "PERSON":
                    print("GETTING IN HERE")
                        # if next(cycle_ents).label_ == "PERSON":
                        #     if last_X_text == '':
                        #         last_X_text = X.text
                        #         print(f'last x text 1: {last_X_text}')
                        #     else:
                        #         last_X_text = last_X_text + ' ' + X.text
                        #         print(f'last x text 2: {last_X_text}')
                    url = 'https://api.europeana.eu/entity/suggest' + api_key + '&type=agent&text=' + X.text + '"'
                    suggested_ents = requests.get(url, timeout=10.00)
                # try:
                    # url = 'https://api.europeana.eu/entity/suggest' + api_key + '&text=' + X.text + '"'
                    # suggested_ents = requests.get(url, timeout=10.00)
                
                    ##print(f"europeana suggests: {json.loads(suggested_ents.text)['items']['id']}")
                    
                    
        
                    sugg_response = {}
                    try:
                        if(json.loads(suggested_ents.text)['items'] is not None):
                            text_df['items'] = pd.Series(json.loads(suggested_ents.text)['items'][0])
                            europeana_suggestion_ent = json.loads(suggested_ents.text)['items']
                        # print(f"europeana suggests ITEMS!!!: {europeana_suggestion_ent['items']['id']}")
                            #print(f"D - O - B: {json.loads(suggested_ents.text)['items']['dateOfBirth']}")
                           ## print(f'SUGG RESPONSE: {json.loads(suggested_ents.text)["items"]}')
                            # sugg_response['id'] = europeana_suggestion_ent['id']
                            # sugg_response['type'] = europeana_suggestion_ent['type']
                            # sugg_response['isShownBy'] = europeana_suggestion_ent['isShownBy']
                            # # sugg_response['dateOfBirth'] = europeana_suggestion_ent['items']
                            # sugg_response['prefLabel'] = europeana_suggestion_ent['prefLabel']
                           # print(f"SUGG RESPONSE FULL: {(json.loads(europeana_suggestion_ent))}")
                           # print(f"SUGG RESPONSE: {(json.loads(europeana_suggestion_ent)['items'])}")
                            print("WTF>!")
                            if json.loads(suggested_ents.text)['items'][0]['type'] == 'Agent':
                                
                                print(f"!!!! {type(json.loads(suggested_ents.text)['items'][0])}")
                                print(f"DOB: {json.loads(suggested_ents.text)['items'][0].keys()}")
                                try:
                                    d1 = json.loads(suggested_ents.text)['items'][0]['dateOfBirth'] 
                                  
                                    if d1 is None:
                                        d1 = json.loads(suggested_ents.text)['items'][0]['dateOfEstablishment']
                                    # d2 = datetime(1800,1,1)
                                    # print(f"typeof d1 {type(d1)} type d2 {type(d2)} d1 {d1} / d2 {d2}")
                                    # print(f"DOB COMPARISON: {d1 < d2}")
                                    print(f"AHHHHH TYPE DOB {type(d1)} // thing::::::: {d1}")
                                    if(d1):
                                        arr = d1.split('-')
                
                                        print(f"CHECH CHECK CHECHKH{arr}")
                                        print(f'datetime test {datetime(int(arr[0]),int(arr[1]),int(arr[2]))}')
                                    # print(f"TEST TESTTTTT {d1 < datetime(1800,1,1)}")
                                    # print(f"TTTEEESSSTTT 1: {int(d1)}")
                                    # print(f"TTTEEESSSTTT 2: {datetime(int(d1))}")
                                    try:
                                        if datetime(int(arr[0]),int(arr[1]),int(arr[2])) < datetime(1800,1,1):
                                            search_url = json.loads(suggested_ents.text)['items'][0]['id'] + api_key
                                            retrieve_agent = requests.get(search_url, timeout=5.0)
                                            print(f'hey an agent type: {type(retrieve_agent)}')
                                            print(f"RETRIEVE AGENT!!! {json.loads(retrieve_agent.text)}")
                                            text_df['entities'] = json.loads(retrieve_agent.text)
                                    except:
                                        print("can't retrive agent")
                                except:
                                    print('no DOB')
                                # try:
                                #     search_url = json.loads(suggested_ents.text)['items'][0]['id'] + api_key
                                #     retrieve_agent = requests.get(search_url, timeout=5.0)
                                #     print(f'hey an agent type: {type(retrieve_agent)}')
                                #     print(f"RETRIEVE AGENT!!! {json.loads(retrieve_agent.text)}")
                                #     text_df['entities'] = json.loads(retrieve_agent.text)
                                # except:
                                #     print("can't retrive agent")
                            # for u in json.loads(europeana_suggestion_ent)['items']:
                            #     print(f"HERE IS U: {u}")
                            # for v in json.loads(europeana_suggestion_ent)['items']:
                            #     print(f"HERE IS U: {v}")
                            # try:
                            #     # europeana_sugg_object['id'] = europeana_suggestion_ent['items']['id']
                            #     # europeana_sugg_object['type'] = europeana_suggestion_ent['items']['type']
                            #     # europeana_sugg_object['prefLabel'] = europeana_suggestion_ent['items']['prefLabel']['en']
                            #     # europeana_sugg_object['isShownBy'] = europeana_suggestion_ent['items']['isShownBy']
                                

                            #     if europeana_sugg_object['type'] == 'Agent':
                            #         ##merge_agent_ids = europeana_suggestion_ent['items']['id'] 
                            #         try:
                            #             print(f"SUGG OBJ ID: {europeana_sugg_object['id']} /// NEXT-> {next(cycle_ents)['id']}")
                            #             # search_url = json.loads(suggested_ents.text)['items']['id'] + api_key
                            #             # retrieve_agent = requests.get(search_url, timeout=2.50)
                            #             # print(f"RETRIEVE AGENT!!! {json.loads(retrieve_agent)}")
                            #         except:
                            #             print("error 527")
                            #         # search_person = 'https://api.europeana.eu/record/v2/search.json' + api_key + '&query=' + europeana_sugg_object['id'] + '"+OR+"' + X.text + '"'
                            #         # print(f'SEARCH WOOOOORKED ON PERSON: {search_person}')
                            #     # if europeana_sugg_object['type'] == 'Timespan':
                            #     #     print(f"HEYOOO {europeana_sugg_object['prefLabel']['en']}")
                            #     #     search_url =json.loads(suggested_ents.text)['items']['id'] + api_key
                            #     #     retrieve_timestamp = requests.get(search_url, timeout=2.50)
                            #     #     print(f"RETRIEVE TIMESPAN!!!! {json.loads(retrieve_timestamp)}")
                            #     #     # search_place = 'https://api.europeana.eu/record/v2/search.json' + api_key + '&query=' + europeana_sugg_object['id'] + '"'
                            #     #     # print(f'SEARCH WOOOOORKED ON PLACE: {search_place}')
                            #     if europeana_sugg_object['type'] == 'Place':
                            #         try:
                            #             print(f"PLAVEC OBJECT: {europeana_sugg_object}")
                            #             # search_url = json.loads(suggested_ents.text)['items']['id'] + api_key
                            #             # retrieve_place = requests.get(search_url, timeout=2.50)
                            #             # print(f"RETRIEVE PLACE!!! {json.loads(retrieve_place)}")
                            #         except:
                            #             print("eerror 543")
                            #         # search_place = 'https://api.europeana.eu/record/v2/search.json' + api_key + '&query=' + europeana_sugg_object['id'] + '"'
                            #         # print(f'SEARCH WOOOOORKED ON PLACE: {search_place}')
                            #     if europeana_sugg_object['type'] == 'Concept':
                            #         try:
                            #             print(f"EUREOOPEANA OBJ CONCEPT: {europeana_sugg_object}")
                            #             # search_url = json.loads(suggested_ents.text)['items']['id'] + api_key
                            #             # retrieve_concept = requests.get(search_url, timeout=2.50)
                            #             # print(f"RETRIEVE AGENT!!! {json.loads(retrieve_concept)}")
                            #         except:
                            #             print("error 549")
                            #         # search_concept = 'https://api.europeana.eu/record/v2/search.json' + api_key + '&query=' + europeana_sugg_object['id'] + '"'
                            #         # print(f'SEARCH WOOOOORKED ON CONCEPT: {search_concept}')
                            #         # try:
                            #         #     #text_df["suggested_entities"].append(europeana_sugg_object).copy()
                            #         #     # search_url = 'https://api.europeana.eu/record/v2/search.json' + api_key + '&query=' + europeana_sugg_object["id"] + '"'
                            #         #     # searched_ents = requests.get(search_url, timeout=2.50)
                            #         #     # print(f"europeana search: {searched_ents.text}")  
                    
                            #         # except:
                            #         #     print("error 562")
                            
                            # except:
                            #     print('error line 515')
                            
                            if json.loads(suggested_ents.text)['items'][0]['type'] == 'Place':
                                print(f"A PLACEE!@!! {json.loads(suggested_ents.text)['items'][0]}")
                            print('=======================================================')
                    except:
                        print('no items')                                
                    print("")
                # except:
                # else:
                    # if X.label_ == "CARDINAL":
                    #     print(f"caught a cardinal: {X.label_}")
                    # if X.label == "DATE":
                    #     print(f"caught a date: {X.label_}")
                
                # search_url = 'https://api.europeana.eu/record/v2/search.json' + api_key + '&query=' + X.text + '"'
                # searched_ents = requests.get(search_url, timeout=2.50)
                # print(f"europeana search: {searched_ents.text}")
    ####        
                 
            labels = [x.label_ for x in doc.ents]
            
            print(f"LABELS: {Counter(labels)}")
            items = [x.text for x in doc.ents]
            text_df["document_entities"] = pd.Series(items)
            print(f"MOST COMMON WORDS: {Counter(items).most_common(20)}")
            # for z in Counter(items).most_common(5):
            #     disp_plot = corpus.dispersion_plot(z)
            #     print(f"DISPERSION PLOT::::: {disp_plot}")
            # colloc = nltk.collocations(corpus)
            # print(f"COLLOCATIONS: {colloc}")
            # for c in Counter(items).most_common(3):
            #     # conc_list = corpus.concordance_list(c)
            #     print(f"CONC LIST::: {conc_list}")
            text_df["most_common_words"] = pd.Series(Counter(items).most_common(20))
            for x in doc.ents:
                if x.label_ == "PERSON":
                    print(f'FOUND A PERSON!! {x.text}')
                    url = 'https://api.europeana.eu/entity/suggest' + api_key + '&text=' + x.text + '"'
                    suggested_ents = requests.get(url, timeout=10.00)
                    try: 
                        d1 = json.loads(suggested_ents.text)['items'][0]['dateOfBirth'] 
                        
                        if d1 is None:
                            d1 = json.loads(suggested_ents.text)['items'][0]['dateOfEstablishment']
                        # d2 = datetime(1800,1,1)
                        # print(f"typeof d1 {type(d1)} type d2 {type(d2)} d1 {d1} / d2 {d2}")
                        # print(f"DOB COMPARISON: {d1 < d2}")
                        print(f"AHHHHH TYPE DOB {type(d1)} // thing::::::: {d1}")
                        if(d1):
                            arr = d1.split('-')
    
                            print(f"CHECH CHECK CHECHKH{arr}")
                            print(f'datetime test {datetime(int(arr[0]),int(arr[1]),int(arr[2]))}')
                            if datetime(int(arr[0]),int(arr[1]),int(arr[2])) < datetime(1800,1,1):
                                print(f"SSS UU GG EEE NNN TTT SSSS {json.loads(suggested_ents.text)['items'][0]}")
                    except:
                        print("no peopole too suggest")
           ## displacy.render(nlp(str(corpus[20])), style='ent')
#########
            

            print("The number of total tokens after removing stopwords are", len((final_tokens)))


            # from nltk.stem import PorterStemmer
            # from nltk.stem import SnowballStemmer 
            # # Snowball Stemmer has language as a parameter.
            # words = final_tokens
            # #Create instances of both stemmers, and stem the words using them.
            # stemmer_ps = PorterStemmer()  
            # #an instance of Porter Stemmer
            # stemmed_words_ps = [stemmer_ps.stem(word) for word in words]
            # print("Porter stemmed words: ", len(stemmed_words_ps))
            # stemmer_ss = SnowballStemmer("english")   
            # #an instance of Snowball Stemmer
            # stemmed_words_ss = [stemmer_ss.stem(word) for word in words]
            # print("Snowball stemmed words: ", len(stemmed_words_ss))


            # from nltk.corpus import wordnet as wn
            # for w in words_no_blanks:
            #     synsets = wn.synsets(w)
            #     print(f"DO SYNSETS WORK>?? {synsets}")
            # import matplotlib.pyplot as plt
            finder = BigramCollocationFinder.from_words(words_no_blanks)
            print(f"BIGRAM FINDER {finder.__dict__}")
            print(f"DID WEE GET DATAFRAME???: {text_df}")
      
            # words_no_blanks_cycle = cycle(words_no_blanks)
            # first_price = ''
            # second_price = ''
            # first_publisher = ''
            # second_publisher = ''
            # third_publisher = ''
            # is_pub = False
            # for i in words_no_blanks_cycle:
            #     get_another = False
            #     and_another = False
            #     if i == "price" and get_another == False:
            #         first_price = next(words_no_blanks_cycle)
            #         get_another = True
            #         print('hit price')
            #     if i == "printed":
            #         is_pub = True
            #         first_publisher = next(words_no_blanks_cycle)
            #         get_another = True
            #         print('hit printed')
            #     if i == "published":
            #         is_pub = True
            #         first_publisher = next(words_no_blanks_cycle)
            #         get_another = True
            #         print('hit published')
            #     if i == "sold":
            #         is_pub = True
            #         first_publisher = next(words_no_blanks_cycle)
            #         get_another = True
            #         print('hit sold')
            #     if get_another == True:
            #         print('hit get anoother')
            #         if is_pub == True:
            #             second_publisher = next(words_no_blanks_cycle)
            #             publisher = first_publisher + ' ' + second_publisher
            #             get_another = False
            #             and_another = True
            #             if get_another == False and and_another == True:
            #                 third_publisher = next(words_no_blanks_cycle)
            #                 publisher = second_publisher + ' ' + third_publisher
            #                 and_another = False
            #                 text_df["suggested_publisher"] = publisher
            #                 return json.dumps(text_df.to_json())
            #                 #return json.dumps({'lemma_sentence:':lemma_sentence, 'publisher':publisher})
            #         else:
            #             second_price = next(words_no_blanks_cycle)
            #             print(f"Next word... {second_price}")
            #             price = first_price + ' ' + second_price
            #             get_another = False
                        
            #             no_nums_tagged_lems = []

            #             text_df["tagged_lems"] = pd.Series(tagged_lems)
            #             text_df["suggested_price"] = str(price)
            #             print(f"DDAATTAAFFRRAAMMEE {text_df.head(10)}")
            #            # return json.dumps({'lemma_sentence:':lemma_sentence, 'tagged_lems': tagged_lems, 'price':price})
            #             return json.dumps(text_df.to_dict()) 
            # print(f'DID WE GET THE DATAFRAME? {text_df.to_dict()}')
            
            #return json.dumps({'lemma_sentence':lemma_sentence})
            return text_df.to_json() 