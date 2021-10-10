# Manasvini Raghunathan, Arunima Mittra
# 10/10/21
# HW5: Web Crawler

import requests
import bs4
import re
from bs4 import BeautifulSoup
from nltk import sent_tokenize


def main():
    URL = 'https://pubmed.ncbi.nlm.nih.gov/12216989/'
    # returns a list of URLs that are relevant to the chosen URL

    urls = []
    web_crawler(URL)
    for url in web_crawler(URL):
        [urls.append(u) for u in web_crawler(url) if u not in urls]

    count = 0
    dict_url = {}
    for u in urls:
        dict_url[count] = u
        count += 1

    # calls function to scrape text off of URLs
    # puts contents in a separate text file page
    web_scraper(dict_url)


# clean text
def clean_text(text):
    lines = text.split(". ")
    listOfClean = []
    for line in lines:
        listOfClean += (sent_tokenize(line))
    return listOfClean


# get list of URLs
def web_crawler(url):
    init_page = requests.get(url)
    soup = BeautifulSoup(init_page.content, 'html.parser')
    urls = []
    data = soup.findAll('a', 'docsum-title')

    # first try-catch gathers links in the same domain
    try:
        for a in data:
            regexp = re.compile(r'[0-9]{6,10}')
            if regexp.search(a.get('href')):
                urls.append('https://pubmed.ncbi.nlm.nih.gov' + a.get('href'))
            else:
                urls.append(a.get('href'))
    except:
        print("Exception occurred for URL", a)

    # get additional links from within the webpage
    outside = soup.findAll('ul', 'linkout-category-links')
    try:
        for obj in outside:
            for a in obj.find_all('a'):
                urls.append(a.get('href'))
    except:
        print("Exception occurred for URL")

    return urls


def web_scraper(dict):
    for key, val in dict.items():
        try:
            page = requests.get(val)
        except:
            continue
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.findAll('div', 'abstract-content selected')
        for post in results:
            try:
                with open(str(key) + '.txt', 'w') as f:
                    f.write(str(post.get_text().encode('utf-8', 'ignore').decode("utf-8")))
                with open(str(key) + '_clean' + '.txt', 'w') as f:
                    lines = clean_text(post.get_text().encode('utf-8', 'ignore').decode("utf-8"))
                    for line in lines:
                        f.write(line)
                        f.write('\n')
            except:
                continue


if __name__ == '__main__':
    main()
