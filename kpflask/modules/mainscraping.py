import random
import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from numpy import array

def webdriverConfigUseProxy(proxy,ipProxy,portProxy,user_agent):
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

def webdriverConfig(user_agent):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)
    profile.update_preferences()
    options = webdriver.FirefoxOptions()
    options.add_argument('--private')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    return webdriver.Firefox(firefox_profile=profile,options=options)

# Rotating User Agent
acak = random.randint(0, 6)
user_agent = 'Firefox/7{}.0 ( Win64; x64; Linux x86_64) Chrome/75.0.3770.142 Safari/537.36'.format(acak)

# memakai 2 driver supaya pencarian proxy menjadi lebih cepat
driverProxyssl = webdriverConfig(user_agent)
driverProxy = webdriverConfig(user_agent)

proxy = Proxy(driverProxyssl,driverProxy)
dataProxy = proxy.generateDataProxy()
dataProxy=None
if dataProxy != None:
    dataProxy=dataProxy.split(":")
    ipProxy,portProxy=dataProxy[0],dataProxy[1]
    
driverLazada = webdriverConfigUseProxy(dataProxy,ipProxy,portProxy,user_agent)
driverTokopedia = webdriverConfigUseProxy(dataProxy,ipProxy,portProxy,user_agent)
driverBukalapak = webdriverConfigUseProxy(dataProxy,ipProxy,portProxy,user_agent)

linkTool="lampu led"
linkTool=linkTool.replace(" ", "+")
batas=10

try:
    bukalapak = Bukalapak(linkTool,driverBukalapak,batas)
    dataBukalapak= bukalapak.generateDataset()
except:
    dataBukalapak= ["Connection Error"]
    pass

try:
    tokopedia = Tokopedia(linkTool,driverTokopedia,batas)
    dataTokopedia= tokopedia.generateDataset()
except BaseException as e:
    print(e)
    dataTokopedia= ["Connection Error"]
    pass

try:
    lazada = Lazada(linkTool,driverLazada,batas)
    dataLazada= lazada.generateDataset()
except:
    dataLazada= ["Connection Error"]
    pass
driverBukalapak.quit()
driverLazada.quit()
driverTokopedia.quit()