########################################################################
########################################################################
######################### FEATURE ANALYSIS #############################
########################################################################
########################################################################

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

# def set_soct_mach(soct_import):
#     global soct
#     soct = soct_import

def machine_learning(old_df,sents,soct): 
    # if 'flask_init' in sys.modules:
    #     from flask_init import soct
    soct.send("eleventh_msg")
    print("are we getting soct? ", soct)
    old_df_vectorized_features = []
    old_df_vectorized_vocab = []
    old_df_vectorized_tfidf = []
    old_df_euclidean_distance_since_last_self = []

    text_df = pd.DataFrame.from_dict(old_df, orient='index')
    text_df = text_df.transpose()
    
    tfidf = TfidfVectorizer(stop_words="english")
    df_abstracts_tfidf = tfidf.fit_transform(text_df)    
    print("DF ABSTRACTS TFIDF SCIKIT", df_abstracts_tfidf)
    entities = old_df["entities"]
    for idx, s in enumerate(sents[0:30]):
        ### vectorize features in array of sentences
        vectorizer = CountVectorizer()
        features = vectorizer.fit_transform(sents[0:10]).todense() 
        #features2 = vectorizer.fit_transform(list("This is test sentence")).todense()
        if idx == len(sents[0:10]) - 1:
            print(f"VECTORIZED VOCAB: {vectorizer.vocabulary_}")
            print(f"FEATURES!@ COUNT VECTORIZER {features}")
            # soct.send("explain_vectorized_vocab")
            # soct.send(vectorizer.vocabulary_)
        old_df_vectorized_features.append(features)
        old_df_vectorized_vocab.append(vectorizer.vocabulary_)

        tfidf = TfidfVectorizer()

        try:
            y = tfidf.fit_transform([s])
            tfidf.get_feature_names()
            df_feat = pd.DataFrame(y.toarray(), columns = tfidf.get_feature_names()).to_json()
            print(f"df feat TFIDF!!!! {type(df_feat)}")
            soct.send('explain_tfidf')
            for tfidf in df_feat.values():
                soct.send(str({tfidf.keys()[0]:tfidf.values()[0]}))
            old_df_vectorized_tfidf.append(df_feat)

            # soct.send("twelfth_msg") 
        except:
            print('')
            ## make this an error handler
            # soct.send('twelfth_msg')
        # y.toarray()
       
        soct.send("explain_euclidean_distance")
        ## WE'll want to bring this back!!!
        for i, f in enumerate(features):
            # print(f"EUCLIDEAN DIST: {euclidean_distances(f, features[i-1])}")
            # old_df_euclidean_distance_since_last_self.append(euclidean_distances(f,features[i-1]))
            
            # soct.send(euclidean_distances(f, features[i-1])[0][0])
            print("TYPEOF EUCLIDEAN DISTANCE's F: ", type(f))
            print(f"EUCLIDEAN DIST: {euclidean_distances(f, features[i-1])}")


            ## attempt clustering 
            # euc_dist = euclidean_distances(f, features[i-1])
            # vectors = [array(f) for f in features]
            # # initialise the clusterer (will also assign the vectors to clusters)
            # clusterer = cluster.KMeansClusterer(2, euclidean_distance)
            # clusterer.cluster(vectors, True)

            # classify a new vector //w random number
            # print(clusterer.classify(array(features[10])))

            old_df_euclidean_distance_since_last_self.append(euclidean_distances(f,features[i-1]))
            
            soct.send(euclidean_distances(f, features[i-1])[0][0])
            # # soct.send("eleventh_msg")         
            # # soct.send("twelfth_msg")
            df = pd.DataFrame({"id": [i for i in old_df['sentence_id']], "temperature": [f for f in old_df['sentence_sentiment_neg']], "pressure": [g for g in old_df['sentence_sentiment_pos']]})
            print(f"TUUUUST: {df}")

            # print("DF COLS:::: ", [i['temperature'] for i in df])
            # df = pd.DataFrame(euclidean_distances(f,features[i-1]))

            # from sklearn.preprocessing import StandardScaler as SS # z-score standardization 
            # from sklearn.cluster import KMeans, DBSCAN # clustering algorithms
            # from sklearn.decomposition import PCA # dimensionality reduction
            # from sklearn.metrics import silhouette_score # used as a metric to evaluate the cohesion in a cluster
            # from sklearn.neighbors import NearestNeighbors # for selecting the optimal eps value when using DBSCAN
            # # import numpy as np

            # # plotting libraries
            # import matplotlib.pyplot as plt


            # def progressiveFeatureSelection(df, n_clusters=3, max_features=4,):
            #     '''
            #     very basic implementation of an algorithm for feature selection (unsupervised clustering); inspired by this post: https://datascience.stackexchange.com/questions/67040/how-to-do-feature-selection-for-clustering-and-implement-it-in-python
            #     '''
            #     feature_list = list(df.columns)
            #     selected_features = list()
            #     # select starting feature
            #     initial_feature = ""
            #     high_score = 0
            #     for feature in feature_list:
            #         kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            #         soct.send(f"KMEANS_{kmeans}")
            #         data_ = df[feature]
            #         labels = kmeans.fit_predict(data_.to_frame())
            #         score_ = silhouette_score(data_.to_frame(), labels)
            #         print("Proposed new feature {} with score {}". format(feature, score_))
            #         if score_ >= high_score:
            #             initial_feature = feature
            #             high_score = score_
            #     print("The initial feature is {} with a silhouette score of {}.".format(initial_feature, high_score))
            #     feature_list.remove(initial_feature)
            #     selected_features.append(initial_feature)
            #     for _ in range(max_features-1):
            #         high_score = 0
            #         selected_feature = ""
            #         print("Starting selection {}...".format(_))
            #         for feature in feature_list:
            #             selection_ = selected_features.copy()
            #             selection_.append(feature)
            #             kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            #             data_ = df[selection_]
            #             labels = kmeans.fit_predict(data_)
            #             score_ = silhouette_score(data_, labels)
            #             print("Proposed new feature {} with score {}". format(feature, score_))
            #             if score_ > high_score:
            #                 selected_feature = feature
            #                 high_score = score_
            #         selected_features.append(selected_feature)
            #         feature_list.remove(selected_feature)
            #         # if soct is not None:
            #         #     soct.send("fifteenth_msg")
            #         print("Selected new feature {} with score {}". format(selected_feature, high_score))
            #     # soct.send("fifteenth_msg")
            #     return selected_features


  
            for (columnName, columnData) in df.iteritems():
        
                print(df.head(5))
                # print(f"AWESOME BUT WTF IS THIS? {text_df['temperature']}")
                # print(f"sanity sake: {type(df[columnName])}")
                # if type(df[columnName][0]) != "float":
                #     return
                soct.send("explain_progressive_feature_selection")
        
        # # try:
        #     # if soct is not None:
        #     #     soct.send("twelfth_msg")  
        #         for s in text_df[columnName].values.reshape(1, -1): 
        # #  

        #             try:
        #                 DNP_text_standardized = scaler.fit_transform(s, s)
        #                 df_text_standardized = pd.DataFrame(DNP_text_standardized, index_col=columnName)
        #                 df_text_standardized = df_text_standardized.set_index(text_df.index)

        #                 selected_features = progressiveFeatureSelection(df_text_standardized, max_features=3, n_clusters=3)
        #                 optimal_features = optimal_features(df_text_standardized)
        #                 # print("SELECTED FEATURES: ", selected_features)
        #                 df_standardized_sliced = df_text_standardized[selected_features]
        #                 DNP_text_standardized = scaler.fit_transform(df_standardized_sliced.reshape(-1,1),df_standardized_sliced.reshape(-1,1))
        #                 print("DNP text standardized", DNP_text_standardized )
                        
        #                 df_standardized_sliced = df_text_standardized[selected_features]

        #                 kmeans = KMeans(n_clusters=5, random_state=42)
        #                 cluster_labels = kmeans.fit_predict(df_standardized_sliced)
        #                 df_standardized_sliced["clusters"] = cluster_labels

        #                 print( df_standardized_sliced.info())

        #                 # show first 5 rows
        #                 print( df_standardized_sliced.head(5))

        #                 # display some statistics
        #                 print( df_standardized_sliced.describe())

        #                 # using PCA to reduce the dimensionality
        #                 pca = PCA(n_components=2, whiten=False, random_state=42)
        #                 texts_standardized_pca = pca.fit_transform(df_standardized_sliced)
        #                 df_texts_standardized_pca = pd.DataFrame(data=texts_standardized_pca, columns=["pc_1", "pc_2"])
        #                 df_texts_standardized_pca["clusters"] = cluster_labels
        #                 print(f"ARE WE GETTING CLUSTERS? {df_authors_standardized_pca['clusters']}")
                        

        #                 print(df_texts_standardized_pca.info())

        #                 # show first 5 rows
        #                 print(df_texts_standardized_pca.head(5))

        #                 # display some statistics
        #                 print(df_texts_standardized_pca.describe())
        #             except ValueError:
        #                 print('Value Error #1!')
        
            
        #     # elbowPlot(range(1,11), df_standardized_sliced)
        #     # silhouettePlot(range(3,9), df_standardized_sliced)


                    

        #             try:
        #                 print(f"WHAT IS DAAATTTAAAFFFRRRAAAAMMMMEEE????? {df_text_standardized.head(5)} {df_text_standardized.describe()}")
        #                 selected_features = progressiveFeatureSelection(df_text_standardized, max_features=3, n_clusters=3)
        #                 optimal_features = optimal_features(df_text_standardized)
        #                 print("SELECTED FEATURES: ", selected_features)
        #                 df_standardized_sliced = df_text_standardized[selected_features]

        #                 print( df_standardized_sliced.info())

        #                 # show first 5 rows
        #                 print( df_standardized_sliced.head(5))

        #                 # display some statistics
        #                 print( df_standardized_sliced.describe())
        #             except ValueError:
        #                 print('Value Error 4!')

        #             try:   
        #                 # elbowPlot(range(1,11), df_standardized_sliced)
        #                 # silhouettePlot(range(3,9), df_standardized_sliced)
        #                 # if soct is not None:
        #                 #     soct.send("thirteenth_msg")  
        #                 kmeans = KMeans(n_clusters=5, random_state=42)
        #                 cluster_labels = kmeans.fit_predict(df_standardized_sliced)
        #                 df_standardized_sliced["clusters"] = cluster_labels
        #                 print("SLICED CLUSTERS: ", df_standardized_sliced["clusters"])
        #                 # using PCA to reduce the dimensionality
        #                 pca = PCA(n_components=2, whiten=False, random_state=42)
        #                 authors_standardized_pca = pca.fit_transform(df_standardized_sliced)
        #                 df_authors_standardized_pca = pd.DataFrame(data=authors_standardized_pca, columns=["pc_1", "pc_2"])
        #                 df_authors_standardized_pca["clusters"] = cluster_labels
        #                 print(f"ARE WE GETTING CLUSTERS? {df_authors_standardized_pca['clusters']}")
        #                 # plotting the clusters with seaborn
        #                 # sns.scatterplot(x="pc_1", y="pc_2", hue="clusters", data=df_authors_standardized_pca)
        #             ## MAKE THIS AN ERROR HANDLER
        #             # soct.send("fourteenth_msg")        
        #             # # initial_text = old_df
        #             except ValueError:
        #                 print('Value Error!')
        #             # except:
        #             #     print('not handling strings')

        #                 # from sklearn import preprocessing
        #                 # try:
        #                 #     text_df[columnName].astype('string')
        #                 # except ValueError as e:
        #                 #     # raise e
        #                 #     print(f"EEEEEEEEEEE IS {e}")
        #                 #     text_df[columnName].astype('float')
        #                 # reshaped = text_df[columnName].values.reshape(-1,1)
        #                 # le = preprocessing.LabelEncoder()

        #                 # le.fit(reshaped.astype(str))
        #                 # list(le.classes_)
        #                 # transformedColumn = le.transform(reshaped.astype(str))
        #                 # if soct is not None:
        #                 #     soct.send("fifteenthfth_msg") 
    machine_dict['vectorized_features'] = old_df_vectorized_features
    machine_dict['vectorized_vocab'] = old_df_vectorized_vocab
    machine_dict['vectorized_tfidf'] = old_df_vectorized_tfidf
    machine_dict['euclidean_distance_since_last_self'] = old_df_euclidean_distance_since_last_self
    print("WHAT IS MACHINE DICT??")
    ## this allows us to keep testing before all ML is ready or useful
    soct.send("fifteenth_msg")
    return machine_dict

    return 0
    
