import glob
import random
import os

def doc_chooser():
    
    #Picks 500 (10% of 5000) random files to move to docs/ subfolder 
    i = 0
    files = glob.glob('*/*/*/*.json')
    while i < 500:
        #Pick random file from glob
        rd = random.choice(files)

        #Move chosen file
        command = 'mv ' + rd + ' docs/' 
        os.system(command)    
        i = i + 1
 

################################################################
#Reads .json files in given loc and returns dataframe of paper_id and text
import json
import pandas as pd

def file_reader(loc, fileNames):

    text = [] 
    id_ = []
    
    #Goes through each .json file in /docs subfolder
    files = glob.glob(loc + fileNames)
    for file in files:

        f = open(file, 'r')
        #Reads json file
        content = json.loads(f.read())

        #Abstract exists
        if 'abstract' in content.keys():
            txt = ''
            for entry in content['abstract']:
                #Merge all sentences together
                txt = txt + entry['text']
            
            if(len(txt) > 15):
                text.append(txt)
                id_.append(content['paper_id'])
                    
        #Abstract doesn't exist, add body_text instead
        else:
            txt = ''
            for entry in content['body_text']:
                #Merge all sentences together
                txt = txt + entry['text']
                        
            if(len(txt) > 15):
                text.append(txt)
                id_.append(content['paper_id'])


    data = {'Paper_ID' : id_, 'Text' : text}
    df = pd.DataFrame(data)
    print(df)
    
    return(df)


###############################################################
#Cluster documents using k-means clustering method
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from progress.bar import Bar

def cluster(text):
    
    #Vectorize text
    stop_words = nltk.corpus.stopwords.words('english')
    vec = CountVectorizer(stop_words = stop_words)
    cv_matrix = vec.fit_transform(text['Text'])
    

    #Find optimal # of clusters using elbow method & comparing silhouette score
    '''
    wcss = []
    sil = []
    bar = Bar('Processing', max = 14)
    for i in range (2, 15):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        kmeans.fit(cv_matrix)
        wcss.append(kmeans.inertia_)
        
        cluster_labels = kmeans.fit_predict(cv_matrix)
        sil_avg = silhouette_score(cv_matrix, cluster_labels)
        sil.append(sil_avg)
        bar.next()
    
    bar.finish()
    elbow ={'Cluster_no' : range(2, 15), 'WCSS' : wcss, 'Silhouette Coeff' : sil}
    edf = pd.DataFrame(elbow)
    print(edf) 
    '''
    clusters = 14

    km = KMeans(n_clusters = clusters, max_iter = 1000, n_init = 10, random_state = 42).fit(cv_matrix)
    terms = vec.get_feature_names()
    ordered_centroids = km.cluster_centers_.argsort()[:,::-1]
    

    #Prints key features and documents in each cluster
    for i in range(clusters):
        key_features = [terms[index] for index in ordered_centroids[i, :10]]
        print('CLUSTER #' + str(i + 1))        
        print('Top 10 Key Features: ', key_features)
        print('Documents:')

        #Prints documents in each cluster
        for j in range(len(km.labels_)):
            if(km.labels_[j] == i):
                print(text['Paper_ID'][j])
        print() 


    text['Cluster'] = km.labels_
    #print(text)
    return(text, clusters)


###############################################################
#Summarizes on a document level using text rank (tr)algorithm
import numpy as np
from nltk.tokenize import sent_tokenize
import networkx
import spacy
nlp = spacy.load('en_core_web_sm')

