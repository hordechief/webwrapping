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

'''
print(yelp_soup.findAll('a', {'class':"biz-name"}))

for name in yelp_soup.findAll('a', {'class':"biz-name"}):
   print(name.text)
'''

'''
businesses = yelp_soup.findAll('div', {'class':"biz-listing-large"})

for biz in businesses:
    title = biz.findAll('a', {'class':"biz-name"})[0].text
    print(title)
    address = biz.findAll('address')[0].text
    print(address)
    print('\n')
    phone = biz.findAll('span', {'class':"biz-phone"})[0].text
    print(phone)
'''

file_path = 'yelp-{loc}.txt'.format(loc=loc)

with open(file_path, "a") as textfile:
    businesses = yelp_soup.findAll('div', {'class':"biz-listing-large"})

    for biz in businesses:
        title = biz.findAll('a', {'class':"biz-name"})[0].text
        print(title)
        address = biz.findAll('address')[0].text
        print(address)
        print('\n')
        phone = biz.findAll('span', {'class':"biz-phone"})[0].text
        print(phone)
        page_line = "{title}\n{address}\n{phone}\n\n".format(
            title=title,
            address=address,
            phone=phone,
        )
        textfile.write(page_line)
