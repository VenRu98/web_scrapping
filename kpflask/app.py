# import library
import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from numpy import array

from flask import Flask, render_template, request,redirect,url_for
from modules.mainscraping import *

app=Flask(__name__,template_folder='page')



@app.route('/',methods=['GET','POST'])
def home():
  dataTokopedia,dataLazada,dataBukalapak,selectProxy=None,None,None,"off"
  selectProxy="off"
  if request.method == 'POST':
    produk=request.form['produk']
    selectProxy = request.form['inlineRadioOptions']

    scraping = MainScraping(selectProxy,produk)
    dataTokopedia,dataLazada,dataBukalapak = scraping.scrapingWebsite()

    return render_template('index.html',produk=produk,proxy=selectProxy,dataTokopedia=dataTokopedia,dataBukalapak=dataBukalapak,dataLazada=dataLazada)
  return render_template('index.html',proxy=selectProxy,dataTokopedia=dataTokopedia,dataBukalapak=dataBukalapak,dataLazada=dataLazada)

@app.route('/about',methods=['GET'])
def about():
  return render_template('about.html')

if __name__ == "__main__":
  
  app.run()

