class Bukalapak:
    driver=""
    linktool=""
    def __init__(self,linkTool,driver,batas):
        linkURLBukalapak="https://www.bukalapak.com/products?utf8=%E2%9C%93&search%5Bkeywords%5D={}&search%5Bsort_by%5D=rating_ratio%3Adesc&search%5Bbrand_seller%5D=0&search%5Bnew%5D=0&search%5Bnew%5D=1&search%5Bused%5D=0&search%5Bused%5D=1&search%5Bfree_shipping_coverage%5D=&search%5Bprovince%5D=&search%5Bcity%5D=&search%5Bcourier%5D=&search%5Bprice_min%5D=&search%5Bprice_max%5D=&search%5Brating_gte%5D=1&search%5Brating_lte%5D=5&search%5Btodays_deal%5D=0&search%5Binstallment%5D=0&search%5Bwholesale%5D=0&search%5Btop_seller%5D=0&search%5Bbrand_seller%5D=0".format(linkTool)
        driver.get(linkURLBukalapak)
        driver.execute_script('window.scrollBy(0, 200)');
        self.driver=driver
       
    def __waitingPageMain(self):
        driver=self.driver
        script='document.querySelector("#mod-product-list-2 > li:nth-child(1) > div > article")'
        while(driver.execute_script('return '+script) == None ):
            # Untuk trigger supaya page dapat loading
            driver.execute_script('window.scrollBy(0, 200)');
            driver.execute_script('window.scrollBy(0, -200)');
            time.sleep(.3)
            
    def __getAllNonRating(self,driver,batas):
        driver=self.driver
        scrapping=BeautifulSoup( driver.page_source,'lxml')
        if driver.execute_script('return document.querySelector("#display_product_search > div.content-segment.blank-slate > p")') != None:
            return -1
        # waiting time
        self.__waitingPageMain()
        Semua = scrapping.findAll('article', attrs={'class':'product-display'})
        Semua = [ filterBekas for filterBekas in Semua if not 'Bekas' in str(filterBekas) ]
        Semua = [ filterTutup for filterTutup in Semua if not 'Lapak Tutup' in str(filterTutup) ]
        Semua = [ filterAktif for filterAktif in Semua if not 'Pelapak Tidak Aktif' in str(filterAktif) ]
        time.sleep(0.5)
        count_data = 0
        arraylink=[]
        for data in Semua:
            if count_data==batas:
                break
            count_data+=1
            link=data.find('a')['href']
            judul=data.find('a',attrs={'product__name'})
            harga=data.find('span',attrs={'amount'})

            yield [link,judul.text,harga.text.replace(".","")]


    def __getRating(self,driver):
        driver=self.driver
        scrapping=BeautifulSoup( driver.page_source,'lxml')
        driver.execute_script('window.scrollBy(0, 1000)');
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
                totalRating = int(totalRating.split()[0])
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
        driver=self.driver
        if 'Attention Required' in BeautifulSoup( driver.page_source,'lxml').find('title').text:
            return ["Access Denied"]
        dataNonRating=list(self.__getAllNonRating(driver,batas))
        if dataNonRating == []:
            return ["Not Found"]
        dataLink=array(dataNonRating)
        for num,link in enumerate(list(dataLink[:,0])) :
            driver.get(link)
            dataNonRating[num].append(list(self.__getRating(driver)))
        return dataNonRating