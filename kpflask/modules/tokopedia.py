class Tokopedia:
    batas=""
    driver=""
    linktool=""
    def __init__(self,linkTool,driver,batas):
        linkURLTokopedia="https://www.tokopedia.com/search?st=product&rt=4%2C5&q="
        driver.get(linkURLTokopedia+linkTool)
        driver.execute_script('window.scrollBy(0, 200)');
        self.driver=driver
       
    def __waitingPageRating(self):
        driver=self.driver
        script = 'document.querySelector("#zeus-root > div > div.css-1jdotmr > div:nth-child(5) > div.css-drikti.e1ufc1ph1 > div.css-nvt3av.e1ufc1ph0 > div > div:nth-child(1) > div.css-udfbf8.e1ufc1ph0 > p")'
        while(driver.execute_script('return '+script) == None ):
            # Untuk trigger supaya page dapat loading
            driver.execute_script('window.scrollBy(0, 400)');
            time.sleep(.3)
            
    def __waitingPageMain(self,pos):
        driver=self.driver
        script='document.querySelector("#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div.css-jza1fo > div:nth-child({})")'.format(pos)
        while(driver.execute_script('return '+script) == None ):
            # Untuk trigger supaya page dapat loading
            driver.execute_script('window.scrollBy(0, 100)');
            time.sleep(.3)
            
    def __getAllNonRating(self,driver,batas):
        driver=self.driver
        content = driver.page_source
        scrapping=BeautifulSoup(content,'lxml')
        # memeriksa apakah barangnya ada atau tidak
        if driver.execute_script('return document.querySelector("#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div.css-109jhir > div > div.css-v7ibj3 > div.css-lu7a1o")') != None:
            return -1
        # waiting time
        time.sleep(1)
        self.__waitingPageMain(batas-1)
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


    def __getRating(self):
        driver=self.driver
        for i in range(5):
            script = 'document.querySelector("#zeus-root > div > div.css-1jdotmr > div:nth-child(5) > div.css-drikti.e1ufc1ph1 > div.css-nvt3av.e1ufc1ph0 > div > div:nth-child({}) > div.css-udfbf8.e1ufc1ph0 > p")'.format(i+1)
            hasil= driver.execute_script('return '+script) 
            yield hasil.text if hasil != None else '0'

    def generateDataset(self):
        driver=self.driver
        if 'Access Denied' in BeautifulSoup( driver.page_source,'lxml').find('title').text:
            return ["Access Denied"]
        dataNonRating=list(self.__getAllNonRating(driver,batas)) 
        if dataNonRating == []:
            return ["Not Found"]
        dataLink=array(dataNonRating)
        for num,link in enumerate(list(dataLink[:,0])) :
            driver.get(link)
            if "(" in BeautifulSoup(driver.page_source,'lxml').findAll("span")[2].text:
                self.__waitingPageRating()
            dataNonRating[num].append(list(self.__getRating()))
        return dataNonRating