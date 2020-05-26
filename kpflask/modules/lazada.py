class Lazada:
    driver,batas="",0
    linkTool=""
    def __init__(self,linkTool,driver,batas):
        linkURLLazada="https://www.lazada.co.id/"
        self.driver,self.batas=driver,batas
        driver.get(linkURLLazada)
        self.linkTool=linkTool
        driver.refresh()
        time.sleep(1)
        
            
    # cekCaptcha Page
    def __cekCaptcha(self):
        driver=self.driver
        return BeautifulSoup(driver.page_source,'lxml').find(lambda tag:tag.name=="title" and "captcha" in tag.text) != None
    
    def __prosesCaptcha(self):
        driver=self.driver
        scrapping = BeautifulSoup(driver.page_source,'lxml')
        #passing recaptha slider
        count=0
        while(self.__cekCaptcha()):
            if BeautifulSoup(driver.page_source,'lxml').find(id='nc_2_n1z') != None:
                if count == 3:
                    return
                src = driver.find_element_by_id('nc_2_n1z')
                ActionChains(driver).drag_and_drop_by_offset(src, 260, 0).perform()
            else:
                count+=1
                driver.get(driver.current_url)
                time.sleep(5)
        driver.get(driver.current_url)
        driver.execute_script('window.scrollBy(0, 200)');
    
    def __waitingPageMain(self,pos):
        driver=self.driver
        script='document.querySelector("#root > div > div.ant-row.c10-Cg > div.ant-col-24 > div > div.ant-col-20.ant-col-push-4.c1z9Ut > div.c1_t2i > div:nth-child({})")'.format(pos)
        while(driver.execute_script('return '+script) == None ):
            # Untuk trigger supaya page dapat loading
            driver.execute_script('window.scrollBy(0, 200)');
            driver.execute_script('window.scrollBy(0, -200)');
            time.sleep(.3)
    
    def __getAllNonRating(self):
        batas=self.batas
        driver=self.driver
        # memprioritaskan data barang yang dikeluarkan adalah data barang yang memiliki rating
        driver.execute_script('document.querySelector("#root > div > div.ant-row.c10-Cg > div.ant-col-24 > div > div.ant-col-4.ant-col-pull-20.c2cfh3 > div > div:nth-child(7) > div.c2uiAC > div:nth-child(1)").click();')
        time.sleep(10)
        scrapping = BeautifulSoup(driver.page_source,'lxml')
        if driver.execute_script('return document.querySelector("#root > div > div.ant-row.c10-Cg > div.ant-col-24 > div > div.ant-col-20.ant-col-push-4.c1z9Ut > div.c2Ce34 > div.c1nVRb")') != None:
            return -1
        count_data = 0 #initial count dari 0
        # waiting time
        self.__waitingPageMain(batas-1)
        Semua = scrapping.findAll('div', attrs={'class':'c2prKC'})
        arraylink=[]
        for data in Semua:
            if count_data==batas:
                break
            count_data+=1            
            link = "https:"+data.find('a')['href']
            judul=data.find('div',attrs={'c16H9d'})
            harga=data.find('span',attrs={'c13VH6'})
            yield [link,judul.text,harga.text[2:].replace(".","")]


    def __getRating(self):
        driver=self.driver
        time.sleep(5)
        for i in range(5):
            script =  'document.querySelector("#module_product_review > div > div:nth-child(1) > div.mod-rating > div > div > div.detail > ul > li:nth-child({}) > span.percent")'.format(i+1)
            hasil= driver.execute_script('return '+script) 
            script += '.textContent'
            yield driver.execute_script('return '+script)  if hasil != None else '0';

    def search(self):
        driver=self.driver
        linkTool=self.linkTool
        driver.execute_script('document.querySelector("#q").value="{}";'.format(linkTool.replace("+", " ")))
        driver.execute_script('document.querySelector("#topActionHeader > div > div.lzd-logo-bar > div > div.lzd-nav-search > form").submit();')
        time.sleep(1)
        
    def generateDataset(self):
        driver=self.driver
        self.search()
        self.__prosesCaptcha()
        try:
            dataNonRating=list(self.__getAllNonRating()) 
            if dataNonRating == []:
                return ["Not Found"]
            dataLink=array(dataNonRating)
            for num,link in enumerate(list(dataLink[:,0])) :
                driver.get(link)
                time.sleep(0.3)
                driver.execute_script('window.scrollBy(0, 3500)');
                dataNonRating[num].append(list(self.__getRating()))
            return dataNonRating
        except:
            if dataNonRating != None:
                return dataNonRating
            return ["Access Denied"]