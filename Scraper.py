# Manasvini Raghunathan, Arunima Mittra
# 10/10/21
# HW5: Web Crawler

import requests
import bs4
import re
from bs4 import BeautifulSoup


def main():
    URL = 'https://pubmed.ncbi.nlm.nih.gov/26057783/'
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


# save files
def store_file(text, name):
    with open(str(name) + '.txt', 'w', encoding="utf-8") as f:
        f.write(str(text))


# clean text
def clean_text(text):
    text = ' '.join(w for w in text.split() if w.isalnum() and w != '\n' and w != '\t')
    return text


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
        print("Exception occured for URL", a)

    # get additional links from within the webpage
    outside = soup.findAll('ul', 'linkout-category-links')
    try:
        for obj in outside:
            for a in obj.find_all('a'):
                urls.append(a.get('href'))
    except:
        print("Exception occured for URL")

    return urls


def web_scraper(dict):
    for key, val in dict.items():
        try:
            page = requests.get(val)
        except:
            print("Error for " + val)
            continue
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.findAll('div', 'abstract')
        if len(results) == 0:
            results = soup.findAll('p')
        text = post.get_text()
        print(len(text.strip()), ":", val)
        for post in results:
            if len(text.strip()) > 15:
                store_file(post.get_text(), str(key))
                store_file(clean_text(post.get_text()), str(key) + "_clean")


if __name__ == '__main__':
    main()
