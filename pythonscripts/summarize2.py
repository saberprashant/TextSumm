


from __future__ import absolute_import    
from __future__ import division, unicode_literals

import string
import collections
import os, glob, sys
from time import time
import numpy as np

from nltk.tokenize import sent_tokenize     #for sentence tokenizing
from nltk.tokenize import word_tokenize     #for word tokenizing
from nltk.tokenize import RegexpTokenizer    #for regex tokenizing by removing punctuations
from nltk.stem import PorterStemmer   
from nltk.corpus import stopwords  

from sklearn import preprocessing       #using label
from sklearn.feature_extraction.text import TfidfVectorizer     #tfidf vectorizing
from sklearn.cluster import KMeans 
from sklearn.cluster import MeanShift
from sklearn.metrics import adjusted_rand_score
from sklearn.cluster import MiniBatchKMeans
from sumy.parsers.plaintext import PlaintextParser
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import CountVectorizer     #count vectorizing
from sumy.nlp.tokenizers import Tokenizer
from sklearn.feature_extraction.text import TfidfTransformer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sklearn.feature_extraction.text import HashingVectorizer      #hash vectorizing
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
clusters = 5     #no. of clusters --> sys.argv[2]



def process_text(text, stem=True):
    # Tokenize text and stem words removing punctuation 
  
    stop_words = set(stopwords.words('english'))
    
    tokens = sent_tokenize(text)
    reg_tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = reg_tokenizer.tokenize(text)
    wd_filter = [w for w in word_tokens if not w in stop_words]

 
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
        # wd_tokens = [stemmer.stem(t) for t in wd_tokens]
        
    print
    # print tokens  #testing
    # print wd_filter

    return wd_filter, tokens



def k_cluster(texts, clusters=2):
    #vectorize the text i.e. convert the strings to numeric features
    t0 = time()
    tf_vectorizer = TfidfVectorizer(stop_words='english')
    X = tf_vectorizer.fit_transform(texts)
    tx = time() - t0

    print "Analysis : "
    print "Shape using Tfidf Vectorizer :  ",
    print X.shape   
    print "Tfidf Vectorizing time in s: %f " % tx

    t0 = time()
    count_vectorizer = CountVectorizer()
    Y = count_vectorizer.fit_transform(texts)
    ty = time() - t0
    print "Shape using Count Vectorizer :  ",
    print Y.shape   
    print "Count Vectorizing time in s: %f " % ty

    t0 = time()
    hash_vectorizer = HashingVectorizer(stop_words='english', alternate_sign=False,
                                   norm=None, binary=False)
    Z = hash_vectorizer.fit_transform(texts)
    tz = time() - t0
    print "Shape using Hashing Vectorizer :  ",
    print Z.shape   
    print "Hashing Vectorizing time in s: %f " % tz

    t0 = time()
    count_vec = count_vectorizer.fit_transform(texts)
    tf_transformer = TfidfTransformer(use_idf=False).fit(count_vec)  
    Y_tfidf = tf_transformer.transform(count_vec)
    t_tf = time() - t0
    print "Shape using Count Vectorizer and tf-idf transformer :  ",
    print Y_tfidf.shape   
    print "Count Vectorizing and tf-idf transforming time in s: %f " % t_tf

    t0 = time()
    hash_vec = hash_vectorizer.fit_transform(texts)
    htf_transformer = TfidfTransformer(use_idf=False).fit(hash_vec)
    Z_htfidf = htf_transformer.transform(hash_vec)   
    t_htf = time() - t0
    print "Shape using Hashing Vectorizer and tf-idf transformer :  ",
    print Z_htfidf.shape   
    print "Hashing Vectorizing and tf-idf transforming time in s: %f " % t_htf


    t0 = time()
    #cluster documents
    #true_k = 2          #no. of clusters
    k_model = KMeans(n_clusters=clusters, init='k-means++', max_iter=100, n_init=1)
    k_model.fit(X)
    k_time = time() - t0

    print
    #print top terms per cluster clusters
    print("K-Means :: Top terms per cluster :")
    order_centroids = k_model.cluster_centers_.argsort()[:, ::-1]
    terms = tf_vectorizer.get_feature_names()
    for i in range(clusters):
        print "Cluster %d:" % i,
        for ind in order_centroids[i, :15]:
            print ' %s' % terms[ind],
        print
    return k_time



