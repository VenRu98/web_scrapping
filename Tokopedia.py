# from selenium import webdriver
# import time

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--test-type")
# driver = webdriver.Chrome(chrome_options=options) 		
# driver.get('http://codepad.org')

# # click radio button
# python_button = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
# python_button.click()

# # type text
# text_area = driver.find_element_by_id('textarea')
# text_area.send_keys("print('Hello World')")

# # click submit button
# submit_button = driver.find_elements_by_xpath('//*[@id="editor"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[3]/input')[0]
# submit_button.click()
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
options.add_argument('--no-sandbox')

options.add_argument('user-agent={0}'.format(user_agent))
options.add_argument('--headless')


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
# price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
# rating=a.find('div', attrs={'class':'hGSR34 _2beYZw'})
# products.append(name.text)
# prices.append(price.text)
# ratings.append(rating.text) 

# python_button = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
# python_button.click()

# # type text
# text_area = driver.find_element_by_class_name('css-27h1vn')
# text_area.send_keys("bts")

# search = driver.find_element_by_class_name('css-1jpg3ui')
# search.click()
# css-1jpg3ui e1v0ehno1
# # click submit button
# submit_button = driver.find_elements_by_xpath('//*[@id="editor"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[3]/input')[0]
# submit_button.click()
