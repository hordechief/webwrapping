# -*- coding:utf-8 -*-


import os,sys, subprocess
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append('/root/homework/')
from time import sleep
from spiderlib import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media")

class amazon_dynamic():
    def __init__(self, result_path, img_path):
        self.result_path = result_path
        self.img_path = img_path
        self.driver = chrome(path="e:\Computer\virtualenv\webscrapping\chrome\chromedriver.exe", headless=True)
        self.next_page_flag = ""

#open the web pages
    def open_web(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "pagnNextString")))
        except:
            print "open the first page failure"

# search the elements, e.g. production name , href, picture and so on
    def get_info(self, max_num_to_extract):
        # extacted result
        product_pic_url_lst = []
        product_info_lst = []

        # find the product infor
        while True:
            info_of_all = self.driver.find_elements_by_xpath('//ul[@id="s-results-list-atf"]/li')
            if len(info_of_all) >= max_num_to_extract:
                break
            sleep(1)

        # get the specific information
        for info in info_of_all[0:10]:
            li_ID = info.get_attribute('id')

            try:
                product_pic = self.driver.find_element_by_xpath(
                    '//li[@id="%s"]//img[@class="s-access-image cfMarker"]' % li_ID)
                # product_infos = self.driver.find_element_by_xpath('//li[@id="%s"]//div[3]/div[1]/a' % li_ID)
                product_infos = self.driver.find_element_by_xpath('//li[@id="%s"]//div[1]/div[3]/div[1]/a' % li_ID)
                # product_price = self.driver.find_elements_by_xpath('//li[@id="%s"]//div[3]/div[2]/a/span' % li_ID)
                product_price = self.driver.find_elements_by_xpath('//li[@id="%s"]//div[1]/div[3]/div[3]/a/span[@class="a-offscreen"]' % li_ID)
            except Exception as e:
                # print "get_info error {}".format(e.message)
                print "get_info error {}".format(e)
                continue

            # src
            pic_url = product_pic.get_attribute('src')
            # title
            product_name = product_infos.get_attribute('title')
            # href
            product_url = product_infos.get_attribute('href')

            # price
            if len(product_price) == 1:
                product_price = product_price[0].get_attribute('aria-label')
            elif len(product_price) >= 2:
                product_price = product_price[1].text
            else:
                product_price = "No price"

            # save to list
            if pic_url and product_name and product_url:
                product_pic_url_lst.append(pic_url)
                product_info_lst.append([product_name, product_price, product_url])
            else:
                print now_time(),"%s \n %s" % (product_name, product_url)
                print now_time(), "ERROR:couldn't get all information of it, and will skip"

        print "{} get info requst len of product {} {}".format(now_time(), len(product_info_lst), len(product_pic_url_lst))
        return product_info_lst, product_pic_url_lst

# click the next page
    def next_page(self):
        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "pagnNextString")))
            self.driver.find_element_by_xpath('//span[@class="srSprite pagnNextArrow"]').click()
        except:
            print "open the next page failure %s" %self.driver.current_url

#close the brower
    def page_close(self):
        self.driver.close()

    # counter : page number
    def start(self, start_url,counter):
        product_lst = []
        pics_lst = []
        
        print now_time(), "Starting to collect the information .........."
        self.open_web(start_url)

        item_num = 24
        # loop each page
        for t in range(counter):
            # url for currrent page
            current_url = self.driver.current_url
            print "{} start to navigate on page {} at url {}".format(now_time(), t, current_url)
            
            # get information from page and return data list
            tmp_product_lst, tmp_pics_url_lst = self.get_info(item_num)
            # tmp_product_lst = [u'https://images-na.ssl-images-amazon.com/images/I/51rnUgglnKL._AC_US200_.jpg']
            # tmp_pics_url_lst = 'E:\Computer\virtualenv\pyspider\..\media\amazon_bedroom_img'
            
            # print(tmp_product_lst, tmp_pics_url_lst)

            # go to next page
            if t <(counter-1):
                self.next_page()

            #save image file to disk
            # print(tmp_pics_url_lst, self.img_path)
            tmp_pics_path = saveImg(tmp_pics_url_lst, self.img_path)
            product_lst.extend(tmp_product_lst)
            pics_lst.extend(tmp_pics_path)
            # print now_time(), len(product_lst), len(pics_lst)

        # save information to excel file
        result_file = write_data_excel(product_lst, pics_lst, self.result_path)
        print now_time(), "upload the result to BAIDU CLOUD"
        # subprocess.call(['bypy', 'upload', str(result_file), "/upload/to/"])

if __name__ == "__main__":

    livingroom_url = "https://www.amazon.com/s/ref=sr_il_ti_garden?rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063306%2Cn%3A1063318%2Cn%3A3733481&sort=featured-rank&ie=UTF8&qid=1505050036&lo=garden"
    bedroom_url = "https://www.amazon.com/s/ref=sr_il_ti_garden?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063306%2Cn%3A1063308&bbn=1063306&sort=featured-rank&ie=UTF8&qid=1505050154&lo=garden"
    #bestseller_url = "https://www.amazon.com/Best-Sellers-Home-Kitchen-Furniture/zgbs/home-garden/1063306/ref=zg_bs_unv_hg_2_3248802011_4"

    # web_site = {'amazon_livingroom': [livingroom_url,200], 'amazon_bedroom': [bedroom_url,400],
    #             'bestseller': [bestseller_url,5]}
    web_site = {'amazon_bedroom': [bedroom_url,1]}

    for key in web_site.keys():
        # create file path for the scrappting files
        result_path = "%s/%s_result" % (static_path, key)
        img_path = "%s/%s_img"% (static_path, key)
        # print(result_path, img_path)
        
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        if not os.path.exists(img_path):
            os.makedirs(img_path)
            # set default picture
            # os.system('cp /root/log/sample.jpg %s/downloadfailure.jpg'%img_path)

        # class initialization
        start_down = amazon_dynamic(result_path, img_path)        

        try:
            # start scrap
            start_down.start(web_site[key][0], web_site[key][1])
            print now_time() + "complete!!"
        finally:
            start_down.page_close()