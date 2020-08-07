import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from numpy import array
from concurrent.futures import ThreadPoolExecutor

class Bukalapak:
    driver,batas="",0
    def __init__(self,linkTool,driver,batas):
        linkURLBukalapak="https://www.bukalapak.com/products?utf8=%E2%9C%93&search%5Bkeywords%5D={}&search%5Bsort_by%5D=rating_ratio%3Adesc&search%5Bbrand_seller%5D=0&search%5Bnew%5D=0&search%5Bnew%5D=1&search%5Bused%5D=0&search%5Bused%5D=1&search%5Bfree_shipping_coverage%5D=&search%5Bprovince%5D=&search%5Bcity%5D=&search%5Bcourier%5D=&search%5Bprice_min%5D=&search%5Bprice_max%5D=&search%5Brating_gte%5D=1&search%5Brating_lte%5D=5&search%5Btodays_deal%5D=0&search%5Binstallment%5D=0&search%5Bwholesale%5D=0&search%5Btop_seller%5D=0&search%5Bbrand_seller%5D=0".format(linkTool)
        driver.get(linkURLBukalapak)
        driver.execute_script('window.scrollBy(0, 200)')
        self.driver,self.batas=driver,batas
       
    def __waitingPageMain(self):
        driver = self.driver
        for i in range(5):
            driver.execute_script('window.scrollBy(0, 200)')
            driver.execute_script('window.scrollBy(0, -100)')
            time.sleep(.3)
            
    def __getAllNonRating(self):
        driver,batas=self.driver,self.batas
        scrapping=BeautifulSoup( driver.page_source,'lxml')
        if driver.execute_script('return document.querySelector("#product-explorer-container > div > div > div.bl-flex-item.bl-product-list-wrapper > div > div > div > div:nth-child(1) > div > div:nth-child(2) > p.mb-8.bl-text.bl-text--subheading-1")') != None:
            yield "none"
        else:
            # waiting time
            self.__waitingPageMain()
            Semua = scrapping.findAll('div', attrs={'class':'bl-product-card__wrapper'})
            count_data = 0
            arraylink=[]
            for data in Semua:
                if count_data==batas:
                    break
                count_data+=1
                link=data.find('a')['href']
                judul=data.find('a',attrs={'bl-link'})
                harga=data.find('p',attrs={'bl-text bl-text--subheading-2 bl-text--semi-bold bl-text--ellipsis__1'})
                yield [link,judul.text,harga.text.strip()[2:].replace(".","")]

    def __getRating(self,driver):
        scrapping=BeautifulSoup( driver.page_source,'lxml')
        driver.execute_script('window.scrollBy(0, 1000)')
        data=  scrapping.findAll('span', attrs={'class':'u-fg--ash u-inline-block u-mrgn-left--3'})
        if len(data)==1:
            return ['0', '0', '0', '0', '0']
        else:
            if data == []:
                data=  scrapping.findAll('div', attrs={'class':'list-item__percentage'})
                try:
                    totalRating = driver.execute_script('return document.querySelector("#section-main-product > div.c-product-details-section__main > div.c-main-product__head > div.c-main-product__head--left > div > div").textContent')
                except:
                    return ['0', '0', '0', '0', '0']
                totalRating = int( totalRating.split()[0].replace(".","") )
                for i in range (5):
                    hasil = driver.execute_script('return document.querySelector("#section-ulasan-barang > div.c-product-details-section__main > div > div.c-reviews__header > div.c-reviews__summary.section-main-content > div.c-reviews__summary-list.c-reviews__summary-list--filtered > div:nth-child({}) > div.list-item__percentage").textContent'.format(i+1)) 
                    hasil = hasil[:-1] if hasil[:-1] != '' else 0
                    hasil = int(float(hasil))
                    rating = (hasil * totalRating) // 100
                    yield rating
            else:
                for i in data:
                    yield i.text

    def generateDataset(self):
        driver,batas=self.driver,self.batas
        if 'Attention Required' in BeautifulSoup( driver.page_source,'lxml').find('title').text:
            return [["#","Access Denied","0",""]]
        dataNonRating=list(self.__getAllNonRating())
        if dataNonRating == []:
            return [["#","The HTML attribute has changed","0",""]]
        elif dataNonRating == ['none']:
            return [["#","Not Found","0",""]]
        dataLink=array(dataNonRating)
        futures = []
        with ThreadPoolExecutor(max_workers=5) as ex:
            for link in dataLink[:,0]:
                futures.append(ex.submit(self.__getContent,link))

        for num,future in enumerate(futures):
            dataNonRating[num].append(future.result())
        return dataNonRating
    
        for num,link in enumerate(list(dataLink[:,0])) :
            driver = self.__driver()
            driver.get(link)
            dataNonRating[num].append(list(self.__getRating(driver)))
            driver.quit()
        return dataNonRating
    
    def __getContent(self,link):
        driver = self.__driver()
        driver.get(link)
        hasil = list(self.__getRating(driver))
        driver.quit()
        return hasil
    
    def __driver(self):
        acak = random.randint(0, 6)
        user_agent = 'Firefox/7{}.0 ( Win64; x64; Linux x86_64) Chrome/75.0.3770.142 Safari/537.36'.format(acak)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        profile.update_preferences()
        options = webdriver.FirefoxOptions()
        options.add_argument('--private')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        return webdriver.Firefox(firefox_profile=profile,options=options)