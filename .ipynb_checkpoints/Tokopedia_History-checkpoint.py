# Mencoba pertama kali request ke Tokopedia
from bs4 import BeautifulSoup
import requests
linkURL="https://www.tokopedia.com/search?st=product&q="
linkTool=input("Mencari Barang: ")
page = requests.get(linkURL+linkTool)
# Gagal, karena terkendala 'Request Time Out'


# Mencoba cara kedua dengan request ke Tokopedia menggunakan 
# Selenium dan Beautiful Soap
from selenium import webdriver
from bs4 import BeautifulSoup
import time
linkURL="https://www.tokopedia.com/search?st=product&q="
linkTool=input("Mencari Barang: ")
batas=int(input("Batas Kemunculan Barang: "))

options = webdriver.ChromeOptions()
options.add_argument('--incognito')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)

driver.get(linkURL+linkTool)

content = driver.page_source
soup = BeautifulSoup(content,'lxml')

Atas = soup.findAll('div', attrs={'class':'ta-product-wrapper'})
Semua = soup.findAll('div', attrs={'class':'_2OBup6Zd'})

TopTwenty=0

# NEW or HOT
for data in Atas:
	if TopTwenty==batas:
		break
	TopTwenty+=1
	link=data.find('a',href=True, attrs={'class':'anchor-overlay'})['href']
	print("Link\t: ",link)
	judul=data.find('span',attrs={'ta-product-title'})
	print("Judul\t: ",judul.text)
	harga=data.find('span',attrs={'ta-product-price'})
	print("Harga\t: ",harga.text)
	rating=data.find('span',attrs={'ta-product-rating-count'})
	print("Rating\t: ","(0)" if rating == None else rating.text)
	print()
# ALL
for data in Semua:
	if TopTwenty==batas:
		break
	TopTwenty+=1
	link=data.find('a')['href']
	print("Link\t: ",link)
	judul=data.find('h3',attrs={'Ka_fasQS'})
	print("Judul\t: ",judul.text)
	harga=data.find('span',attrs={'_3fNeVBgQ'})
	print("Harga\t: ",harga.text)
	rating=data.find('span',attrs={'_3-hbLA9j'})
	print("Rating\t: ","(0)" if rating == None else rating.text)
	print()
driver.quit()
# Berhasil, tetapi harus membuka aplikasi chrome.
# Hal ini akan mengurangi performance Scrapping


# Mencoba cara ketiga dengan request ke Tokopedia menggunakan 
# Selenium dan Beautiful Soap dengan Headless dan User Agent
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
linkURL="https://www.tokopedia.com/search?st=product&q="
linkTool=input("Mencari Barang: ")
batas=int(input("Batas Kemunculan Barang: "))


options = webdriver.ChromeOptions()
options.add_argument('--incognito')

options.add_argument('user-agent={0}'.format(user_agent))
options.add_argument('--headless')

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True 
capabilities['acceptInsecureCerts'] = True

driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get(linkURL+linkTool)

content = driver.page_source
soup = BeautifulSoup(content,'lxml')

Atas = soup.findAll('div', attrs={'class':'ta-product-wrapper'})
Semua = soup.findAll('div', attrs={'class':'_2OBup6Zd'})

TopTwenty=0

# NEW or HOT
for data in Atas:
	if TopTwenty==batas:
		break
	TopTwenty+=1
	link=data.find('a',href=True, attrs={'class':'anchor-overlay'})['href']
	print("Link\t: ",link)
	judul=data.find('span',attrs={'ta-product-title'})
	print("Judul\t: ",judul.text)
	harga=data.find('span',attrs={'ta-product-price'})
	print("Harga\t: ",harga.text)
	rating=data.find('span',attrs={'ta-product-rating-count'})
	print("Rating\t: ","(0)" if rating == None else rating.text)
	print()
# ALL
for data in Semua:
	if TopTwenty==batas:
		break
	TopTwenty+=1
	link=data.find('a')['href']
	print("Link\t: ",link)
	judul=data.find('h3',attrs={'Ka_fasQS'})
	print("Judul\t: ",judul.text)
	harga=data.find('span',attrs={'_3fNeVBgQ'})
	print("Harga\t: ",harga.text)
	rating=data.find('span',attrs={'_3-hbLA9j'})
	print("Rating\t: ","(0)" if rating == None else rating.text)
	print()
driver.quit()
#Berhasil