#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Short summary that describe what the algorithm does
"""


import os
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from unicodedata import normalize
from string import maketrans
from string import punctuation


__author__ = 'Giacomo Legnaro'
__version__ = '0.0'
__email__ = 'g.legnaro@gmail.com'
__status__ = 'Production'
__date__ = 'August 1st, 2016'
__studentID__ = '1724522'


def Tokenization(document):
    """
    Return the list of all the words in the document.

    :param document: document file name to be tokenized
    """
    # string.punctuation is the list of the punctuation characters
    replace_punctuation = maketrans(
        punctuation, ' '*len(punctuation))
    # maketrans is a function of library string that make a couple between
    # two character to make a substitution with translate function.
    # It's like a vocabolary italian-english
    text = \
        document.encode('utf-8').translate(replace_punctuation).decode('utf-8')
    tokens = word_tokenize(text)
    return tokens


def RMStopWords(bow, stop_words):
    """
    Return the words of a document without stopwords.

    Keyword arguments:
    :param bow: bag of words to be tokenized
    :param stopW: string_name is the name of file that is processing( string);
    """

    stem_words = ['vendo', 'vendesi', 'mappa', 'nome', 'indirizzo', 'situato']
    for w in stem_words:
        stop_words.append(w.decode('utf-8'))
    stop_dict = {w: None for w in stop_words}
    vocabulary = [t for t in Tokenization(bow) if t not in stop_dict]
    return vocabulary


def Normalization(bow):
    """
    Return the words without the accent

    :param bow: bag of words to be processed with a normalization algorithm
    """

    stop_words = stopwords.words('italian')
    words_list = [normalize('NFKD', b).encode(
        'ascii', 'ignore') for b in RMStopWords(bow, stop_words)]
    return words_list


def Stemming(bow, stemmer):
    """
    Return the words stemmed

    :param bow: bag of words to be stemmed
    :param stemmer: the stem words corresponding to words
    """
    text_norm = Normalization(bow)
    vocabulary = [stemmer.stem(w) for w in text_norm]
    for w in vocabulary:
        if len(w) < 1:
            vocabulary.remove(w)
    return [v for v in vocabulary if len(v) > 0]


def algorithmBoW(main_dir):
    """
    Return the list of the word of each advertise.
    This algorithm is a Bag-of-Words model

    :param main_dir: main directory which are located all the subfolders with
                     the documents
    """
    bow = []
    stemmer_snow = SnowballStemmer('italian')
    # Snowball is a small string processing programming language designed
    # for creating stemming algorithms for use in information retrieval
    sub_dir_sort = sorted(os.listdir(main_dir))
    if '.DS_Store' in sub_dir_sort:
        sub_dir_sort.remove('.DS_Store')
    for d_item in sub_dir_sort:
        sub_sub_dir_sort = sorted(os.listdir(main_dir + '/' + d_item))
        if '.DS_Store' in sub_sub_dir_sort:
            sub_sub_dir_sort.remove('.DS_Store')
        for f_item in sub_sub_dir_sort:
            with open(os.path.join(main_dir, d_item, f_item), 'r+') as f:
                f = re.sub('[^a-zA-Z]', ' ', f.read())
                f = f.lower()
                f = f.replace('\x80', '\xe2\x82\xac')  # €
                # f = f.replace('\xc3', '\xc3\x83')  # Ã
                # f = f.replace('\xac', '\xc2\xac')  # ¬
                f = f.decode('utf-8')
                f = f.replace("'", ' ').split('\t')
                # del f[3]  # remove the price
                # delete the url of the ad
                f = '\t'.join(f)
                bow.append(Stemming(f, stemmer_snow))
    return bow


# This is a duplicate of the collect file
def makeDirectory(path, directory):
    """
    Return the directory path where save the documents

    :param path: path where create the new folder
    :param directory: name of the new folder
    """
    try:
        os.makedirs(os.path.join(path, directory))
    except OSError:
        if not os.path.isdir(os.path.join(path, directory)):
            raise
    return os.path.join(path, directory)


def makeVocabulary(bow, directory):
    """
    Return the vocabulary.txt file
    The file <vocabulary.txt> is a TSV file and it is organized with
        one term per line:
        termnumber <TAB> term

    :param bow: bag of words return from algorithmBoW
    :param directory: '/Index' directory created by makeDirectory(*,'Index')
                      function
    """

    words = [bow[i][j] for i in range(len(bow)) for j in range(len(bow[i]))]
    words_sort = sorted(set(words))
    key = range(1, len(words_sort)+1)
    vocabulary = pd.DataFrame({'key': key, 'term': words_sort})
    vocabulary.to_csv(directory + '/vocabulary.txt', sep='\t',
                      header=False, index=False)


def makePostings(bow, directory):
    """
    Return the posting.txt file
    The file is a TSV file and it is organized with one term per line:
        termnumber <TAB> document1 <TAB> document2 <TAB> ...'\n'

    :param bow: bag of words return from algorithmBoW
    :param directory: '/Index' directory created by makeDirectory(*,'Index')
                      function
    """
    postings = {}
    words_doc = \
        [(bow[i][j], i+1) for i in range(len(bow)) for j in range(len(bow[i]))]
    for k, d in words_doc:
        postings.setdefault(k, []).append(d)
    with open(directory+'/postings.txt', 'w') as p:
        for key in sorted(postings.iterkeys()):
            p.write(str(key)+'\t'+'\t'.join(map(str, postings[key]))+'\n')


if __name__ == "__main__":
    bow = algorithmBoW(os.getcwd()+'/documents')
    directory = 'index'
    index_dir = makeDirectory(os.getcwd(), directory)
    makeVocabulary(bow, index_dir)
    makePostings(bow, index_dir)
