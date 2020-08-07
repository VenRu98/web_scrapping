import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from numpy import array
from concurrent.futures import ThreadPoolExecutor

class Tokopedia:
    batas,driver="",""
    def __init__(self,linkTool,driver,batas):
        linkURLTokopedia="https://www.tokopedia.com/search?st=product&rt=4%2C5&q="
        driver.get(linkURLTokopedia+linkTool)
        driver.execute_script('window.scrollBy(0, 200)')
        self.driver,self.batas=driver,batas
        
    def __waitingPageRating(self,driver):
        script = 'document.querySelector("#zeus-root > div > div.css-1jdotmr > div:nth-child(5) > div.css-drikti.e1ufc1ph1 > div.css-nvt3av.e1ufc1ph0 > div > div:nth-child(1) > div.css-udfbf8.e1ufc1ph0 > p")'
        while(driver.execute_script('return '+script) == None ):
            # Untuk trigger supaya page dapat loading
            driver.execute_script('window.scrollBy(0, 200)')
            driver.execute_script('window.scrollBy(0, -100)')
            time.sleep(.3)
            
    def __waitingPageMain(self,pos):
        driver=self.driver
        script='document.querySelector("#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div.css-jza1fo > div:nth-child({})")'.format(pos)
        count = 0
        while(driver.execute_script('return '+script) == None ):
            # memeriksa UI berubah atau tidak
            if(count==30):
                return "ui"
            count+=1
            # Untuk trigger supaya page dapat loading
            driver.execute_script('window.scrollBy(0, 100)')
            time.sleep(.3)
            # memeriksa apakah barangnya ada atau tidak
            if driver.execute_script('return document.querySelector("#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div.css-109jhir > div > div.css-v7ibj3 > div.css-lu7a1o")') != None:
                return "none"
        return "complete"
            
    def __getAllNonRating(self):
        batas,driver=self.batas,self.driver
        # waiting time
        wait= self.__waitingPageMain(batas-1)
        if (wait != 'complete'):
            yield wait
        else:
            scrapping=BeautifulSoup(driver.page_source,'lxml')
            Semua = scrapping.findAll('div', attrs={'class':'css-1g20a2m'})
            count_data = 0
            arraylink=[]
            for data in Semua:
                if count_data==batas:
                    break
                count_data+=1
                link = data.find('a')['href']
                judul = data.find('span',attrs={'css-1bjwylw'})
                harga = data.find('span',attrs={'css-o5uqvq'})
                yield [link,judul.text,harga.text[3:].replace(".","")]

    def __getRating(self,driver):
        for i in range(5):
            script = 'document.querySelector("#zeus-root > div > div.css-1jdotmr > div:nth-child(5) > div.css-drikti.e1ufc1ph1 > div.css-nvt3av.e1ufc1ph0 > div > div:nth-child({}) > div.css-udfbf8.e1ufc1ph0 > p")'.format(i+1)
            hasil= driver.execute_script('return '+script) 
            yield hasil.text if hasil != None else '0'

    def generateDataset(self):
        driver=self.driver
        if 'Access Denied' in BeautifulSoup( driver.page_source,'lxml').find('title').text:
            return [["#","Access Denied","0",""]]
        dataNonRating=list(self.__getAllNonRating())
        if dataNonRating == ['none']:
            return [["#","Not Found","0",""]]
        elif dataNonRating == ['ui']:
            return [["#","The HTML attribute has changed","0",""]]
        
        dataLink=array(dataNonRating)
        futures = []
        with ThreadPoolExecutor(max_workers=5) as ex:
            for link in dataLink[:,0]:
                futures.append(ex.submit(self.__getContent,link))
        for num,future in enumerate(futures):
            dataNonRating[num].append(future.result())
        return dataNonRating


    def __getContent(self,link):
        driver=self.__driver()
        driver.get(link)
        time.sleep(1)
        if "(" in BeautifulSoup(driver.page_source,'lxml').findAll("span")[0].text:
            self.__waitingPageRating(driver)
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