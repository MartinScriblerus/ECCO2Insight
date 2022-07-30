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

from tsfresh.examples import load_robot_execution_failures
from tsfresh.transformers import RelevantFeatureAugmenter
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import extract_features
from tsfresh.feature_extraction import settings
import pandas as pd
import sys

machine_dict = {}

def machine_learning(old_df,sents): 

    if 'flask_init' in sys.modules:
        from flask_init import soct

    old_df_vectorized_features = []
    old_df_vectorized_vocab = []
    old_df_vectorized_tfidf = []
    old_df_euclidean_distance_since_last_self = []

    text_df = pd.DataFrame.from_dict(old_df, orient='index')
    text_df = text_df.transpose()
    
    tfidf = TfidfVectorizer(stop_words="english")
    df_abstracts_tfidf = tfidf.fit_transform(text_df)    
    print("DF ABSTRACTS TFIDF SCIKIT", df_abstracts_tfidf)

    soct.send("eleventh_msg")

    for idx, s in enumerate(sents):
        ### vectorize features in array of sentences
        vectorizer = CountVectorizer()
        features = vectorizer.fit_transform(sents).todense() 
        #features2 = vectorizer.fit_transform(list("This is test sentence")).todense()
        if idx == len(sents) - 1:
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

        soct.send("twelfth_msg") 

        ## WE'll want to bring this back!!!
        for i, f in enumerate(features):
            print(f"EUCLIDEAN DIST: {euclidean_distances(f, features[i-1])}")
            old_df_euclidean_distance_since_last_self.append(euclidean_distances(f,features[i-1]))
           
    # soct.send("twelfth_msg")
    df = pd.DataFrame({"id": [i for i in old_df['sentence_id']], "temperature": [f for f in old_df['sentence_sentiment_neg']], "pressure": [g for g in old_df['sentence_sentiment_pos']]})
    print(f"TUUUUST: {df}")
    settings_minimal = settings.MinimalFCParameters() 
    # print(f"MIN SEETT TUUST: {settings_minimal}")
    soct.send("thirteenth_msg")
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
    soct.send("fourteenth_msg")
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
            soct.send("fifteenth_msg")
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
            print(f"ARE WE GETTING CLUSTERS? {df_authors_standardized_pca['clusters']}")
            # plotting the clusters with seaborn
            sns.scatterplot(x="pc_1", y="pc_2", hue="clusters", data=df_authors_standardized_pca)
            
    # initial_text = old_df

    machine_dict['vectorized_features'] = old_df_vectorized_features
    machine_dict['vectorized_vocab'] = old_df_vectorized_vocab
    machine_dict['vectorized_tfidf'] = old_df_vectorized_tfidf
    machine_dict['euclidean_distance_since_last_self'] = old_df_euclidean_distance_since_last_self

    return machine_dict

