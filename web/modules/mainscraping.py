import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from numpy import array

from modules.tokopedia import *
from modules.proxy import *
from modules.lazada import *
from modules.bukalapak import *

class MainScraping:
    statusproxy=""
    productname=""
    def __init__(self,statusproxy,productname):
        self.statusproxy=statusproxy
        self.productname=productname

    def __webdriverConfigUseProxy(self,proxy,ipProxy,portProxy,user_agent):
        profile = webdriver.FirefoxProfile()
        if proxy != None:
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http",ipProxy)
            profile.set_preference("network.proxy.http_port",int(portProxy))
            profile.set_preference("network.proxy.https",ipProxy)
            profile.set_preference("network.proxy.https_port",int(portProxy))
            profile.set_preference("network.proxy.ssl",ipProxy)
            profile.set_preference("network.proxy.ssl_port",int(portProxy))
            profile.set_preference("network.proxy.socks",ipProxy)
            profile.set_preference("network.proxy.socks_port",int(portProxy))
            profile.set_preference("general.useragent.override", user_agent)
            profile.update_preferences()
        options = webdriver.FirefoxOptions()
        options.add_argument('--private')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        return webdriver.Firefox(firefox_profile=profile,options=options)

    def __webdriverConfig(self,user_agent):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        profile.update_preferences()
        options = webdriver.FirefoxOptions()
        options.add_argument('--private')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        return webdriver.Firefox(firefox_profile=profile,options=options)

    def scrapingWebsite(self):
        # Rotating User Agent
        acak = random.randint(0, 6)
        user_agent = 'Firefox/7{}.0 ( Win64; x64; Linux x86_64) Chrome/75.0.3770.142 Safari/537.36'.format(acak)
        if self.statusproxy == "on":
            # memakai 2 driver supaya pencarian proxy menjadi lebih cepat
            driverProxyssl = self.__webdriverConfig(user_agent)
            driverProxy = self.__webdriverConfig(user_agent)
    
            proxy = Proxy(driverProxyssl,driverProxy)
            dataProxy,ipProxy,portProxy = proxy.generateDataProxy(),None,None
            if dataProxy != None:
                dataProxy=dataProxy.split(":")
                ipProxy,portProxy=dataProxy[0],dataProxy[1]
        else:
            dataProxy,ipProxy,portProxy=None,None,None
        driverLazada = self.__webdriverConfigUseProxy(dataProxy,ipProxy,portProxy,user_agent)
        driverTokopedia = self.__webdriverConfigUseProxy(dataProxy,ipProxy,portProxy,user_agent)
        driverBukalapak = self.__webdriverConfigUseProxy(dataProxy,ipProxy,portProxy,user_agent)

        linkTool=self.productname
        linkTool=linkTool.replace(" ", "+")
        batas=10

        try:
            bukalapak = Bukalapak(linkTool,driverBukalapak,batas)
            dataBukalapak= bukalapak.generateDataset()
            
        except (Exception,NoSuchElementException) as e:
            print(e)
            dataBukalapak= [["#","Connection Error","0",""]]
            pass

        try:
            tokopedia = Tokopedia(linkTool,driverTokopedia,batas)
            dataTokopedia= tokopedia.generateDataset()
        except (Exception,NoSuchElementException)as e:
            print(e)
            dataTokopedia= [["#","Connection Error","0",""]]
            pass

        try:
            lazada = Lazada(linkTool,driverLazada,batas)
            dataLazada= lazada.generateDataset()
        except (Exception,NoSuchElementException) as e:
            print(e)
            dataLazada= [["#","Connection Error","0",""]]
            pass
        driverBukalapak.quit()
        driverLazada.quit()
        driverTokopedia.quit()
        return dataTokopedia,dataLazada,dataBukalapak