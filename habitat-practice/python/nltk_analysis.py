import nltk
import numpy as np
import requests
from nltk.corpus import inaugural
from nltk.tokenize import RegexpTokenizer,sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.text import Text
from ast import While
import asyncio
import sys, json
import datetime
import sys
from flask import Flask
from machine_learning import machine_learning
# from gevent import monkey
# monkey.patch_all()
# from gevent.pywsgi import WSGIServer
# from flask_sock import Sock


import time

# from flask_sock import Sock
# these two unused imports are referenced in collocations.doctest
# from nltk.metrics import (
#     BigramAssocMeasures,
#     ContingencyMeasures,
#     QuadgramAssocMeasures,
#     TrigramAssocMeasures,
# )
from nltk.metrics.spearman import ranks_from_scores, spearman_correlation
from nltk.probability import FreqDist
from nltk.util import ngrams
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import Nonterminal, nonterminals, Production, CFG

import pyphen
import pronouncing
import re
import itertools as _itertools
from datetime import date, datetime
from itertools import cycle
from config import API_KEY

import string

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

from machine_learning import machine_learning
nlp = en_core_web_sm.load()
from flask import Flask, request,Response

from crud import Session
s = Session()

from word_keylists import keyList,fullKeyList


########################################################################
########################################################################
################################ NLTK ##################################
########################################################################
########################################################################


# create handler for each connection

