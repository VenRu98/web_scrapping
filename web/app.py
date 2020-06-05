# import library
import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from numpy import array

from flask import Flask, render_template, request,session,jsonify
from modules.mainscraping import *

app=Flask(__name__,template_folder='page')
app.secret_key = "1772026 Steven Rumanto"
# variable global
dataTokopedia,dataLazada,dataBukalapak,selectProxy=None,None,None,"off"

@app.route('/',methods=['GET','POST'])
def home():
  global dataTokopedia,dataLazada,dataBukalapak,selectProxy

  if request.method == 'POST':
    produk , selectProxy = request.form['produk'] , request.form['inlineRadioOptions']
    session['produk'] = produk 
    return render_template('waiting.html')
    
  return render_template('index.html',proxy=selectProxy,dataTokopedia=dataTokopedia,dataBukalapak=dataBukalapak,dataLazada=dataLazada)

@app.route('/wait')
def wait():
  global dataTokopedia,dataLazada,dataBukalapak,selectProxy
  produk = session['produk']

  scraping = MainScraping(selectProxy,produk)
  dataTokopedia,dataLazada,dataBukalapak=scraping.scrapingWebsite()

  return jsonify("wait")

@app.route('/result')
def result():
  global dataTokopedia,dataLazada,dataBukalapak,selectProxy
  produk = session['produk']
  return render_template('index.html',produk=produk,proxy=selectProxy,dataTokopedia=dataTokopedia,dataBukalapak=dataBukalapak,dataLazada=dataLazada)

@app.route('/about',methods=['GET'])
def about():
  return render_template('about.html')

if __name__ == "__main__":
  
  app.run()