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


            return json.dumps(text_in_html)
        
        ########################################################################
        ########################################################################
        ################################ NLTK ##################################
        ########################################################################
        ########################################################################

        else:
            text_in_html = browser.page.find('div',class_="maincontent").text
            # ## NLTK PROCESSING
            # ## =================================
            text_obj = {}
            keyList =["title_url","entities","spacy_entities","sentences","sentence_sentiment_compound","sentence_sentiment_neg","sentence_sentiment_neu","sentence_sentiment_pos","avg_tokens_sentence","unique_words","most_common_words","places","orgs","summary","lemmatized_words"]

            old_df= {key: None for key in keyList}
           
            old_df_entities = []
            old_df['title_url'] = r['titleUrl']
            old_df_sentences = []
            old_df_unique = []
 
            import nltk

            # Sample corpus.
            from nltk.corpus import inaugural
            from nltk.tokenize import RegexpTokenizer,sent_tokenize
            tokenizer = RegexpTokenizer(r'\w+')
            #corpus = inaugural.raw('1789-Washington.txt')
            corpus = text_in_html
            corpus_lc = [entry.lower() for entry in corpus]
                       
            words = tokenizer.tokenize(corpus)
            words_no_blanks = list(filter(None, words))
            sents = nltk.sent_tokenize(corpus)

            old_df_places = []
            old_df_orgs = []
            unique_tokens = list(words_no_blanks)
            print("The number of unique tokens is", len(unique_tokens))
            old_df_unique.append(unique_tokens)

            text_obj['unique_tokens'] = unique_tokens
            
            from nltk.corpus import stopwords
            
            stop_words = set(stopwords.words('english'))
            final_tokens = []
            banned_words = ["[unnumbered]","Previous", "Next", "section", "Page", "How","cite","bookbag", "|","<<",">>", "add"]
            for each in words_no_blanks:
                if each not in stop_words and each not in banned_words:
                        final_tokens.append(each)
                      
            print(f'CHECK FINAL TKS {"bookbag" in final_tokens}')   

            
            for se in sents:
                for each in se:
                    if each in banned_words or each in stop_words:
                        se.replace(each,'')
                print(f'CHECK IN SENTS {"Page" in se}')      
                not_this = "Previous"
                if not_this in se:
                    se.replace(not_this,'')
                not_this = "section"
                if not_this in se:
                    se.replace(not_this,'')
                not_this = "| How to cite"
                if not_this in se:
                    se.replace(not_this,'')
                not_this = "bookbag"
                if not_this in se:
                    se.replace(not_this,'')
                not_this = "next"
                if not_this in se:
                    se.replace(not_this,'')
                not_this = "<<"
                if not_this in se:
                    se.replace(not_this,'')
                not_this = ">>"
                if not_this in se:
                    se.replace(not_this,'')
                for wo in se:
                    if wo not in stop_words:
                        if wo != "[unnumbered]" and wo != "next" and wo != "section" and wo != "page" and wo.isalpha() and wo != "How" and wo != "cite" and wo != "bookbag":
                            se = ''.join(wo)
                print(f'Double CHECK IN SENTS {"Page" in se}') 
            
            print("The number of sentences is", len(sents))
            average_tokens = round(len(words_no_blanks)/len(sents))
            print("The average number of tokens per sentence is",average_tokens)
            old_df['avg_tokens_sentence'] = average_tokens
            text_obj["avg_tokens_per_sentence"] = average_tokens

            from nltk.stem import WordNetLemmatizer
            nltk.download('wordnet','names','stopwords','averaged_perceptron_tagger','vader_lexicon','punkt')

            words = final_tokens
            lemmatizer = WordNetLemmatizer()   
            #an instance of Word Net Lemmatizer
            lemmatized_words = []
            if words and lemmatized_words == []:
                #prints the lemmatized words
                lemmatized_words_pos = [lemmatizer.lemmatize(word, pos = "v") for word in words]
                print("Length of lemmatized words using a POS tag: ", len(lemmatized_words_pos)) 
                #prints POS tagged lemmatized words
                tagged_lems = nltk.pos_tag(lemmatized_words_pos)
                print(f"tagged lems length: {len(tagged_lems)}")
                lemmatized_words.append(tagged_lems)
            old_df['lemmatized_words'] = lemmatized_words





            word_frequencies = {}
         
            summary = ''
            index = 0
            sentences = []

       
            sentence_sentiment_compound = []
            sentence_sentiment_neg = []
            sentence_sentiment_pos = []
            sentence_sentiment_neu = []
            
            old_df_summary = []
            for index,word in enumerate(words_no_blanks):
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

                # print(f"WTF FREQQQQ {word_frequencies}")
                maximum_frequncy = max(word_frequencies.values())
             
                for word in word_frequencies.keys():
                    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

                if(index == len(words_no_blanks)-1):    
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
                    print(f"SUMMARY! {summary}")
                    
                    old_df_summary.append(' '.join(summary_sentences))
                 
            old_df['summary'] = old_df_summary[0]

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
                
                old_df_sentences.append(sents)
            
            # for sentence in sents:
                    
                sid = SentimentIntensityAnalyzer()
                print(s)
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
                old_df["sentence_sentiment_compound"] = sentence_sentiment_compound
                old_df["sentence_sentiment_neg"] = sentence_sentiment_neg
                old_df["sentence_sentiment_neu"] = sentence_sentiment_neu
                old_df["sentence_sentiment_pos"] = sentence_sentiment_pos
                print()
            old_df["sentences"] = old_df_sentences
            old_df["entities"] = old_df_entities
            old_df["unique_words"] = old_df_unique
            old_df['places'] = old_df_places
            old_df['orgs'] = old_df_orgs
            ### =================================================
            index = index + 1
