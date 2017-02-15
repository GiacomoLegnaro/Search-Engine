#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Short summary that describe what the algorithm does
"""

import requests
import time
import os
from bs4 import BeautifulSoup
import os.path
import os
os.chdir('/Users/giacomolegnaro/Documents/'
         'Data Science/1st Year/1st Semester/'
         'Algorithmic Methods of Data Mining and Laboratory/'
         'Project 1')


__author__ = 'Giacomo Legnaro'
__version__ = '0.0'
__email__ = 'g.legnaro@gmail.com'
__status__ = 'Production'
__date__ = 'August 1st, 2016'
__studentID__ = '1724522'


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


def webSitesDict(website):
    """
    Return sites where do web scraping

    :param website: file contain the link
    """
    websites_list = [row for row in open(website, 'r+')]
    websites = [ws for ws in websites_list]
    return websites


def Kijiji(website, page, path):
    """
    Return the ads and store for each announcement the title, location,
    price, description and the url of the full ad.

    :param website: website main url
    :param page: which page of the website i want to download
    :param nodocdir: number of documents for each directory (ordered)
    :param path: where store the ads
    :param delay: time to wait between two requests to prevent scrap block
    """
    # website = 'http://www.kijiji.it/case/vendita/annunci-roma/'
    # page=1
    global ct
    if page is 1:
        urlpage = ''
    else:
        urlpage = '?p=' + str(page)
    r = requests.get(website + urlpage)
    source_code = r.content
    soup = BeautifulSoup(source_code, "html.parser")
    # Python library for pulling data out of HTML and XML files
    items = soup.find_all('li', {"class": "item result"})
    # cta = Call To Action
    # extract the links of each ad in the page
    for item in items:
        title = item.find(
            'h3', {'class': 'title'}).string.strip().encode('utf-8')
        location = item.find(
            'p', {'class': 'locale'}).string.strip().encode('utf-8')
        price = item.find(
            'h4', {'class': 'price'}).string.strip().encode('utf-8')
        description = item.find(
            'p', {'class': 'description'}).string.strip().encode('utf-8')
        url = item.find('a')['href'].strip().encode('utf-8')
        ad = '%s\t%s\t%s\t%s\t%s' % (title, location, price, url, description)
        lb = 500*(ct/501)+1
        ub = 500*((ct/501)+1)
        with open(
            os.path.join(path, (
                'documents/documents-'
                + str(0) * (6-len(str(lb))) + str(lb)
                + '-'
                + str(0) * (6-len(str(ub))) + str(ub)),
                'document-'
                + str(0) * (6-len(str(ct))) + str(ct)), 'w') as f:
            f.write(ad)
        # time.sleep(delay)
        ct += 1


def selPageKijiji(website, path, all=True, init_page=1, end_page=1,
                  nodocdir=500, delay=2):
    """
    Return the ads and store for each announcement the title, location,
    price, description and the url of the full ad.
    [This is done to all pages between init_page and end_page]

    :param init_page: initial scraping page
    :param end_page: end scraping page
    :param all: Boolean to modify initial and end pages to all range available
    :param website: website main url
    :param nodocdir: number of documents for each directory (ordered)
    :param path: where store the ads
    :param delay: time to wait between two requests to prevent scrap block
    """
    global ct
    ovf_kijiji = 3334
    r = requests.get(website)
    source_code = r.content
    soup = BeautifulSoup(source_code, "html.parser")

    # if all:
    init_page = 1
    end_page = min(
        int(soup.find('a', {'class': 'last-page'}).string), ovf_kijiji)
    s = soup.find(
        'script', {'class': 'gtm'}).string.strip().encode('utf-8')
    start = s.find('"tr":') + 5
    end = s.find(',', start)
    noresults = min(
        int(s[start:end]), (ovf_kijiji * (end_page-init_page+1)))
    # else:
    # s = soup.find(
    #     'script', {'class': 'gtm'}).string.strip().encode('utf-8')
    # start = s.find('"ps":') + 5
    # end = s.find(',', start)
    # noresults = int(s[start:end]) * (end_page - init_page + 1)
    # The next for cycle it is done to reduce the computation time
    # to search at every time the presence of the path
    for i in range((noresults/500)+1):
        lb = 500*i + 1
        ub = 500*(i + 1)
        makeDirectory(path, (
            'documents/documents-'
            + str(0) * (6-len(str(lb))) + str(lb)
            + '-'
            + str(0) * (6-len(str(ub))) + str(ub)))
    ct = 1
    for i in range(init_page, (end_page+1)):
        Kijiji(website=website, page=i, path=path)
        time.sleep(delay)

if __name__ == "__main__":
    selPageKijiji(
        'http://www.kijiji.it/case/vendita/annunci-roma/', os.getcwd())
