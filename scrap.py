import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.yelp.com/search?find_desc=&find_loc='
loc = 'San+Francisco%2C+CA&ns=1'
page = 10

url = base_url + loc + "&start=" + str(page)


yelp_r = requests.get(url)

print(yelp_r.status_code)
# print(type(yelp_r))
# print(yelp_r.text)

yelp_soup = BeautifulSoup(yelp_r.text, 'html.parser')

# print(yelp_soup.prettify())
# print(yelp_soup.findAll('li', {'class':"regular-search-result"}))

# print(yelp_soup.findAll('a', {'class':"biz-name"}))

for name in yelp_soup.findAll('a', {'class':"biz-name"}):
   print(name.text)
    