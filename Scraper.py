import requests
from bs4 import BeautifulSoup

URL = 'https://www.cnn.com/2021/10/06/us/zodiac-killer-identity-law-enforcement-investigation/index.html'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
text = soup.get_text()
print(text)

for p in soup.select('p'):
    print(p.get_text())

results = soup.findAll('div', {'zn-body__paragraph'})
for post in results:
    print(post.get_text())