def summarize_tr(text, clusters):
    
    summarized = []
    for i in range(len(text)):
        
        #print('Original Text:')
        #print(text['Text'][i])
        
        #Tokenize sentences
        sentences = nltk.sent_tokenize(text['Text'][i])

        #Vectorize each tokenized sentence
        stop_words = nltk.corpus.stopwords.words('english')
        vec = CountVectorizer(min_df = 0., max_df = 1., stop_words = stop_words)    
            
        #Build document-term frequency matrix
        dt_matrix = vec.fit_transform(sentences)
        dt_matrix = dt_matrix.toarray()
    
        vocab = vec.get_feature_names()
        td_matrix = dt_matrix.T
            
        #Compute document similarity matrix
        sim_matrix = np.matmul(dt_matrix, td_matrix)
        sim_graph = networkx.from_numpy_array(sim_matrix)    
            
        #Compute pagerank scores for all sentences and sort
        scores = networkx.pagerank(sim_graph)
        ranked_sentences = sorted(((score, index) for index, score in scores.items()))
            
        #Prints summary
        if(len(ranked_sentences) < 4):
            top_sentence_indices = [ranked_sentences[index][1] for index in range(1)]
        else:
            top_sentence_indices = [ranked_sentences[index][1] for index in range(4)]
            
        top_sentence_indices.sort()
        summary = ('\n'.join(np.array(sentences)[top_sentence_indices]))
        summarized.append(summary)
             
        #print('Summary:')
        #print(summary)
        #print()
     
    text['Summarized'] = summarized
    return(text, clusters)
            

###############################################################
#Summarizes on a document level using latent semantic analysis (lsa) algorithm
from scipy.sparse.linalg import svds

def summarize_lsa(text, clusters):

    summarized = []
    for i in range(len(text)):

        #print('Original Text:')
        #print(text['Text'][i])

        #Tokenize sentences
        sentences = nltk.sent_tokenize(text['Text'][i])
        
        #Vectorize each tokenized sentence
        stop_words = nltk.corpus.stopwords.words('english')
        vec = CountVectorizer(min_df = 0., max_df = 1., stop_words = stop_words)
        
        #Build document-term frequency matrix
        dt_matrix = vec.fit_transform(sentences)
        dt_matrix = dt_matrix.toarray()
        
        vocab = vec.get_feature_names()
        td_matrix = dt_matrix.T
        td_matrix = td_matrix.astype(float)

        try:
            u, s, vt = svds(td_matrix, k = 3)
            term_topic_mat, singular_values, topic_document_mat = u, s, vt

            sv_threshold = 0.5
            min_sigma_value = max(singular_values) * (sv_threshold) 
            salience_scores = np.sqrt(np.dot(np.square(singular_values), np.square(topic_document_mat)))
        
            top_sentence_indices = (-salience_scores).argsort()[:4]
            top_sentence_indices.sort()
            summary = ('\n'.join(np.array(sentences)[top_sentence_indices]))
            summarized.append(summary)
        
        except ValueError:

            print('error')
            summary = text['Text'][i]
            summarized.append(summary)

        #print('Summary:')
        #print(summary)
        #print()

    text['Summarized'] = summarized
    return(text, clusters)


###############################################################
#Writes summary for each document per cluster

def write_summary(text, clusters, method):

    text.sort_values(by=['Cluster'])

    i = 0
    for cluster in range(clusters):
        f = open('output/cluster_' + str(cluster) + '_' + method + '.md', 'w+') 
        f.write('CLUSTER ' + str(cluster) + ' SUMMARIZATIONS: \n\n')
        
        while (i < len(text) and text['Cluster'][i] == cluster):
            
            f.write(str(i) + '. Document: ' + text['Paper_ID'][i] + '\n')
            f.write('Summary : \n')
            f.write(text['Summarized'][i] + '\n\n')
            i = i + 1

        f.close()


################################################################
if __name__ == '__main__':
    
    #doc_chooser() - commented out b/c only needs to run once @ beginning of code
    fileNames = '*.json'

    df = file_reader('docs/', fileNames)
    text, clusters = cluster(df)
    
    text, clusters = summarize_tr(text, clusters)
    #text, clusters = summarize_lsa(text, clusters)
    write_summary(text, clusters, 'tr')
    