def nltk_analysis(r, text_in_html):
 
    if 'flask_init' in sys.modules:
        from flask_init import soct

        soct.send("third_msg") 
            

        ## Here come a bunch of NLTK imports
        ## TODO: DO MORE WITH PUNKT
        lemmatizer = WordNetLemmatizer()  
        stop_words = set(stopwords.words('english'))
        not_words = [">>","<<","[unnumbered]","unnumbered","page","Page","previous","Previous","Next","section","cite","bookbag","next","table","Table","contents","add","|","how","or","cite"]

        nltk.download('wordnet','names','stopwords','averaged_perceptron_tagger','vader_lexicon','punkt')

        tokenizer = RegexpTokenizer(r'\w+')
        #corpus = inaugural.raw('1789-Washington.txt')
        
        pyphen.language_fallback('nl_NL_variant1')
        'nl_NL' in pyphen.LANGUAGES
        dic = pyphen.Pyphen(lang='nl_NL')
            
        old_df= {key: None for key in keyList}
        global initial_text 
        initial_text = {key: None for key in fullKeyList}
        


        # #### fix this
        # s.query(r['titleUrl'])
        # query_by_url = s.query(Book).filter(Book.titleUrl.contains(r['titleUrl'])).all()
        # print(f"QUERY ")

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
        seen_poetic_forms = set()        
        old_df_poetic_form = []
        old_df_perc_drama = 0
        old_df_perc_poetry_syllables = 0
        old_df_perc_poetry_rhymes = 0
        old_df_spacy_tokens = []
        old_df_internal_rhyme_most_recent = []
        old_df_internal_rhyme_second_most_recent = []

        final_tokens = []
        
        word_frequencies = {}
        lines_per_sentence = []
        
        isPoeticLine = 0
        poetry_count = 0
        drama_count = 0
        summary = ''
        index = 0
        sentence_sentiment_compound = []
        sentence_sentiment_neg = []
        sentence_sentiment_pos = []
        sentence_sentiment_neu = []
        syllables_per_line = []
        last_line_internal = []
        last_line_internal_fodder = []
        lines_in_corpus = []
        lemmatized_words = []
        indexed_last_word_forms = {}

        # ------------------------------------------------------------
        # GET DATA / CLEAN WHOLE TEXT / TOKENIZED LIST OF ALL WORDS
        # ------------------------------------------------------------
        print("start getting data -----------------------------------------")
        corpus = text_in_html
        
        # print("\n" in corpus) 

        # initial clean of whole text
        corpus = corpus.replace("'d","ed")
        corpus = corpus.replace("'n","en")
        corpus = corpus.replace("ev'","eve")
        corpus = corpus.replace("t'r","ter")
        corpus = corpus.replace("f'r","fer")
        corpus = corpus.replace("Add to","")
        corpus = corpus.replace("How to", "")

        cleaned_corpus1= re.sub("[^a-zA-Z,;:.'\n]+", " ", corpus)
        pattern_corpus = r"\b(?=[MDCLXVIΙ])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?"
        corpus = re.sub(pattern_corpus, '', cleaned_corpus1)
        
        for m in not_words:
            try:
                corpus = corpus.replace(m,'')
            except:
                print(f"NO SIGN OF {m}")
        for r in not_words:
            if r in corpus:
                corpus = corpus.replace(r,'')
        corpus = corpus.replace(" f "," ")
        split_corpus = corpus.split("\n")
        almost_lines_in_corpus = []
        for c in split_corpus:
            almost_lines_in_corpus.append(c)
        all_lines = []
        for i in almost_lines_in_corpus:
            querywords = i.split()
            resultwords  = [word for word in querywords if word.lower() not in not_words]
            line = ' '.join(resultwords)
            if len(resultwords) > 3:
                all_lines.append(line)
        lines_in_corpus = all_lines

        for i in corpus:
            if "'d" in i:
                i.replace("'d","ed")
            if "'n" in i:
                i.replace("'n","en")
            if "ev'" in i:
                i.replace("ev'","eve")
            if "t'r" in i:
                i.replace("t'r","ter")
            if "f'r" in i:
                i.replace("f'r","fer")
            # if "'s" in i:
            #     i.replace("'s","") 
        # split_corpus = [word.strip(string.punctuation) for word in phrase.split(" ")]

        words = tokenizer.tokenize(corpus)
        
        words = [word.lower() for word in words]
        words_no_blanks = list(filter(None, words))

        # unique_tokens = list(words_no_blanks)
        # old_df_unique.append(unique_tokens)
        soct.send("explain_tokens_and_lemmas")
        #print("about to create final tokens -----------------------------------------")
        for each_word in words_no_blanks:
            if each_word not in stop_words:
                if each_word not in not_words:
                    final_tokens.append(each_word)
                    if len(each_word) > 0:
                        soct.send(each_word)

        final_tokens = [lemmatizer.lemmatize(word) for word in final_tokens]
        
        ## TODO: Add lang detect back in here -> 
        ## loop each word & apply results
        ## to the lines and sentences  

        # Create your bigrams
        # bgs = nltk.bigrams(final_tokens)

        # #compute frequency distribution for all the bigrams in the text
        # fdist = nltk.FreqDist(bgs)
        # for k,v in fdist.items():
        #     print(f"BIGRAM BIGRAM BIGRAM _____________________ k: {k} / v: {v}")
        
        #print("about to get coountable words -----------------------------------------")
        countable_words = []
        for e_w in final_tokens:
            z = e_w
            for letter in z:
                if letter.isalpha() is False:
                    z.replace(letter,'')
            countable_words.append(z)
        
        final_tokens_as_single_string = ' '.join(final_tokens)
        
        old_df['most_common_words'] = Counter(final_tokens).most_common(20)
        ##soct.send("explain_common_words")
       ## soct.send(Counter(final_tokens).most_common(20))

        # ------------------------------------------------------------
        # LINE LEVEL FOCUS -> INIT ANALYSIS OF POETRY / DRAMA FEATURES
        # ------------------------------------------------------------

        print("line level focus -----------------------------------------")
        ## Is it a drama?
        colons_in_text = final_tokens_as_single_string.count(":")
        old_df_perc_drama = (colons_in_text)/len(lines_in_corpus)
        
        clean_lines = []
        lines_in_corpus = list(filter(None, lines_in_corpus))
        # soct.send("explain_poetry_intro")
        for clean_l in lines_in_corpus:
            clean_l = re.sub("[^a-zA-Z.,;:'\n]+", " ", clean_l)
            pattern_li = r"\b(?=[MDCLXVIΙ])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?"
            clean_l = re.sub(pattern_li, '', clean_l)
            clean_lines.append(clean_l)
        lines_in_corpus = clean_lines
                    
        ### loop through every line in array of lines
        # ---------------------------------------------------------------------
        # Begin Poetic Analysis
        # ---------------------------------------------------------------------
        
        soct.send("fourth_msg")
  
        
        for idx, li in enumerate(lines_in_corpus):
            if idx + 1 == len(lines_in_corpus):
                print("UP 1")
                break
            if "'d" in li:
                li.replace("'d","ed")  
            if "'n" in li:
                li.replace("'n", "en")
            if "ev'" in li:
                li.replace("eve")
            if "t'r" in li:
                li.replace("ter")
            if "f'r" in li:
                li.replace("fer")
            if li is None or li == '':
                del li

            hyphenated = dic.inserted(li)
            hyphen_to_array = hyphenated.split('-')
            count = len(hyphen_to_array)
            # print(f"errr.... WHAT IS COUNT: {count}")
            old_df_syllables_per_line.append(count)
            tokens_in_line = tokenizer.tokenize(li)
            
            
            ### Loop through every word in line 
            ## find last word in each line
            ## make a bank of internal words for later rhyme analysis
            # print("loop each token in line -----------------------------------------")
            
            for w in tokens_in_line:
                if w == tokens_in_line[-1]:
                    # soct.send(f'{w}')
                    old_df_last_word_per_line.append(w)
                    # soct.send('explain_last_words_per_line')
                    # print(f"check old df last word per line: {old_df_last_word_per_line}")
                else: 
                    if len(w) > 3 and w.isalpha() is True:
                        last_line_internal_fodder.append(w)
            soct.send('explain_last_words_per_line')
            last_line_internal = last_line_internal_fodder
            count_form = 0
            ### poetry check 
            form_count_multiplier = 0
            # print("POETIC_FORM_3: ", len(old_df_last_word_per_line))
        for index, i in enumerate(old_df_last_word_per_line):  
            if index + 1 == len(old_df_last_word_per_line) or index + 1 == len(lines_in_corpus):
                print("BREAK!!!!!")
                break
            #print(f"HOW LONG IS LAST WORD PER LINE??? {len(old_df_last_word_per_line)}")

            #couplet check
            isPoetic = False
            appendage = {
                "index":count_form,
                "form":"heroic couplet", 
                "this_rhyme": old_df_last_word_per_line[index], 
                "last_rhyme":old_df_last_word_per_line[index - 1],
                "this_interrhyme":"",
                "last_interrhyme":"",
                "this_line": lines_in_corpus[index], 
                "last_line": lines_in_corpus[index-1],
                "this_interline":"",
                "last_interline":""
            }    
            #if index > 1:
            



            #check for quatrains
            if index > 3:
                if isPoetic is False and ( (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]) or (old_df_last_word_per_line[index - 2] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]))) ) or ( (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 3 ]) or (old_df_last_word_per_line[index - 3] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 3 ]))) ):
                    if (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]) or old_df_last_word_per_line[index - 2] in pronouncing.rhymes(old_df_last_word_per_line[index])):
                        if(index + 1 == len(old_df_last_word_per_line[index])):
                            break
                        print("PROBABLY AN ABAB INTERLOCKING QUATRAIN! ", index)
                        print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 2 ]}?")
                        
                        appendage = {"index":count_form, "form":"interlocking quatrain (ABAB)", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 2],"this_interrhyme": old_df_last_word_per_line[index - 1],"last_interrhyme":old_df_last_word_per_line[index - 1], "this_line": lines_in_corpus[index], "last_line": lines_in_corpus[index-2],"this_interline":lines_in_corpus[index-1],"last_interline":lines_in_corpus[index-3]}
                    if (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 3 ]) or old_df_last_word_per_line[index - 3] in pronouncing.rhymes(old_df_last_word_per_line[index])):
                        if(index + 1 == len(old_df_last_word_per_line[index])):
                            break
                        print("PROBABLY AN ABBA INTERLOCKING QUATRAIN! ", index)
                        print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 3 ]}?")
                        #soct.send(f"22222222222222____{old_df_last_word_per_line[index]}_{old_df_last_word_per_line[index - 3 ]}")
                        appendage = {"index":count_form, "form":"interlocking quatrain (ABAB)", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 2],"this_interrhyme": old_df_last_word_per_line[index - 1],"last_interrhyme":old_df_last_word_per_line[index - 1], "this_line": lines_in_corpus[index], "last_line": lines_in_corpus[index-2],"this_interline":lines_in_corpus[index-1],"last_interline":lines_in_corpus[index-3]}
                    if appendage['index'] not in [m['index'] for m in old_df_poetic_form]:
                        old_df_poetic_form.append(appendage)
                        isPoetic = True
                        if len(appendage) > 0:
                            soct.send(f"{appendage['this_rhyme']}_{appendage['last_rhyme']}")
                        form_count_multiplier = 4
                        if(index + 1 == len(old_df_last_word_per_line[index])):
                            break
                                              
                #check for tercets
                if isPoetic is False and index > 2 and (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1]) or (old_df_last_word_per_line[index-1] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 1]) )) and (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2]) or (old_df_last_word_per_line[index-2] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 2]) )):
                    if(index + 1 == len(old_df_last_word_per_line[index])):
                        break
            #  if isPoetic is False and index > 2 and old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]):
                    isPoetic = True
                    #if old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1 ]) or old_df_last_word_per_line[index -1] in pronouncing.rhymes(old_df_last_word_per_line[index]):
                    print("PROBABLY A TERCET! ", index)
                    print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 1 ]} and also with {old_df_last_word_per_line[index - 2 ]}?")
                    # soct.send(f"111111111111111111_{old_df_last_word_per_line[index]}_{old_df_last_word_per_line[index - 1 ]}_{old_df_last_word_per_line[index - 2 ]}")
                    appendage = {"index":count_form, "form":"tercet", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 2 ],"this_interrhyme": old_df_last_word_per_line[index - 1],"last_interrhyme":"", "this_line": lines_in_corpus[index], "last_line": lines_in_corpus[index-2],"this_interline":lines_in_corpus[index-1],"last_interline":"",
                    
                    }
                    if appendage["index"] not in [m['index'] for m in old_df_poetic_form]:
                        if len(appendage) > 0:
                            soct.send(f"{appendage['this_rhyme']}_{appendage['this_interrhyme']}_{appendage['last_rhyme']}")
                        old_df_poetic_form.append(appendage)
                        isPoetic = True
                        form_count_multiplier = 1
                    # else:
                    #     # print(f"WHAT in world IS APPENDAGE INDEX? {appendage['index']}")
                    #     print(f"WHAT IS OLD DF POETIC FORM length: {len(old_df_poetic_form)}")
                    # # isPoetic = True
                
                



            ## CHECK FOR COUPLETS
            if index > 1 and old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1]) or old_df_last_word_per_line[index-1] in pronouncing.rhymes(old_df_last_word_per_line[index]):
                                
                #print(f"here are those m values {[z['index'] for z in old_df_poetic_form]}")
                if appendage['index'] not in [m['index'] for m in old_df_poetic_form]:
                    print("PROBABLY A COUPLET! ", index)
                    print(f"couplet: does {old_df_last_word_per_line[index-1]} rhyme with {i}?")
                    if len(old_df_last_word_per_line) > 0:
                        soct.send(f"{old_df_last_word_per_line[index]}_{old_df_last_word_per_line[index - 1]}")
                    old_df_poetic_form.append(appendage)
                    isPoetic = True
                    form_count_multiplier = 2
                    
                else:
                    print(f"WHAT is APPENDAGE INDEX? {appendage['index']}")
                if index + 1 == len(old_df_last_word_per_line):
                    break
                # except:
                #     print('this line probably does not exist')
                # isPoetic = True
                    
            # #check for quatrains
            # if index > 3:
            #     if isPoetic is False and ( (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]) or (old_df_last_word_per_line[index - 2] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]))) ) or ( (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 3 ]) or (old_df_last_word_per_line[index - 3] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 3 ]))) ):
            #         if (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]) or old_df_last_word_per_line[index - 2] in pronouncing.rhymes(old_df_last_word_per_line[index])):
            #             if(index + 1 == len(old_df_last_word_per_line[index])):
            #                 break
            #             print("PROBABLY AN ABAB INTERLOCKING QUATRAIN! ", index)
            #             print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 2 ]}?")
                        
            #             appendage = {"index":count_form, "form":"interlocking quatrain (ABAB)", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 2],"this_interrhyme": old_df_last_word_per_line[index - 1],"last_interrhyme":old_df_last_word_per_line[index - 1], "this_line": lines_in_corpus[index], "last_line": lines_in_corpus[index-2],"this_interline":lines_in_corpus[index-1],"last_interline":lines_in_corpus[index-3]}
            #         if (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 3 ]) or old_df_last_word_per_line[index - 3] in pronouncing.rhymes(old_df_last_word_per_line[index])):
            #             if(index + 1 == len(old_df_last_word_per_line[index])):
            #                 break
            #             print("PROBABLY AN ABBA INTERLOCKING QUATRAIN! ", index)
            #             print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 3 ]}?")
            #             #soct.send(f"22222222222222____{old_df_last_word_per_line[index]}_{old_df_last_word_per_line[index - 3 ]}")
            #             appendage = {"index":count_form, "form":"interlocking quatrain (ABAB)", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 2],"this_interrhyme": old_df_last_word_per_line[index - 1],"last_interrhyme":old_df_last_word_per_line[index - 1], "this_line": lines_in_corpus[index], "last_line": lines_in_corpus[index-2],"this_interline":lines_in_corpus[index-1],"last_interline":lines_in_corpus[index-3]}
            #         if appendage['index'] not in [m['index'] for m in old_df_poetic_form]:
            #             old_df_poetic_form.append(appendage)
            #             isPoetic = True
            #             soct.send(f"{appendage['this_rhyme']}_{appendage['last_rhyme']}")
            #             form_count_multiplier = 4
                                              
            #     #check for tercets
            #     if isPoetic is False and index > 2 and (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1]) or (old_df_last_word_per_line[index-1] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 1]) )) and (old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2]) or (old_df_last_word_per_line[index-2] in pronouncing.rhymes(old_df_last_word_per_line[index]) and old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 2]) )):
            #         if(index + 1 == len(old_df_last_word_per_line[index])):
            #             break
            # #  if isPoetic is False and index > 2 and old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]):
            #         isPoetic = True
            #         #if old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1 ]) or old_df_last_word_per_line[index -1] in pronouncing.rhymes(old_df_last_word_per_line[index]):
            #         print("PROBABLY A TERCET! ", index)
            #         print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 1 ]} and also with {old_df_last_word_per_line[index - 2 ]}?")
            #         # soct.send(f"111111111111111111_{old_df_last_word_per_line[index]}_{old_df_last_word_per_line[index - 1 ]}_{old_df_last_word_per_line[index - 2 ]}")
            #         appendage = {"index":count_form, "form":"tercet", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 2 ],"this_interrhyme": old_df_last_word_per_line[index - 1],"last_interrhyme":"", "this_line": lines_in_corpus[index], "last_line": lines_in_corpus[index-2],"this_interline":lines_in_corpus[index-1],"last_interline":"",
                    
            #         }
            #         if appendage["index"] not in [m['index'] for m in old_df_poetic_form]:
            #             soct.send(f"{appendage['this_rhyme']}_{appendage['this_interrhyme']}_{appendage['last_rhyme']}")
            #             old_df_poetic_form.append(appendage)
            #             isPoetic = True
            #             form_count_multiplier = 1
            #         # else:
            #         #     # print(f"WHAT in world IS APPENDAGE INDEX? {appendage['index']}")
            #         #     print(f"WHAT IS OLD DF POETIC FORM length: {len(old_df_poetic_form)}")
            #         # # isPoetic = True
                
                



            #print("POETIC_FORM_2: ", len(old_df_poetic_form))
            old_df['poetic_form'] = old_df_poetic_form

            last_rhyme_to_check = pronouncing.rhymes(old_df_last_word_per_line[index - 1])

            for id, d in enumerate(last_line_internal):
                if id + 1 == len(last_line_internal):
                    print("UP")
                    break
                if d in last_rhyme_to_check and len(d) > 3:
                    old_df_internal_rhyme_most_recent.append({"index": index,"end_rhyme":old_df_last_word_per_line[index - 1],"internal_rhyme":d})
        
            #print(f"WHAT IS INTERNAL RHYME MOSTT RECENT inner?? {old_df_internal_rhyme_most_recent}")
            count_form = count_form + 1

    
            if isPoetic is True:
                count_form = count_form + 1
                poetry_count = poetry_count + form_count_multiplier
                # print(f"POET_COUNT {poetry_count}")
                isPoetic = False
            
                old_df_perc_poetry_rhymes = poetry_count/len(lines_in_corpus)
                # print(f"AHHHHHHHH {old_df_perc_poetry_rhymes}")

        # print(f"WHAT IS INTERNAL RHYME MOSTT RECENT outer?? {old_df_internal_rhyme_most_recent}")
        res = []
        for ix,i in enumerate(old_df_internal_rhyme_most_recent):
            if ix + 1 == len(old_df_internal_rhyme_most_recent):
                break
            if i not in res:    
                res.append(i)
            if i['internal_rhyme'] == i['end_rhyme']:
                old_df_internal_rhyme_most_recent.remove(i)
            if i['index'] == 0:
                # print('removing id=0 ', i)
                old_df_internal_rhyme_most_recent.remove(i)
                
        old_df['internal_rhyme_most_recent'] = res

    
        # print(f"DO WE HAVE SYLL PER LINE??? {syllables_per_line}")
        syllables_per_line = list(filter(None, syllables_per_line))

        print(f"POET_COUNT_1 {poetry_count}")
        # print(f"TEST WHAT IS SYL PER LINE {syllables_per_line}")
        # print(f"TEST OLD DF SYL PER LINE {old_df_syllables_per_line}")

        ## loop through every syllable in the line 
        for u in old_df_syllables_per_line:
            if u < 14 and u > 4:
                isPoeticLine = isPoeticLine + 1
                percentage_poetry_by_syllable = isPoeticLine / len(lines_in_corpus)
                print(f"PERC POETRY {percentage_poetry_by_syllable}")
                if percentage_poetry_by_syllable is not None:
                    soct.send(f"{percentage_poetry_by_syllable}")
                old_df_perc_poetry_syllables = percentage_poetry_by_syllable
        elements = np.asarray(old_df_syllables_per_line)
        mean = np.mean(elements, axis=0)    
        print(f"MEAN IS {mean}")
        
        # soct.send(f"{mean}")

        ### ------------------------------------------------------------
        ### Analysis of sentence-level stuff
        ### ------------------------------------------------------------
        
        sents = nltk.sent_tokenize(corpus)

        line_division = len(lines_in_corpus)/len(sents)
        lines_per_sentence.append(line_division)

        # print("The number of sentences is", len(sents))
        average_tokens = round(len(words_no_blanks)/len(sents))
        print("The average number of tokens per sentence is",average_tokens)
        old_df['avg_tokens_sentence'] = average_tokens

        idx_array = []
        # tokens = []
        sentence_words_grammar = []

        ### loop through the array of sentences 
        ### this is a huge loop -- !!!
        soct.send("eighth_msg")
        
        for idx,s in enumerate(sents):
            # soct.send("explain_grammar")
            # if "f" in s:
            #     print(f"DETECT F PROBLEM {s}")
            if "'d" in s:
                s.replace("'d","ed") 
            if "ev'" in s:
                s.replace("ev'","eve")
            if "'n" in s:
                s.replace("'n","en")
            if "t'r" in s:
                s.replace("t'r","ter")
            if "f'r" in s:
                s.replace("f'r","fer")
            s_tok = tokenizer.tokenize(s)
            
            ## loop through each token in this single sentence 
            # (this cleanup should be done by now...)
            for each in s_tok:
                if each is not None:
                    soct.send(each)
                if each.lower() in not_words or each.lower() in stop_words:
                    try:
                        s_tok.remove(each)
                    except:
                        print(f"problem removing s_tok (stopword): {s_tok}")
                if each.isalpha() is False:
                    try:
                        s_tok.remove(each)
                        # print(f"why are we here in alpha: {each}")
                    except:
                        print(f"problem removing s_tok (alpha): {s_tok}")
                if each.lower() == "page" or each.lower() == "previous" or each.lower() == "section" or each.lower() == "cite" or each.lower() == "bookbag" or each.lower == "next" or each == "<<" or each == ">>":
                    try:
                        s_tok.remove(each)
                    except:
                        print(f"problem removing s_tok (not_words): {s_tok}")
                
            s = " ".join(s_tok)

            words = s

            doc = nlp(s)
               
            for token in doc:
                #print(f'token text: {token.text} / token pos: {token.pos_} / token tag: {token.tag_}')
                word_index_in_sent = str(sents[idx]).find(token.text)
                sentence_words_grammar.append({'sentence_index':idx,'token_text':token.text,'token_pos':token.pos_,'token_tag':token.tag_,'index_in_sent':word_index_in_sent})
                if len(token) > 0 and token.pos_ == "VERB" or token.pos_ == "NOUN" or token.pos_ == "PROPN" or token.pos_ == "ADJ":
                    soct.send(f"{token.pos_}: {token.text}")

            ### lemmatize the words in each sentence
            # (this may not be necessary)
            if words and lemmatized_words == []:
                #prints the lemmatized words
                
                lemmatized_words_pos = [lemmatizer.lemmatize(s, pos = "v") for s in sents]
                tagged_lems = nltk.pos_tag(lemmatized_words_pos)
                ## print(f"TAGGED LEMS {tagged_lems}")
                string_lems = []
                # sentence_words_grammar = []
                # for idx, i in enumerate(tagged_lems):
                #     string_lems.append(i[0])
                # string_lems = ' '.join(string_lems)

                grammar = "NP: {<DT>?<JJ>*<NN>}"
                cp = nltk.RegexpParser(grammar)
                result = cp.parse(tagged_lems)
                
                

                ## add grammars to the object
                old_df_sentences_grammars.append({"sentence_level_grammar_result":result,"word_level_grammar_result":sentence_words_grammar})
                # print(f"LEMMA GRAMMAR LEN: {len(result)}")

                # print(f"tagged lems length: {len(tagged_lems)}")
                lemmatized_words.append(tagged_lems)


            ########################################################################
            ########################################################################
            ########################### ENTITY ANALYSIS ############################
            ########################################################################
            ########################################################################
            
            idx_array.append(idx)
                    
            ######## europeana data links  < = >  spacy
            api_key=API_KEY
            # cycle_ents = cycle(doc.ents)
            # last_X_text = ''
            # soct.send("explain_entity_analysis")
            soct.send("explain_entity_analysis")
            for i,X in enumerate(doc.ents):
                
                old_df_spacy_ents.append({idx:{X.text:X.label_}})
                # soct.send("explain_entity_analysis")
                if X.label_ == "LOC":
                    soct.send(f"LOCATION: {X.text}")
                    old_df_places.append(X.text)
                    print(f'DOCUMENT ENTITIES: {X.text}:{X.label_}')
                    
                if X.label_ == "PERSON":
                    soct.send(f"PERSON: {X.text}")
                    ## NO EUROPEANA API YET!!!!
                    # url = 'https://api.europeana.eu/entity/suggest' + api_key + '&type=agent&text=' + X.text + '"'
                    # # try:
                    # suggested_ents = requests.get(url, timeout=10.00)
                    # try:
                    #     print("ENTITY CHECK: ", json.loads(suggested_ents.text)['items'][0])
                    #     ## AGENTS
                    #     if(json.loads(suggested_ents.text)['items'] is not None):  
                    #         if json.loads(suggested_ents.text)['items'][0]['type'] == 'Agent':
                    #             print(f"DOB: {json.loads(suggested_ents.text)['items'][0].keys()}")
                    #             try:
                    #                 d1 = json.loads(suggested_ents.text)['items'][0]['dateOfBirth'] 
                    #                 if d1 is None:
                    #                     d1 = json.loads(suggested_ents.text)['items'][0]['dateOfEstablishment']
                    #                 if(d1):
                    #                     arr = d1.split('-')             
                    #                     # print(f'datetime test {datetime(int(arr[0]),int(arr[1]),int(arr[2]))}')
                    #                 try:
                    #                     if datetime(int(arr[0]),int(arr[1]),int(arr[2])) < datetime(1800,1,1):
                    #                         print(f"SUGGESTED ENTITIES::::::: {json.loads(suggested_ents.text)['items'][0]}")
                    #                         # soct.send(json.loads(suggested_ents.text)['items'][0])
                    #                         old_df_entities.append(json.loads(suggested_ents.text)['items'][0])
                    #                 except:
                    #                     print("can't retrieve agent")
                    #             except:
                    #                 print('no DOB')
                    #         else:
                    #             print(f"WHAT TYPE IS THIS???!@!! {json.loads(suggested_ents.text)['items'][0]['type']}")
                    # except:
                    #     print('no items')                                
                    

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

            #print(f'CLASSIFIER ACCURACY: {nltk.classify.accuracy(classifier, test_set)}')
            # for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
                # print('{0}: {1}'.format(key, value))
            
            old_df_sentences.append(s)

            sid = SentimentIntensityAnalyzer()
            # print(f"THE SENTENCE IS... {s}")
            # ss = sid.polarity_scores(s)
            ss = sid.polarity_scores(s)

                           
            for k in (sorted(ss)):
                # soct.send("explain_sentiment_analysis") 
                #print('{0}: {1}, '.format(k, ss[k]), end='')
                # soct.send("explain_entity_analysis")
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
            old_df["sentence_grammar"] = old_df_sentences_grammars[0] 
            old_df["last_word_per_line"] = old_df_last_word_per_line
            old_df["syllables_per_line"] = old_df_syllables_per_line
            old_df['poetic_form'] = old_df_poetic_form
            old_df['perc_poetry_syllables'] = old_df_perc_poetry_syllables
            old_df['perc_poetry_rhymes'] = old_df_perc_poetry_rhymes
            old_df['perc_drama'] = old_df_perc_drama
        # soct.send("explain_entity_analysis")    
        soct.send("eleventh_msg") 

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

                # print(f"SUMMARY! {summary}")
                regex = re.compile('[^a-zA-Z]')
                cleaned_summary1 = re.sub("[^a-zA-Z.']+", " ", summary)
                pattern = r"\b(?=[MDCLXVIΙ])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?"
                cleaned_summary = re.sub(pattern, '', cleaned_summary1)
                print(f"CLEANED SUMMARY ANY BETTER? {cleaned_summary}")
                
                old_df_summary.append(' '.join(summary_sentences))
                
        soct.send("explain_sentence_summary")
        old_df['summary'] = old_df_summary[0].replace("/n"," ")            
        old_df['spacy_entities'] = old_df_spacy_ents
        old_df["sentences"] = old_df_sentences
        old_df["entities"] = old_df_entities
        # old_df["unique_words"] = old_df_unique
        old_df['places'] = old_df_places
        old_df['orgs'] = old_df_orgs
        # old_df['spacy_tokens'] = old_df_spacy_tokens
        if len(old_df) > 0:
            soct.send(f"SUMMARY_{old_df['summary']}")
        # soct.send("explain_sentence_summary")
        # for k,v in old_df.items():
        #     print(f"wHAT TYPE IS THIS??? {k}: {type(v)}")

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
        
        # bigram_measures = nltk.collocations.BigramAssocMeasures() # measures

        # finder = BigramCollocationFinder.from_words(post_lem_token_string)
        # finder.apply_freq_filter(2) # filter on bigram min frequencies 
        
        # finder.apply_freq_filter(2)
        #bigram_measures = nltk.collocations.BigramAssocMeasures()
        # finder_new = finder.nbest(bigram_measures.pmi, 10)
        # old_df['common_bigrams'] = finder_new
        # print(f"BIGRAM FINDER {finder_new}")

        ### =================================================
        
        index = index + 1

        # print("WHAT ARE SENTS??? ", sents)
        machine_learning(old_df,sents,soct)
        return old_df,sents

# if __name__ == '__main__':
#     socketio.run(app)