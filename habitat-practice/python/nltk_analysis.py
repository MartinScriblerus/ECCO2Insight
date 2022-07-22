import nltk
import requests
from nltk.corpus import inaugural
from nltk.tokenize import RegexpTokenizer,sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
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

import pyphen
import pronouncing
import re
import itertools as _itertools
from datetime import date, datetime
from itertools import cycle
from config import API_KEY

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

from crud import Session
s = Session()

from word_keylists import keyList,fullKeyList

def nltk_analysis(r, text_in_html):
    
    stop_words = set(stopwords.words('english'))
    not_words = [">>","<<","[unnumbered]","unnumbered","page","Page","previous","Previous","Next","section","cite","bookbag","next","table","Table","contents","add","|","how","or","cite"]

    lemmatizer = WordNetLemmatizer()   
    nltk.download('wordnet','names','stopwords','averaged_perceptron_tagger','vader_lexicon','punkt')

    tokenizer = RegexpTokenizer(r'\w+')
    #corpus = inaugural.raw('1789-Washington.txt')
    
    pyphen.language_fallback('nl_NL_variant1')
    'nl_NL' in pyphen.LANGUAGES
    dic = pyphen.Pyphen(lang='nl_NL')
        
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
    last_line_internal = {"most_recent":[],"second_most_recent": []}
    last_line_internal_fodder = []
    lines_in_corpus = []
    lemmatized_words = []
    indexed_last_word_forms = {}

    # ------------------------------------------------------------
    # GET DATA / CLEAN WHOLE TEXT / TOKENIZED LIST OF ALL WORDS
    # ------------------------------------------------------------
    print("start getting data -----------------------------------------")
    corpus = text_in_html
    print("\n" in corpus) 

    # initial clean of whole text
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
    old_df_unique.append(unique_tokens)
    
    print("about to create final tokens -----------------------------------------")
    for each_word in words_no_blanks:
        if each_word not in stop_words:
            if each_word not in not_words:
                final_tokens.append(each_word)

    final_tokens = [lemmatizer.lemmatize(word) for word in final_tokens]

    print("about to get coountable words -----------------------------------------")
    countable_words = []
    for e_w in final_tokens:
        z = e_w
        for letter in z:
            if letter.isalpha() is False:
                z.replace(letter,'')
        countable_words.append(z)
    
    final_tokens_as_single_string = ' '.join(final_tokens)
    
    old_df['most_common_words'] = Counter(final_tokens).most_common(20)


    # ------------------------------------------------------------
    # LINE LEVEL FOCUS -> INIT ANALYSIS OF POETRY / DRAMA FEATURES
    # ------------------------------------------------------------

    print("line level focus -----------------------------------------")
    ## Is it a drama?
    colons_in_text = final_tokens_as_single_string.count(":")
    old_df_perc_drama = (colons_in_text)/len(lines_in_corpus)
    
    clean_lines = []
    lines_in_corpus = list(filter(None, lines_in_corpus))

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
    print("loop every line in array of lines -----------------------------------------")
    for idx, li in enumerate(lines_in_corpus):
        if li is None or li == '':
            del li
        print(f'what is idx? {idx}')
        print(f"old_poetic_form {old_df_poetic_form}")
        # if idx > 1:      
        #     old_df_poetic_form[idx] = {"index": idx} 
        hyphenated = dic.inserted(li)
        hyphen_to_array = hyphenated.split('-')
        count = len(hyphen_to_array)
        
        

        old_df_syllables_per_line.append(count)
        tokens_in_line = tokenizer.tokenize(li)

        ### Loop through every word in line 
        ## find last word in each line
        ## make a bank of internal words for later rhyme analysis
        print("loop each token in line -----------------------------------------")
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
                  
                    appendage = {"index":index,"form":"heroic couplet", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 1 ]}                    
                    if appendage['index'] not in [m['index'] for m in old_df_poetic_form]:
                        old_df_poetic_form.append(appendage)
                    isPoetic = True
                   
            #check for quatrains
            if isPoetic is False and index > 2 and old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]):
                
                if old_df_last_word_per_line[index] not in pronouncing.rhymes(old_df_last_word_per_line[index - 1 ]):
                    print("PROBABLY AN INTERLOCKING QUATRAIN! ", index)
                    print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 2 ]}?")
                
                    appendage = {"index":index, "form":"interlocking quatrain", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 2 ]}
                    if appendage['index'] not in [m['index'] for m in old_df_poetic_form]:
                        old_df_poetic_form.append(appendage)
                    isPoetic = True
                   
            #check for tercets
            if isPoetic is False and index > 2 and old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 2 ]):
                isPoetic = True
                if old_df_last_word_per_line[index] in pronouncing.rhymes(old_df_last_word_per_line[index - 1 ]):
                    print("PROBABLY A TERCET! ", index)
                    print(f"DOES {old_df_last_word_per_line[index]} rhyme with {old_df_last_word_per_line[index - 1 ]} and also with {old_df_last_word_per_line[index - 2 ]}?")
                    appendage = {"index":index, "form":"tercet", "this_rhyme": old_df_last_word_per_line[index], "last_rhyme":old_df_last_word_per_line[index - 1 ],"two_rhymes_ago":old_df_last_word_per_line[index - 2 ]}
                    if appendage['index'] not in [m['index'] for m in old_df_poetic_form]:
                        old_df_poetic_form.append(appendage)
                    isPoetic = True
                   

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
                except:
                    print(f"problem removing s_tok (stopword): {s_tok}")
            if each.isalpha() is False:
                try:
                    s_tok.remove(each)
                    print(f"why are we here in alpha: {each}")
                except:
                    print(f"problem removing s_tok (alpha): {s_tok}")
            if each.lower() == "page" or each.lower() == "previous" or each.lower() == "section" or each.lower() == "cite" or each.lower() == "bookbag" or each.lower == "next" or each == "<<" or each == ">>":
                try:
                    s_tok.remove(each)
                except:
                    print(f"problem removing s_tok (not_words): {s_tok}")
        s = " ".join(s_tok)

        words = s

        ### lemmatize the words in each sentence
        # (this may not be necessary)
        if words and lemmatized_words == []:
            #prints the lemmatized words

            lemmatized_words_pos = [lemmatizer.lemmatize(s, pos = "v") for s in sents]
            tagged_lems = nltk.pos_tag(lemmatized_words_pos)
            ## print(f"TAGGED LEMS {tagged_lems}")
            string_lems = []
            for i in tagged_lems:
                string_lems.append(i[0])
            string_lems = ' '.join(string_lems)

            grammar = "NP: {<DT>?<JJ>*<NN>}"
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(tagged_lems)
            
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
                # try:
                suggested_ents = requests.get(url, timeout=10.00)
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
        #print(f'CLASSIFIER ACCURACY: {nltk.classify.accuracy(classifier, test_set)}')
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
            
            # print(f"SUMMARY! {summary}")
            regex = re.compile('[^a-zA-Z]')
            cleaned_summary1 = re.sub("[^a-zA-Z.']+", " ", summary)
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
    return old_df,sents