def mean_cluster(texts, clusters = 2):

    t0 = time()
    tf_vectorizer = TfidfVectorizer(stop_words='english')
    X = tf_vectorizer.fit_transform(texts)
    tx = time() - t0
  
    t0 = time()
    mean_model = MeanShift(bandwidth=None, seeds=None, bin_seeding=False, 
            min_bin_freq=1, cluster_all=True, n_jobs=1)
    mean_model.fit(X.toarray())
    mean_time = time() - t0
    print
    #print top terms per cluster clusters
    print("MeanShift :: Top terms per cluster :")
    order_centroids = mean_model.cluster_centers_.argsort()[:, ::-1]
    terms = tf_vectorizer.get_feature_names()
    labels = mean_model.labels_
    cluster_centers = mean_model.cluster_centers_
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    # print labels     #testing
    # print cluster_centers
    # print labels_unique
    # print n_clusters_
    for i in range(n_clusters_):
        print "Cluster %d:" % i,
        for ind in order_centroids[i, :100]:
            print ' %s' % terms[ind],
        print
    return mean_time
    


def mini_cluster(texts, clusters = 2):
    t0 = time()
    tf_vectorizer = TfidfVectorizer(stop_words='english')
    X = tf_vectorizer.fit_transform(texts)
    tx = time() - t0
 
    t0 = time()
    mini_model = MiniBatchKMeans(init='random', n_clusters=clusters,n_init=1,
                 max_iter=101, batch_size=100, verbose=0)
    mini_model.fit(X)
    mini_time = time() - t0
    print
    #print top terms per cluster clusters
    print("Mini Batch :: Top terms per cluster :")
    order_centroids = mini_model.cluster_centers_.argsort()[:, ::-1]
    terms = tf_vectorizer.get_feature_names()
    for i in range(clusters):
        print "Cluster %d:" % i,
        for ind in order_centroids[i, :15]:
            print ' %s' % terms[ind],
        print
    return mini_time

def aglo_cluster(texts, wd_filter, clusters = 2):
    t0 = time()
    tf_vectorizer = TfidfVectorizer(stop_words='english')
    X = tf_vectorizer.fit_transform(texts)
    tx = time() - t0

    le = preprocessing.LabelEncoder()
    le.fit(wd_filter)
    # print list(le.inverse_transform([6, 2, 1]))
    #print list(le.classes_)

    t0 = time()
    ag_model = AgglomerativeClustering(linkage='ward', n_clusters=clusters)
    ag_model.fit(X.toarray())
    ag_time = time() - t0
    print
    print("Agglomerative :: Top terms of cluster :")
    terms = tf_vectorizer.get_feature_names()
    labels = ag_model.labels_
    inverse_labels = list(le.inverse_transform(labels))
    n_leaves = ag_model.n_leaves_
    # print labels
    # print n_leaves
    print inverse_labels
    return ag_time

def time_analysis(kt, mit, met, at):
    print '@'
    # $ kmeans
    # ! mini
    # @ mean shift
    # * aglo
    print "$ : a%fb, ! : c%fd, @ : e%ff, * : g%fh" % (kt, mit, met, at)

def summ_checker(input_file, SENTENCES_COUNT = 3):
    print '$'
    LANGUAGE = "english"
    parser = PlaintextParser.from_file(input_file, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    # print     #new line
    print "Summary :"
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print sentence


def main():
    document_file = 'public/Input_Files/'+sys.argv[1]+'.txt'
    with open(document_file, "r+") as doc:
            inputd = doc.read()
            # print inputd       #testing
    wd_filter, token_text = process_text(inputd)   #n_samples
    k_time = k_cluster(token_text,clusters)
    mini_time = mini_cluster(token_text,clusters)
    mean_time = mean_cluster(token_text, clusters)
    ag_time = aglo_cluster(token_text, wd_filter, clusters)
    #print(dict(clusters))
    time_analysis(k_time, mini_time, mean_time, ag_time)
    summ_checker(document_file, clusters)     
 
if __name__ == "__main__": main()