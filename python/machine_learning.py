########################################################################
########################################################################
######################### FEATURE ANALYSIS #############################
########################################################################
########################################################################
import numpy as np
from nltk.tree import Tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, euclidean_distances, jaccard_score
from nltk import cluster
from nltk.cluster import euclidean_distance
from numpy import array

import pandas as pd
import sys

machine_dict = {}
chosenTexts = [{},{}]

def machine_learning(old_df,sents,soct): 

    if len(chosenTexts[0])< 1:
        # chosenTexts[0] = {}
        chosenTexts[0]['df'] = old_df
        chosenTexts[0]['sents'] = sents
    else:
        # chosenTexts[1] = {}
        chosenTexts[1]['df'] = old_df
        chosenTexts[1]['sents'] = sents

    # if 'flask_init' in sys.modules:
    #     from flask_init import soct
    # soct.send("eleventh_msg")
    global placeholderObject
    placeholderObject = {}

    for index, t in enumerate(chosenTexts): 
        placeholderObject[index] = {}
        placeholderObject[index]['old_df_vectorized_features'] = []
        placeholderObject[index]['old_df_vectorized_vocab'] = []
        placeholderObject[index]['old_df_vectorized_tfidf'] = []
        placeholderObject[index]['old_df_euclidean_distance_since_last_self'] = []
        placeholderObject[index]['text_df'] = pd.DataFrame.from_dict(chosenTexts[index]['df'], orient='index')
        placeholderObject[index]['text_df'] = placeholderObject[index]['text_df'].transpose()
    
        tfidf = TfidfVectorizer(stop_words="english")
        placeholderObject[index]['df_abstracts_tfidf'] = tfidf.fit_transform(placeholderObject[index]['text_df'])    
        print("DF ABSTRACTS TFIDF SCIKIT", placeholderObject[index]['df_abstracts_tfidf'])
        # entities = old_df["entities"]
        
        for idx, s in enumerate(chosenTexts[index]['sents'][0:30]):
            ### vectorize features in array of sentences
            vectorizer = CountVectorizer()
            placeholderObject[index]['features'] = vectorizer.fit_transform(chosenTexts[index]['sents'][0:10]).todense() 
            #features2 = vectorizer.fit_transform(list("This is test sentence")).todense()
            if idx == len(chosenTexts[index]['sents'][0:10]) - 1:
                # soct.send('explain_tfidf')
                # soct.send(str(placeholderObject[index]['features']))
                print(f"VECTORIZED VOCAB: {vectorizer.vocabulary_}")
                print(f"FEATURES!@ COUNT VECTORIZER {placeholderObject[index]['features'] }")
            placeholderObject[index]['old_df_vectorized_features'].append(placeholderObject[index]['features'] )
            placeholderObject[index]['old_df_vectorized_vocab'].append(vectorizer.vocabulary_)

            tfidf = TfidfVectorizer()

            try:
                y = tfidf.fit_transform([s])
                # tfidf.get_feature_names()
                placeholderObject[index]['df_feat'] = pd.DataFrame(y.np.asarray(), columns = tfidf.get_feature_names()).to_json()
                print(f"df feat TFIDF!!!! {placeholderObject[index]['df_feat'].keys()} / vals: {placeholderObject[index]['df_feat'].values().values()}")
                # soct.send('explain_tfidf')
                
                for tfidf in placeholderObject[index]['df_feat'].values():
                    print("CHECK TFIDF: ", tfidf)
                    print("CHECK TFIDF KEYS: ", tfidf.keys()[0])
                    print("CHECK TFIDF VALUES: ", tfidf.values()[0])

                    #soct.send(str({tfidf.keys()[0]:tfidf.values()[0]}))
                
                placeholderObject[index]['old_df_vectorized_tfidf'].append([placeholderObject[index]['df_feat']])

            except:
                print('')
       
            soct.send("explain_euclidean_distance")
            ## WE'll want to bring this back!!!
            for i, f in enumerate(placeholderObject[index]['features']):
                # print(f"EUCLIDEAN DIST: {euclidean_distances(f, features[i-1])}")
                # old_df_euclidean_distance_since_last_self.append(euclidean_distances(f,features[i-1]))
            
                # soct.send(euclidean_distances(f, features[i-1])[0][0])
                # print("TYPEOF EUCLIDEAN DISTANCE's F: ", type(f))
                # print(f"EUCLIDEAN DIST: {euclidean_distances(f, placeholderObject[0]['features'][i-1])}")

                placeholderObject[index]['old_df_euclidean_distance_since_last_self'].append(euclidean_distances(f,placeholderObject[0]['features'][i-1]))
            
                soct.send(str(euclidean_distances(f, placeholderObject[0]['features'][i-1])[0][0]))
                # print("WHAT ARE CHOSEN TEXTS? ", chosenTexts[index])
                print('EUC DIST: ', euclidean_distances(f, placeholderObject[0]['features'][i-1])[0][0])
                #df = pd.DataFrame({"id": [i for i in placeholderObject[index]['features'] if type(chosenTexts[index])==float or type(chosenTexts[index]) == int], "temperature": [f['df']['sentence_sentiment_neg'] for f in chosenTexts[index] if type(chosenTexts[index])==float or type(chosenTexts[index]) == int], "pressure": [g['df']['sentence_sentiment_pos'] for g in chosenTexts[index] if type(chosenTexts[index])==float or type(chosenTexts[index]) == int]})
                # df = pd.DataFrame(
                #     [i for i in placeholderObject[index]['features'] if type(chosenTexts[index])==float or type(chosenTexts[index]) == int]
                # )
                # df = pd.DataFrame("euclidean_distances":placeholderObject[index]['old_df_euclidean_distance_since_last_self'],)
                # print(f"check this dataframe: {df}")


                soct.send("explain_progressive_feature_selection")
                # for (columnName, columnData) in df.iteritems():
        
                    # print(df.head(5))
                    # print(f"what is this? {text_df['temperature']}")
                    # print(f"sanity sake: {type(df[columnName])}")
                    # if type(df[columnName][0]) != "float":
                    #     return

        machine_dict['vectorized_vocab'] = placeholderObject[index]['old_df_vectorized_vocab'][0]
        machine_dict['vectorized_tfidf'] = placeholderObject[index]['old_df_vectorized_tfidf']
        machine_dict['euclidean_distance_since_last_self'] = [i[0][0] for i in placeholderObject[index]['old_df_euclidean_distance_since_last_self']]        
        machine_dict['vectorized_features'] = [i for i in placeholderObject[index]['old_df_vectorized_features']]


        print("WHAT IS MACHINE DICT?? ", machine_dict)
        ## this allows us to keep testing before all ML is ready or useful
        soct.send("fifteenth_msg")
        return machine_dict

        return 0
    
