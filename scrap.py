import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.yelp.com/search?find_desc=&find_loc='
loc = 'San+Francisco%2C+CA&ns=1'
current_page = 0

while current_page < 201:
    url = base_url + loc + "&start=" + str(current_page)

    yelp_r = requests.get(url)

    # print(yelp_r.status_code)

    yelp_soup = BeautifulSoup(yelp_r.text, 'html.parser')

    # print(yelp_soup.prettify())
    # print(yelp_soup.findAll('li', {'class':"regular-search-result"}))

    file_path = 'yelp-{loc}.txt'.format(loc=loc)

    with open(file_path, "a") as textfile:
        businesses = yelp_soup.findAll('div', {'class':"biz-listing-large"})

        for biz in businesses:
            title = biz.findAll('a', {'class':"biz-name"})[0].text
            print(title)
            try:
                address = biz.findAll('address')[0].contents
            except:
                address = None
            print(address)
            if address:
                for item in address:
                    if "br" in str(item):
                        print(item.getText())
                    else:
                        print(item.strip(" \n\t\r"))
            print('\n')
            try:
                phone = biz.findAll('span', {'class':"biz-phone"})[0].text
            except:
                phone = None
            print(phone)
            page_line = "{title}\n{address}\n{phone}\n\n".format(
                title=title,
                address=address,
                phone=phone,
            )
            textfile.write(page_line)
    current_page += 10