######### spacy entity recognition
            doc = nlp(corpus)
            old_df_spacy_ents = []
            
            for X in doc.ents:
                old_df_spacy_ents.append( {X.text:X.label_})
                print(f'DOCUMENT ENTITIES: {X.text}:{X.label_}')
                print(f'CHURCK: {X}')
                # text_df["document_entities"].append({X.label_ :X.text}).copy()
            #print(f'NAMES AND LABELS: {[(X.text, X.label_) for X in doc.ents]}')
            
            for token in doc:
                print(f'token text: {token.text} / token pos: {token.pos_} / token tag: {token.tag_}')
                if token.pos_ == 'PUNCT':
                    del token                
               
                    #print(f'spacy analysis {token.text}, {token.lemma_}, {token.pos_}, {token.tag_}, {token.dep_}, {token.shape_}, {token.is_alpha}, {token.is_stop}')
    #### europeana data links
        
            old_df['spacy_entities'] = old_df_spacy_ents
            api_key=API_KEY
            cycle_ents = cycle(doc.ents)
            last_X_text = ''

            for X in doc.ents:
                items = [x.text for x in doc.ents]
                labels = [x.label_ for x in doc.ents]
                print(f"LABELS: {Counter(labels)}")

                print(f"MOST COMMON WORDS: {Counter(items).most_common(20)}")
                old_df['most_common_words'] = Counter(items).most_common(20)
                finder = BigramCollocationFinder.from_words(Counter(items).most_common(20))
                text_obj["common_bigrams"] = finder
                print(f"BIGRAM FINDER {finder.__dict__}")
                ##print(f"SPACY text {X.text} // SPACY label {X.label_}")

                if X.label_ == "LOC":
                    old_df_places.append(X.text)
                # if X.label_ == "ORG":
                #     old_df_orgs.append(X.text)
                if X.label_ == "PERSON":
                    print("GETTING IN HERE")
                    url = 'https://api.europeana.eu/entity/suggest' + api_key + '&type=agent&text=' + X.text + '"'
                    suggested_ents = requests.get(url, timeout=10.00)
                    
                    try:
                        ## AGENTS
                        if(json.loads(suggested_ents.text)['items'] is not None):
                            text_obj['items'] = json.loads(suggested_ents.text)['items'][0]

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
                            print('=======================================================')
                    except:
                        print('no items')                                
                    print("")

            # labels = [x.label_ for x in doc.ents]
            # items = [x.text for x in doc.ents]
            # print(f"LABELS: {Counter(labels)}")

            # print(f"MOST COMMON WORDS: {Counter(items).most_common(20)}")
            # old_df['most_common_words'] = Counter(items).most_common(20)

           # text_obj["most_common_words"] = Counter(items).most_common(20)


            print("The number of total tokens after removing stopwords are", len((final_tokens)))

            # old_df["sentences"] = old_df["sentences"].append(sents)
            # old_df["sentence_sentiment_compound"] = old_df["sentence_sentiment_compound"].append(sentence_sentiment_compound)
            # old_df["sentence_sentiment_neg"] = old_df["sentence_sentiment_neg"].append(sentence_sentiment_neg)
            # old_df["sentence_sentiment_neu"] = old_df["sentence_sentiment_neu"].append(sentence_sentiment_neu)
            # old_df["sentence_sentiment_pos"] = old_df["sentence_sentiment_pos"].append(sentence_sentiment_pos)

            # finder = BigramCollocationFinder.from_words(Counter(items).most_common(20))
            # text_obj["common_bigrams"] = finder
            # print(f"BIGRAM FINDER {finder.__dict__}")
            print(f"WHAT IS DF: {old_df}")
            
            return old_df 
        #     #return json.dumps({'lemma_sentence':lemma_sentence})
        #     old_df = [i.strip('[]') for i in old_df]
        #     print(f"AHHHH {type(old_df)}")
        #     return json.dumps(old_df,
        #   separators=(',', ':'), 
        #   sort_keys=True, 
        #   indent=4)