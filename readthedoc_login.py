#coding:utf-8

import os
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options


def webdriver_env_setup():
    #chrome path error solution (II)
    # os.environ["webdriver.chrome.driver"] = "e:\Computer\virtualenv\webscrapping\chrome\chromedriver.exe"
    # driver = webdriver.Chrome()
    #OR
    driver = webdriver.Chrome(r'e:\Computer\virtualenv\webscrapping\chrome\chromedriver.exe')

    return driver

def login(browser,loginurl):
    browser.get(loginurl)  
    time.sleep(1)

    username = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='id_login']")))
    username.clear()
    username.send_keys("hebinn@163.com")   
    print("name sent")
    time.sleep(1)
    
    # browser.execute_script("document.getElementById('id_password').setAttribute('class', 'form-control')") #purpose?
    password = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='id_password']")))
    password.clear()
    password.send_keys("steer101214")    
    browser.execute_script("document.getElementById('id_password').disabled=false") #purpose?
    print("password sent")
	
    sign = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='primaryAction']")))
    print(sign.text)
    sign.send_keys(u"登录")
    sign.click()
    print("sign sent")
    time.sleep(1)

def go_to_next_page(browser):
    next = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//a[@rel='next']")))
    next.click()    
	
browser = webdriver_env_setup()	
loginurl = 'https://readthedocs.org/accounts/login/'
targeturl = 'https://docs.readthedocs.io/en/latest/getting_started.html'  

login(browser,loginurl)

browser.get(targeturl) 

go_to_next_page(browser)

