import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import shutil
import time

url = "http://www.chrisburkard.com/"

web_r = requests.get(url)
web_soup = BeautifulSoup(web_r.text, 'html.parser')
# print(web_soup)
print(web_soup.findAll("img"))

# import os
# os.environ['webdriver.firefox.driver'] = "e:\Computer\virtualenv\webscrapping\Firefox\geckodriver.exe"
# driver = webdriver.Firefox()

driver = webdriver.Firefox(executable_path = r"e:\Computer\virtualenv\webscrapping\Firefox\geckodriver.exe")
driver.get(url)

iter = 0
while iter < 10:
    html = driver.execute_script("return document.documentElement.outerHTML")
    # print(html)
    sel_soup = BeautifulSoup(html, 'html.parser')
    # print(sel_soup.findAll("img"))

    images = []
    for i in sel_soup.findAll("img"):
        print(type(i))
        # print(dir(i))    
        src = i["src"]
        images.append(src)
    print(images)

    current_path = os.getcwd()
    for img in images:
        try:
            file_name = os.path.basename(img)
            img_r = requests.get(img, stream=True)
            new_path = os.path.join(current_path, "images", file_name)
            with open(new_path, "wb") as output_file:
                shutil.copyfileobj(img_r.raw, output_file)
            del img_r
        except:
            pass
    iter += 1
    time.sleep(5)
    
driver.quit()

# print(help(webdriver.Firefox)) # 这样就知道传什么参数