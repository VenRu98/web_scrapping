import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from numpy import array
class Proxy:
    driverssl,driver="",""
    def __init__(self,driverssl,driver):
        # buka link
        url1 = "http://spys.one/en/https-ssl-proxy/"
        url2 = "http://spys.one/en/http-proxy-list/"
        driverssl.get(url1)
        driver.get(url2)
        driverssl.implicitly_wait(100)
        driver.implicitly_wait(100)
        self.driverssl,self.driver=driverssl,driver
    
    def __loadMoreData(self,driverPage):
        src = driverPage.find_element_by_id('xpp')
        ActionChains(driverPage).click(src).perform()
        driverPage.execute_script('document.querySelector("#xpp").selectedIndex=4;document.querySelector("#xpp").form.submit()')
        # time.sleep(2)
    
    def __scrapingDataProxy(self,proxy,driverPage):
        count=0
        selectAll = 'document.querySelectorAll("font.spy14")'
        for i in driverPage.execute_script('return ' + selectAll):
            if ':' in i.text:
                speedproxy = driverPage.execute_script('return document.querySelector("body > table:nth-child(3) > tbody > tr:nth-child(5) > td > table > tbody > tr:nth-child({}) > td:nth-child(7) > table").getAttribute("width");'.format(3+count))

                # menambah data proxy ssl dengan filter 'connection speed'
                if int(speedproxy) > 17 :
                    proxy.add(i.text)
                count+=1
        return proxy
    
    def __testProxy(self,proxy):
        proxies=list(proxy)
        random.shuffle(proxies)
        random.shuffle(proxies)
        url="https://api.myip.com"
        for proxy in proxies:
            try:
                response = requests.get(url,proxies={"http": proxy, "https": proxy},timeout=1.5)
                return proxy
            except:
                pass
    
    def generateDataProxy(self):
        driverssl,driver=self.driverssl,self.driver
        self.__loadMoreData(driverssl)
        self.__loadMoreData(driver)
        proxy=set()
        try:
            proxy = self.__scrapingDataProxy(proxy,driverssl)
            proxy = self.__scrapingDataProxy(proxy,driver)
        except:
            return None
        driverssl.quit()
        driver.quit()
        return self.__testProxy(proxy)