# Manasvini Raghunathan, Arunima Mittra
# 10/10/21
# HW5: Web Crawler

import requests
import re
from bs4 import BeautifulSoup
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords


def main():
    URL = 'https://pubmed.ncbi.nlm.nih.gov/12216989/'
    urls = []

    # returns a list of URLs that are relevant to the chosen URL
    web_crawler(URL)
    for url in web_crawler(URL):
        [urls.append(u) for u in web_crawler(url) if u not in urls]

    # initializes a dict of urls with the keys as the index
    count = 1
    dict_url = {}
    for u in urls:
        dict_url[count] = u
        count += 1

    # calls function to scrape text off of URLs
    # puts contents in a separate text file page
    # web_scraper(dict_url)

    # docs = []
    tf_dicts = []
    for num in range(count):
        try:
            filename = str(num) + '_clean.txt'
            with open(filename, mode='r') as f:
                text = f.read()
                tf_dicts.append(term_frequency(text))
        except:
            continue

    # creates set of unique words from all the docs
    vocab = set(tf_dicts[0].keys())
    for tfd in tf_dicts[1:]:
        vocab = vocab.union(set(tfd.keys()))

    top_words = []
    for word in vocab:
        avg = 0
        for dic in tf_dicts:
            if word in dic:
                avg += dic[word]
            else:
                avg += 0
        top_words.append((word, avg / count))

    top_words.sort(key=lambda y: y[1], reverse=True)
    print(top_words[:11])
    print('number of unique words:', len(vocab))


# clean text
def clean_text(text):
    lines = text.split(". ")
    list_of_clean = []
    for line in lines:
        line = line.strip().lower().replace('\n', ' ').replace('\t', ' ')
        list_of_clean += (sent_tokenize(line))
    return list_of_clean


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


def term_frequency(text):
    stopword = stopwords.words('english')
    tf_dict = {}
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w.isalpha() and w not in stopword]

    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    sorted_dict = {k: v for k, v in sorted(tf_dict.items(), key=lambda item: item[1], reverse=True)}
    return sorted_dict;


if __name__ == '__main__':
    main()
