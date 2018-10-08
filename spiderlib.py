# -*- coding:utf-8 -*-

import urllib2
from selenium import webdriver
import subprocess, os, time
from xlsxwriter import Workbook
from threading import Thread
import shutil

import requests

def now_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return current_time+': '


def chrome(path="e:\Computer\virtualenv\pyspider\src\chromedriver.exe", headless=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    if headless is True:
        chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
    driver = webdriver.Chrome(r"e:\Computer\virtualenv\webscrapping\chrome\chromedriver.exe", chrome_options=chrome_options)
    return driver


def firefox_browser(download_path=""):
    username = subprocess.check_output(['whoami']).strip()
    if username == "root":
        default_files_path = "/root/.mozilla/firefox/"
    else:
        default_files_path = "/home/%s/.mozilla/firefox/"% username

    files = os.listdir(default_files_path)
    for f in files:
        if ".default" in f:
            firefox_default_file = default_files_path + f
            break
    #print firefox_default_file
    profile = webdriver.FirefoxProfile(firefox_default_file)
    profile.set_preference("extensions.firebug.allPagesActivation", "on")
    profile.set_preference("permissions.default.image", 2)

    if download_path !="":
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", download_path)
        profile.set_preference('browser.download.manager.showWhenStarting', False)

        application = '''application/zip,text/plain,application/vnd.ms-excel,text/csv,text/comma-separated-values,
        application/octet-stream,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,
        application/vnd.openxmlformats-officedocument.wordprocessingml.document'''

        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', application)
    driver = webdriver.Firefox(profile,executable_path="/root/homework/common/geckodriver")

    return driver

proxies = {
  # "https": "http://135.245.48.34:8000"
}

def web_static(url):

    '''
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,' \
                 'like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    headers = {'User-Agent': user_agent}
    '''
    
    try:
        # https://images-na.ssl-images-amazon.com/images/I/51ukRWG-WFL._AC_US200_.jpg
        
        return requests.get(url, proxies=proxies, stream=True)
        
        '''
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        return response.read()
        '''
    except Exception as e:
        print "web_static :: url request get failure {} for url {}".format(e, url)
        return False


def saveImg_sub(name, url, path):
    # print("saveImg_sub...........\n")
    img = web_static(url.strip())
    try:        
        with open(name, 'wb') as p:
            # p.write(img)
            shutil.copyfileobj(img.raw, p)
            del img
    except:
        print now_time(), "save image failure: %s %s" % (url, path)
        img = os.path.join(path,"downloadfailure.jpg")
        os.system('cp  %s  %s' % (img, name))


def saveImg(product_pic_url, path):
    # print("saveImg.............\n")
    pics_path = []
    len_lst = len(product_pic_url)
    for pic_url in product_pic_url:
        len_lst -= 1
        name = os.path.join(path, pic_url.split('/')[-1])
        pics_path.append(name)
        if os.path.exists(name):
            continue
        t = Thread(target=saveImg_sub,args=(name, pic_url, path))
        t.start()

    return pics_path


def create_dir(dname, path):
    try:
        if u'\u2013' in dname:
            dname = str(dname.replace(u'\u2013', ''))
        if u'"' in dname:
            dname = str(dname.replace(u'"', ''))
        dir_name = path + dname
        if os.path.exists(u"%s" % dir_name) is False:
            os.makedirs(u"%s" % dir_name)
        return dir_name
    except:
        print "create dir {} failure {}".format(path + dname, now_time(), )


def write_data_excel(data1, data2, path):
    # print ('data1:', data1)
    # print ('data2:', data2)
    name = path.split('/')[-1]
    create_time = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
    pure_name = '%s_%s.xlsx' % (name, create_time)
    file_name = os.path.join(path , pure_name)
    # print("file_name:", file_name)
    new_f = Workbook(file_name)
    sheet1 = new_f.add_worksheet(create_time)
    sheet1_format = new_f.add_format({})
    sheet1_format.set_text_wrap()
    sheet1.set_column(0, 0, 25)
    sheet1.set_column(1, 4, 60)
    for i in range(len(data1)):
        if i:
            sheet1.set_row(i, 125)
            print "start to insert image {}".format(data2[i])
            sheet1.insert_image(i, 0, data2[i])
        for j in range(len(data1[i])):
            if i == 0:
                sheet1.set_row(0, 18)
                headers = ['PRODUCE NAME', 'PRODUCE PRICE', 'THE LINK']
                sheet1.write(0, j + 1, headers[j])
            else:
                try:
                    sheet1.write(i, (j + 1), data1[i][j], sheet1_format)
                except:
                    pass
    new_f.close()

    return file_name

