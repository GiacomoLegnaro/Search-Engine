#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Short summary that describe what the algorithm does
"""


import os
import re
from collections import OrderedDict
from Index import SnowballStemmer
from Index import Stemming

__author__ = 'Giacomo Legnaro'
__version__ = '0.0'
__email__ = 'g.legnaro@gmail.com'
__status__ = 'Production'
__date__ = 'August 1st, 2016'
__studentID__ = '1724522'


def loadPostings(postings_file):
    """
    Return the postings dictionary from a text file.

    :param postings_file: name of the file to be loaded
    """
    with open(postings_file) as p:
        term = [l.strip().split('\t') for l in p]
    postings = OrderedDict()
    for t in term:
        postings.update({t[0]: t[1:]})
    return postings


def mapOfTerms(vocabulary_file, postings):
    """
    Return the map of terms from file <vocabulary.txt>.

    :param vocabulary_file: name of the file to be loaded
    :param postings: postings dictionaries from loadPostings function
    """
    with open(vocabulary_file, 'r+') as v:
        term = [l.strip().split('\t') for l in v]
    vocabulary = OrderedDict()
    for t in term:
        vocabulary.update({t[0]: t[1]})
    mot = OrderedDict(zip(vocabulary.values(), postings.values()))
    return mot


def answerQuery(query_stem, mot):
    """
    Return no. of documents which have the query's words

    :param query_stem: query stemmed
    :param mot: map of terms return from relative function
    """
    if len(query_stem) == 0:
        return None
    query_find = [q for q in query_stem if q in mot]
    # Find out if all the words are mapped from the documents
    if len(query_find) != len(query_stem):
        # We must return the documents that contain ALL the terms
        return None
    else:
        list_doc = [mot[query_stem[i]] for i in range(len(query_stem))]
        # list of all the document for each words
        return intersectionAlgorithm(list_doc)


def intersectionAlgorithm(list_doc):
    """
    Return identifier of the documents which have ALL the query's words

    :param list_docs: list of the documents which contains at least one of the
                      query_stem words
    """
    if len(list_doc) == 1:
        return list_doc[0]
    else:
        doc_id = sorted(set([int(list_doc[i][j]) for i in range(len(list_doc))
                        for j in range(len(list_doc[i]))]))
        doc_values = [0 for i in range(len(doc_id))]
        ranking = OrderedDict(zip(doc_id, doc_values))
        for i in range(len(list_doc)):
            unique_doc = set(list_doc[i])
            for j in unique_doc:
                ranking[int(j)] += 1
        rank_dict = dict(ranking)
        intersected = [rank_dict.keys()[i] for i in range(len(rank_dict))
                       if rank_dict.values()[i] == len(list_doc)]
    return intersected


def answerToUser(directory, answer_query):
    """
    Graphical interface with the user to print out the result of the query.

    :param directory: directory with the entire dataset of documents
    :param answer_query: list of the documents with ALL the terms query
    """
    if len(answer_query) == 0:
        print 'No one advertisement correspond to your request. Sorry'
    else:
        sub_dir_sort = sorted(os.listdir(directory))
        if '.DS_Store' in sub_dir_sort:
            sub_dir_sort.remove('.DS_Store')
        folder_id = map(lambda x: int(x)/501, answer_query)
        for i in range(len(answer_query)):
            lb = 500*folder_id[i]+1
            ub = 500*(folder_id[i]+1)
            with open(
                os.path.join(
                    directory, (
                    'documents-'
                    + str(0) * (6-len(str(lb))) + str(lb)
                    + '-'
                    + str(0) * (6-len(str(ub))) + str(ub)),
                    'document-'
                    + str(0) * (6-len(str(answer_query[i])))
                    + str(answer_query[i])),
                    'r+') as document:
                terms = document.read().split('\t')
                # print '\n'.join(terms[0:4]), '\n\n'
                print 'Title: %s ' % terms[0]
                print 'Location: %s ' % terms[1]
                print 'Price: %s ' % terms[2]
                print 'URL: %s ' % terms[3]
                # print 'Description: %s ' % terms[4]
                print '\t\t\t-------\t\t\t-------\t\t\t-------\n\n'


if __name__ == "__main__":
    # Create in memory the posting lists and a map of terms
    loaded_postings = loadPostings('index/postings.txt')
    map_terms = mapOfTerms('index/vocabulary.txt', loaded_postings)

    # ASk to user which terms would you search
    query_usr = raw_input('Terms you would search: ').decode('utf-8')

    # Preprocessed query terms
    stemmer_snow = SnowballStemmer('italian')
    query_stemmed = Stemming(query_usr, stemmer_snow)

    # Find out the identifier of the document that have at least one term
    print query_stemmed
    # print map_terms
    list_doc = answerQuery(query_stemmed, map_terms)
    if list_doc is not None:
        answerToUser('documents', list_doc)
        # Print the title, the location, the price and the URL of the ads
        # that satisfies all query term
    else:
        print 'No ads satisfy your request.'
