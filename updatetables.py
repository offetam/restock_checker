import uuid
import pandas as pd 
import time
from pandas.core.indexes.base import Index 
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
from pages.views import update,email_notify,addProduct,addtovendor
import schedule
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import date

chrome_options = Options()
chrome_options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
agent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', "Accept-Encoding": "*",
    "Connection": "keep-alive"}
def fuzzy_merge(df_1, df_2, key1, key2, threshold):
    list1 = df_1[key1].tolist()
    list2 = df_2[key2].tolist()
    mat1=[]
    mat2=[]
    for i in list1:
        mat1.append(process.extractOne(i,list2,scorer=fuzz.token_set_ratio))
    df_1['matches']=mat1
    p=[]
    for j in df_1['matches']:
        if j[1]>=threshold:
            p.append(j[0])
        mat2.append(",".join(p))        
        p=[]
    df_1['matches']=mat2
    return df_1
def name(word):
    word=word.replace("Technologies","")
    word=word.replace("  "," ")
    return word
def normBestbuy(word):
    word=word.replace('(rev2.0)',"Rev 2")
    word=word.replace("- ","")
    word=word.replace("-"," ")
    word=word.replace("PCI Express","PCIe")
    word=word.replace("PCI EXPRESS","PCIe")
    word=word.replace("Black","")
    word=word.replace(";","")
    word=word.replace("Steel and","")
    word=word.replace("Titanium and","")
    word=word.replace("/Silver","")
    word=word.replace("/Gray","")
    word=word.replace("Dark Platinum and","")
    word=word.replace("White","")
    word=word.replace("Unlocked Desktop Processor","")
    word=word.replace("Locked Desktop Processor","")
    word=word.replace("Socket ","")
    word=word.replace("\"","")
    word=word.replace("$","")
    word=word.replace("LIGHT HASH RATE","")
    word=word.replace("LHR","")
    word=word.replace("  "," ")
    
    if word[0:14]=='NVIDIA GeForce':
        word=word.replace('NVIDIA GeForce','NVIDIA GeForce Founder Edition')
    return word.strip()
def normMicro(word):
    word=word.replace(" -","")
    word=word.replace("-"," ")
    word=word.replace("Single-Fan ","")
    word=word.replace("Single Fan","")
    word=word.replace("Dual-Fan ","")
    word=word.replace("Dual Fan","")
    word=word.replace("Triple-Fan ","")
    word=word.replace("Triple Fan","")
    word=word.replace("Overclocked","OC")
    word=word.replace("Heatsink Not Included","")
    word=word.replace("Quad","4")
    word=word.replace("Six","6")
    word=word.replace("Eight","8")
    word=word.replace("Ten","10")
    word=word.replace(" Boxed Processor","")
    word=word.replace("\"","")
    word=word.replace("LHR","")
    word=word.replace("  "," ")
    word=word.replace("White","")
    return word
def normGame(word):
    word=word.replace("PCI Express","PCIe")
    word=word.replace("Triple Fan","")
    word=word.replace("Dual Fan","")
    word=word.replace("LHR","")
    if "Gaming X" in word:
        word="MSI "+word
    if 'NVIDIA GeForce' in word:
        word=word
    else:
        word=word.replace('GeForce','NVIDIA GeForce')
    return word
def normAdor(word):
    word=word.replace("\"","")
    word=word.replace("New Arrival - ","")
    word=word.replace("RGB ","")
    word=word.replace(",","")
    word=word.replace("Triple Fan","")
    word=word.replace("Dual Fan","")
    word=word.replace("Dual-Fan","")
    word=word.replace("iCX3 Cooling","")
    word=word.replace("iCX3 Technology","")
    word=word.replace("Single Fan","")
    word=word.replace("  "," ")
    word=word.replace("Black ","")
    
    return word
def normBH(word):
    word=word.replace("Technologies ","")
    word=word.replace("LHR","")
    word=word.replace("Edition","")
    word=word.replace("(Rev 1.0","R1")
    word=word.replace("(Rev 2.0","R2")
    word=word.replace("(Rev. 2.0)","R2")
    word=word.replace("  "," ")
    word=word.replace("BLACK","")
    word=word.replace("Black","")
    return word
def normAMZN(word):
    if 'Card' in word:
        i= word.index('Card')
        word=word[:i+4]
    word=word.replace(",","")
    if "-" in word:
        i=word.index("-")
        word=word[:i]
    
    return word
def cleanWord(word):
    word=str(word)
    word=word.replace(" ","")
    return str(word)
def cleanPrice(word):
    word=word.replace("\"","")
    word=word.replace("$","")
    word=word.replace(",","")
    return float(word)
def addproducts(store,df):
    listadd=[]
    if store=="BestBuy":
        listadd.append(df['BestBuy_Name'].tolist())
        listadd.append(df['BestBuy_Image'].tolist())
        listadd.append(df['UUID'].tolist())
    if store=="MicroCenter":
        listadd.append(df['MicroCenter_Name'].tolist())
        listadd.append(df['Product_Image'].tolist())
        listadd.append(df['UUID'].tolist())
    if store=="Amazon":
        listadd.append(df['Amazon_Name'].tolist())
        listadd.append(df['Amazon_Image'].tolist())
        listadd.append(df['UUID'].tolist())
    if store=="GameStop":
        listadd.append(df['Name'].tolist())
        listadd.append(df['Images'].tolist())
        listadd.append(df['UUID'].tolist())
    
    addProduct(listadd)
def updateBest():
    """
    df=pd.read_csv('testingBest.csv')
    df['BestBuy_SKU']=df['BestBuy_SKU'].apply(cleanWord)
    df['BestBuy_Status']=df['BestBuy_Status'].apply(cleanWord)
    listLink=df['BestBuy_Link'].tolist()
    records=[]
    for x in listLink:
        page=requests.get(x,headers=agent)
        page.raise_for_status()
        soup=BeautifulSoup(page.content,'html.parser')
        
        title2=soup.find('div', class_='priceView-hero-price priceView-customer-price')
        title2_string=str(title2)
    
        title3=soup.findAll('div', {'style':"position:relative"})
        title3_string=str(title3)

        title5=soup.findAll('span', class_='product-data-value body-copy')
        title5_string=str(title5)
        price=re.search('(?<=<span aria-hidden="true">).*?(?=</span><span class=")',title2_string)
        status=re.search('(?<=data-button-state=").*?(?=" data-sku-id=")',title3_string)
        productcode=re.findall('(?<=copy">).*?(?=</span>)',title5_string)
        if len(productcode)==0:
            productcode=['None','None']
        elif len(productcode)==1:
            productcode=['None',productcode[0]]
        records.append([price[0],status[0],productcode[1]])
    """
    df=pd.read_csv('testingBest.csv')
    df['BestBuy_SKU']=df['BestBuy_SKU'].apply(cleanWord)
    df['BestBuy_Status']=df['BestBuy_Status'].apply(cleanWord)
    URL='https://www.bestbuy.com/site/searchpage.jsp?cp='
    xboxURL='https://www.bestbuy.com/site/searchpage.jsp?st=xbox&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
    ps5URL='https://www.bestbuy.com/site/searchpage.jsp?st=ps5&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
    end='&id=pcat17071&st=graphics+card'
    records=[]
    for x in range(1,8,1):
        page=requests.get(URL+str(x)+end, headers=agent)
        soup=BeautifulSoup(page.content,'html.parser')
        title=soup.findAll('li', class_="sku-item")
        
        
        #titleprice=soup.findAll('div', class_="priceView-hero-price priceView-customer-price")
        #titleprice_string=str(titleprice)

        #titlestatus=soup.findAll('div', class_="sku-list-item-button")
        #titlestatus_string=str(titlestatus)
        for i in title:
            sku=re.findall('(?<=sku-item" data-sku-id=").*?(?=">)',str(i))
            price=re.findall('(?<=-->).*?(?=</span>)',str(i))
            status=re.findall('(?<=data-button-state=").*?(?=" data-sku-id)',str(i))
            records.append([sku[0],price[0],status[0]])
            
   
    page=requests.get(xboxURL,headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('li', class_="sku-item")
    for i in title:
            sku=re.findall('(?<=sku-item" data-sku-id=").*?(?=">)',str(i))
            price=re.findall('(?<=-->).*?(?=</span>)',str(i))
            status=re.findall('(?<=data-button-state=").*?(?=" data-sku-id)',str(i))
            if (len(sku)>0 and len(price)>0 and len(status)>0):
                if(price[0].isnumeric()):
                    records.append([sku[0],price[0],status[0]])
    
    page=requests.get(ps5URL,headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('li', class_="sku-item")
    for i in title:
            sku=re.findall('(?<=sku-item" data-sku-id=").*?(?=">)',str(i))
            price=re.findall('(?<=-->).*?(?=</span>)',str(i))
            status=re.findall('(?<=data-button-state=").*?(?=" data-sku-id)',str(i))
            if (len(sku)>0 and len(price)>0 and len(status)>0):
                if(price[0].isnumeric()):
                    records.append([sku[0],price[0],status[0]])
    
    
   
    dfnewbest=pd.DataFrame(records,columns=['BestBuy_SKU','newPrice','newStatus'])#,columns=['newPrice','newStatus','BestBuy_SKU'])
   
    
    
    dfnewbest['newPrice']=dfnewbest['newPrice'].apply(cleanPrice)
    dfnewbest['BestBuy_SKU']=dfnewbest['BestBuy_SKU'].apply(cleanWord)
    dfnewbest['newStatus']=dfnewbest['newStatus'].apply(cleanWord)
    dfnewbest=dfnewbest.drop_duplicates(subset=['BestBuy_SKU'])
    combinedf=pd.merge(df,dfnewbest,on='BestBuy_SKU',how='left')
    combinedf['change']=combinedf.apply(lambda x: (((x['BestBuy_Status']!=x['newStatus'])or(x['BestBuy_Price']!=x['newPrice'])) and (x['newPrice']>0) and (len(x['newStatus'])>0)),axis=1)
    onlyChange=combinedf[combinedf['change']]
    listchange=[]
    listchange.append(onlyChange['UUID'].tolist())
    listchange.append(onlyChange['BestBuy_SKU'].tolist())
    listchange.append(onlyChange['newPrice'].tolist())
    listchange.append(onlyChange['newStatus'].tolist())
    inStock=[]
    
    for i in range(len(listchange[0])):
        if 'OUT' not in listchange[3][i]:
            inStock.append(listchange[0][i])
    if(len(listchange[0])>0):
        update('BestBuy',listchange)
    if(len(inStock)>0):
        email_notify('BestBuy',inStock)
        #uptrends(inStock)
    combinedf['BestBuy_Price']=combinedf.apply(lambda x: x['newPrice'] if x['change']==True else x['BestBuy_Price'],axis=1)
    combinedf['BestBuy_Status']=combinedf.apply(lambda x: x['newStatus'] if x['change']==True else x['BestBuy_Status'],axis=1)
    combinedf=combinedf.drop(columns=['newStatus','newPrice','change'])
    combinedf.to_csv('testingBest.csv',index=False)
def updateMicro():
    df=pd.read_csv('testingMicro.csv')
    df['MicroCenter_SKU']=df['MicroCenter_SKU'].astype(str)
    linklist=df['MicroCenter_Link'].tolist()
    records=[]
    for x in linklist:
        page=requests.get(x,headers=agent)
        page.raise_for_status()
        soup=BeautifulSoup(page.text,'html.parser')
        title2=soup.findAll('span',{'id': "pricing"})
        title2_string=str(title2)
        title3=soup.findAll('div', class_="content-wrapper")
        title3_string=str(title3)
        uniqueprice=re.findall('(?<=</span>).*?(?=</span>)',title2_string)
        sku=re.findall('(?<=<div class="SKUNumber">).*?(?=</div></div>)',title3_string)
        if len(sku)==0:
            sku.append('0')
        if len(uniqueprice)==0:
            uniqueprice.append('0')
        records.append([sku[0],uniqueprice[0]])
    dfnewmicro=pd.DataFrame(records,columns=['MicroCenter_SKU','newPrice'])
    
    dfnewmicro['MicroCenter_SKU']=dfnewmicro['MicroCenter_SKU'].apply(cleanWord)
    dfnewmicro['newPrice']=dfnewmicro['newPrice'].apply(cleanPrice)
    dfnewmicro=dfnewmicro.drop_duplicates(subset=['MicroCenter_SKU'])
    combinedf=pd.merge(df,dfnewmicro,on='MicroCenter_SKU',how='left')
    combinedf['change']=combinedf.apply(lambda x: ((x['MicroCenter_Price']!=x['newPrice']) and (x['newPrice']>0) ),axis=1)
    onlyChange=combinedf[combinedf['change']]
    listchange=[]
    listchange.append(onlyChange['UUID'].tolist())
    listchange.append(onlyChange['MicroCenter_SKU'].tolist())
    listchange.append(onlyChange['newPrice'].tolist())
    if len(listchange[0])>0:
        update('Micro',listchange)
    
    combinedf['MicroCenter_Price']=combinedf.apply(lambda x: x['newPrice'] if x['change']==True else x['MicroCenter_Price'],axis=1)
    combinedf=combinedf.drop(columns=['newPrice','change'])
    combinedf.to_csv('testingMicro.csv',index=False)
def updateAMZN():
    def get_url(product):
        #url when searching a product
        template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"
        
        #replace every space with a + in order to get a working url
        product = product.replace(' ', '+')

        #replaces {} with product name
        url = template.format(product)

        return url
    def get_item_price(product):
        try:
            #go to the span tag thats called a-price
            price1 = product.find('span', 'a-price')
            #use price1 because the price is under the tag a-price
            price2 = price1.find('span', 'a-offscreen').text
        except :
            price = 0
            return price
        #get rid of symbols in order to put them in a csv file
        price = price2.replace('$', '')
        price = price.replace(',', '')
        return float(price)
    def get_item_stock(product):
        #find the tag called a-size-base a-color-price to get the stock
        try:
            stock = product.find('span', 'a-size-base a-color-price').text
        except :
            stock = "out of stock"
        return stock
    def create_a_dataframe(product_info):
        headers = ['ASIN', 'newPrice', 'newStock']
        df  = pd.DataFrame(np.array(product_info), columns= headers)
        return df
        #df.to_csv(csv_name + ".csv", index = False)
    def scrape_amazon():
        product_information = []
        searched_item = ['Xbox Series X', 'Playstation 5', '3060 Graphics Card', '3070 Graphics Card', '3080 Graphics Card', '3090 Graphics Card', 'Radeon RX 6900 XT', 'Radeon RX 6800 XT']
        for i in searched_item:
            url = get_url(i)
            #loads the url
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            #number of items
            results = soup.find_all('div', {'data-component-type': 's-search-result'})

            #loop through each item to get info
            for item in results:
                record = [item.get('data-asin'), get_item_price(item),get_item_stock(item)]
                product_information.append(record)

        
        return create_a_dataframe(product_information)
    dfnewAMZN=scrape_amazon()
    dfnewAMZN=dfnewAMZN.drop_duplicates(subset=['ASIN'])
    df=pd.read_csv('testingAMZN.csv')
    combinedf=pd.merge(df,dfnewAMZN,left_on='Amazon_SKU',right_on='ASIN',how='left')
    combinedf['change']=combinedf.apply(lambda x: (((x['price']!=x['newPrice']) or (x['stock']!=x['newStock'])) and (float(x['newPrice']) > 0) and (len(x['newStock'])>0)),axis=1)
    onlyChange=combinedf[combinedf['change']]
    listchange=[]
    listchange.append(onlyChange['UUID'].tolist())
    listchange.append(onlyChange['ASIN'].tolist())
    listchange.append(onlyChange['newPrice'].tolist())
    listchange.append(onlyChange['newStock'].tolist())
    listchange.append(onlyChange['stock'].tolist())
    inStock=[]
    for i in range(len(listchange[0])):
        if str(listchange[3][i]).count('in stock') > str(listchange[4][i]).count('in stock'):
            inStock.append(listchange[0][i])
    if len(listchange[0])>0:
        update('Amazon',listchange)
    if len(inStock)>0:
        email_notify('Amazon',inStock)
        uptrends(inStock)
    combinedf['price']=combinedf.apply(lambda x: x['newPrice'] if x['change']==True else x['price'],axis=1)
    combinedf['stock']=combinedf.apply(lambda x: x['newStock'] if x['change']==True else x['stock'],axis=1)
    combinedf=combinedf.drop(columns=['ASIN','newPrice','newStock','change'])
    combinedf.to_csv('testingAMZN.csv',index=False)
def updateGame(): 
    def extract_info(item):
    #get sku
        sku_parent = str(item.find("div","product-tile product-detail"))
        sku_parent = sku_parent[:80]
        sku = re.findall(r'pid=\"(.*)\">',sku_parent)[0]
        
        #get price
        price_parent = str(item.find_all('span' ,  class_ = "actual-price"))
        price = re.findall(r'\$(.*)',price_parent)[0]

        #get status
        status_parent = str(item.find_all("div","availability product-availability global-availability mb-2"))
        status = re.findall(r'data-available=\"(.*)\" data-is-instock',status_parent)[0]
        if status == 'true':
            stock = 'In Stock'
        else:
            stock = 'Out of Stock'
        result = [sku,price,stock]
        return result
    records = []
    url = "https://www.gamestop.com/search/?q=graphics%20card&view=new&tileView=list&sz=100"
    driver.get(url)
   

    soup = BeautifulSoup(driver.page_source, 'html.parser')


    results = soup.find_all("div", 'product-grid-tile-wrapper')
    for item in results:
        record = extract_info(item)
        if record:
            records.append(extract_info(item))
    df=pd.read_csv('testingGame.csv')
    df['GameStop_SKU']=df['GameStop_SKU'].apply(cleanWord)
    dfnewGame=pd.DataFrame(records,columns=['GameStop_SKU','newPrice','newStock'])
    dfnewGame['newPrice']=dfnewGame['newPrice'].apply(cleanPrice)
    dfnewGame['GameStop_SKU']=dfnewGame['GameStop_SKU'].apply(cleanWord)
    dfnewGame=dfnewGame.drop_duplicates(subset=['GameStop_SKU'])
    combinedf=pd.merge(df,dfnewGame,on='GameStop_SKU',how='left')
    combinedf['change']=combinedf.apply(lambda x: (((x['Product_Stock']!=x['newStock'])or(x['Product_Price']!=x['newPrice'])) and (((x['newPrice'])>0) and ((len(x['newStock']))>0))),axis=1)
    onlyChange=combinedf[combinedf['change']]
    listchange=[]
    listchange.append(onlyChange['UUID'].tolist())
    listchange.append(onlyChange['GameStop_SKU'].tolist())
    listchange.append(onlyChange['newPrice'].tolist())
    listchange.append(onlyChange['newStock'].tolist())
    inStock=[]
    for i in range(len(listchange[0])):
        if 'Out' not in listchange[3][i]:
            inStock.append(listchange[0][i])
    if len(listchange[0])>0:
        update('GameStop',listchange)
    if len(inStock)>0:
        email_notify('Gamestop',inStock)
        uptrends(inStock)
    combinedf['Product_Price']=combinedf.apply(lambda x: x['newPrice'] if x['change']== True else x['Product_Price'],axis=1)
    combinedf['Product_Stock']=combinedf.apply(lambda x: x['newStock'] if x['change']== True else x['Product_Stock'],axis=1)
    combinedf=combinedf.drop(columns=['newPrice','newStock','change'])
    combinedf.to_csv('testingGame.csv',index=False)
def updateBH():
    def extract_info(item):
        #get b&h sku
        sku_parent = item.find("div", "desc_1Tzf71-71iRGoSImRMVVzQ")
        sku = sku_parent.find("div", "sku_1xEagLq5syWf24ghxMo9-4").text
        sku = re.findall(r'# (.*) MFR',sku)[0]

        '''
        #find item name
        atag = item.h3.a
        title = atag.text.strip()
        '''
        try:
            #Find price
            ptag = item.find_all("span", "container_14EdEmSSsYmuetz3imKuAI")
            tprice = str(ptag)
            uppertag = re.findall(r'First">(.*)<\/span><',tprice)[0]
            lowertag = re.findall(r'Second">(.*)<\/sup>',tprice)[0]
            price = uppertag + "." + lowertag
        except IndexError:
            return

        try:
            #get stock info
            stocktag = item.find_all("span", attrs={"data-selenium": "stockStatus"})
            t_stock = str(stocktag)
            stock = re.findall(r'Status">(.*)<\/',t_stock)[0]
        except IndexError:
            return

        
        
        result = [sku,price,stock]
        return result
    url = "https://www.bhphotovideo.com/c/buy/Graphic-Cards/ci/6567/pn/"
    records = []
    for i in range(1,10):
        next_url = url + str(i)
        driver.get(next_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        time.sleep(15)
        #get item
        results = soup.find_all("div", attrs={"data-selenium": "miniProductPageProduct"})
        print(len(results))
        for item in results:
            record = extract_info(item)
            if record:
                records.append(extract_info(item))

        time.sleep(5)
def updateAD():
    def extract_info(item):
        try:
            #get sku
            skutag = item.p.i
            sku = skutag.text.strip()
            sku = re.findall(r': (.*)',sku)[0]
        except AttributeError:
            return
        '''
        #find item name
        atag = item.h2.a
        title = atag.text.strip()
        '''
        try:
            #get price
            price = str(item.find_all("strong","your-price"))
            price = re.findall(r'">(.*)<',price)[0]
        except IndexError:
            return

        try:
            #get stock info
            stocktag = str(item.find_all("button", attrs={"type": "button"}))
            t_stock = re.findall(r'        (.*)',stocktag)[0]
            if t_stock == "Add to Cart":
                stock = "In Stock"
            else:
                stock = "Not in Stock"
        except IndexError:
            return
        result=[sku,price,stock]
        return result
    records=[]
    url = "https://www.adorama.com/l/Computers/Computer-Components/Video-and-Graphics-Cards?startAt="
    end = "&sf=relevance&st=de&perPage=25&sel=Price-Range_-dollar-400-to-dollar-2500"   
    for i in range(0,100,25):
        new_url = url + str(i) +end
        driver.get(new_url)
    

        soup = BeautifulSoup(driver.page_source, 'html.parser')


        time.sleep(25)
        #get item
        results = soup.find_all("div", 'item')
        print(len(results))

        for item in results:
                record = extract_info(item)
                if record:
                    records.append(extract_info(item))
        time.sleep(5)        
def newBest():
    df=pd.read_csv('testingBest.csv')
    df=df[['BestBuy_SKU']]
    URL='https://www.bestbuy.com/site/searchpage.jsp?cp='
    xboxURL='https://www.bestbuy.com/site/searchpage.jsp?st=xbox&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
    ps5URL='https://www.bestbuy.com/site/searchpage.jsp?st=ps5&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
    end='&id=pcat17071&st=graphics+card'
    records=[]
    for x in range(1,8,1):
        page=requests.get(URL+str(x)+end, headers=agent)
        soup=BeautifulSoup(page.content,'html.parser')
        title=soup.findAll('li', class_="sku-item")
        
        for i in title:
            sku=re.findall('(?<=sku-item" data-sku-id=").*?(?=">)',str(i))
            price=re.findall('(?<=-->).*?(?=</span>)',str(i))
            status=re.findall('(?<=data-button-state=").*?(?=" data-sku-id)',str(i))
            rating=re.findall('(?<=class="visually-hidden">).*?(?=</p>)',str(i))
            product=re.findall('(?<=<a href=").*?(?=">)',str(i))
            img = re.findall('(?<=src=").*?(?=" srcset)',str(i))
            model=re.findall('(?<=sku-value">).*?(?=</span>)',str(i))
            name=re.findall('(?<=<a href=").*?(?=</a>)',str(i))
            namesplit=name[0].split(">")
            
            if 'Not yet reviewed' in rating[0]:
                if len(model)>1:
                    records.append([price[0],status[0],0,0,model[0],sku[0],"https://www.bestbuy.com"+product[0],img[0],namesplit[1]])
                else:
                    records.append([price[0],status[0],0,0,"None",sku[0],"https://www.bestbuy.com"+product[0],img[0],namesplit[1]])
            else:
                
                rate=re.findall('(?<=rating, ).*?(?= out)',rating[0])
                rate=float(rate[0])
                review=re.findall('(?<=with ).*?(?= review)',rating[0])
                reviews=int(review[0])
                if len(model)>1:
                    records.append([price[0],status[0],rate,reviews,model[0],sku[0],"https://www.bestbuy.com"+product[0],img[0],namesplit[1]])
                else:
                    records.append([price[0],status[0],rate,reviews,"None",sku[0],"https://www.bestbuy.com"+product[0],img[0],namesplit[1]])
   
    dfnewbest=pd.DataFrame(records,columns=['BestBuy_Price','BestBuy_Status','BestBuy_Rating','BestBuy_Review','BestBuy_Model Number','BestBuy_SKU','BestBuy_Link','BestBuy_Image','BestBuy_Name'])
    dfnewbest['BestBuy_Name']=dfnewbest['BestBuy_Name'].apply(normBestbuy)
    dfnewbest['BestBuy_Price']=dfnewbest['BestBuy_Price'].apply(cleanPrice)
    df['BestBuy_SKU']=df['BestBuy_SKU'].apply(cleanWord)
    dfnewbest['BestBuy_SKU']=dfnewbest['BestBuy_SKU'].apply(cleanWord)
    dfnewbest['BestBuy_Status']=dfnewbest['BestBuy_Status'].apply(cleanWord)
    dfnewbest=dfnewbest.drop_duplicates(subset=['BestBuy_SKU'])
    
    combinedf=pd.merge(df,dfnewbest,on='BestBuy_SKU',how='right',indicator=True).query('_merge=="right_only"').drop('_merge',1)
    combinedf=combinedf.drop_duplicates(subset=['BestBuy_Name'])
    
    productdf=pd.read_csv('testing1.csv')
    
    dfmatch=fuzzy_merge(productdf,combinedf,'Product_Name','BestBuy_Name',99)
    dfmatch=dfmatch[dfmatch.matches != '']
    dfmatch=dfmatch.drop_duplicates(subset=['matches'])
    
    notnew=pd.merge(dfmatch,combinedf,left_on='matches',right_on='BestBuy_Name',how='left')
    notnew=notnew.drop_duplicates(subset=['Product_Name'])
    notnew=notnew[['BestBuy_Price','BestBuy_Status','BestBuy_Rating','BestBuy_Review','BestBuy_Model Number','BestBuy_SKU','BestBuy_Link','BestBuy_Image','UUID']]
    
    list1=notnew['BestBuy_SKU'].tolist()
    addbest=combinedf[~combinedf.BestBuy_SKU.isin(list1)]
    addbest['UUID']=addbest.apply(lambda x: uuid.uuid4(),axis=1)
    
    df=pd.read_csv('testingBest.csv')
    checkUUID=pd.merge(df,notnew,on='UUID',how='inner')
    list2=checkUUID['UUID'].tolist()
    notnew=notnew[~notnew.UUID.isin(list2)]
    
    
    addproduct=addbest[['BestBuy_Name','BestBuy_Image','UUID']]
    addproducts('BestBuy',addproduct)
    
    list4=[]
    list4.append(addproduct['BestBuy_Name'].tolist())
    list4.append(addproduct['UUID'].tolist())
    addtrends(list4)
    
    addbest=addbest[['BestBuy_Price','BestBuy_Status','BestBuy_Rating','BestBuy_Review','BestBuy_Model Number','BestBuy_SKU','BestBuy_Link','BestBuy_Image','UUID']]
    addbest=pd.concat([addbest,notnew])
    
    
    data=[]
    data.append(addbest['BestBuy_Price'].tolist())
    data.append(addbest['BestBuy_Status'].tolist())
    data.append(addbest['BestBuy_Rating'].tolist())
    data.append(addbest['BestBuy_Review'].tolist())
    data.append(addbest['BestBuy_Model Number'].tolist())
    data.append(addbest['BestBuy_SKU'].tolist())
    data.append(addbest['BestBuy_Link'].tolist())
    data.append(addbest['BestBuy_Image'].tolist())
    data.append(addbest['UUID'].tolist())
    addtovendor("BestBuy",data)
    
    #156
    #423
    dftest=pd.read_csv('testing1.csv')
    addproduct=addproduct.rename(columns={'BestBuy_Name':'Product_Name','BestBuy_Image':'Image_URL'})
    addtoproduct=pd.concat([dftest,addproduct])
    addtoproduct.to_csv('testing1.csv',index=False)
    addtobest=pd.concat([addbest,df])
    addtobest.to_csv("testingBest.csv",index=False)
def newMicro():
    URL='https://www.microcenter.com/search/search_results.aspx?N=4294966937&NTK=all&page='
    end='&cat=Graphics-Cards-:-MicroCenter&myStore=false'   
    uniqueArr=[]
    for x in range(1,9,1):
        page=requests.get(URL+str(x)+end,headers=agent)
        page.raise_for_status()
        soup=BeautifulSoup(page.text,"html.parser")
        title=soup.findAll('div',{'class': "normal"})
        title_string=str(title)
        uniqueLink=re.findall('(?<=href=").*?(?=" id=)',title_string)
        for i in uniqueLink:
            uniqueArr.append('https://www.microcenter.com'+i)
    df=pd.read_csv('testingMicro.csv')
    list1=df['MicroCenter_Link'].tolist()
    newitems=list(set(uniqueArr)-set(list1))
    records=[]
    for i in newitems:
        page=requests.get(i,headers=agent)
        page.raise_for_status()
        soup=BeautifulSoup(page.text,'html.parser')
        title=soup.findAll('div',{'class': "StandardSku"})
        title_string=str(title)
        
        title2=soup.findAll('span',{'id': "pricing"})
        title2_string=str(title2)
        
        title3=soup.findAll('div', class_="content-wrapper")
        title3_string=str(title3)
        
        title4 = soup.findAll('img', class_='productImageZoom')
        title4_string = str(title4)
    
        uniquename=re.findall('(?<=data-name=").*?(?=" data-position=)',title_string)
        uniquebrand=re.findall('(?<=data-brand=").*?(?=" data-category)',title_string)
        uniqueprice=re.findall('(?<=</span>).*?(?=</span>)',title2_string)
        sku=re.findall('(?<=<div class="SKUNumber">).*?(?=</div></div>)',title3_string)
        model=re.findall('(?<=Mfr Part#</div><div>).*?(?=</div></div>)',title3_string)
        try: 
            image=re.findall('(?<=src=).*?(?=/>)', title4_string)[0]
        except:
            image = 'none'
        if len(model)==0:
            model.append('None')
        if len(sku):
            sku.append('None')
        if len(image) == 0:
            image = "none"
        
        records.append([uniquebrand[0]+' '+uniquename[0],uniqueprice[0],sku[0],model[0],i,image])
    newdf=pd.DataFrame(records,columns=['MicroCenter_Name','MicroCenter_Price','MicroCenter_SKU','MicroCenter_Model Number','MicroCenter_Link','Product_Image'])
    newdf['MicroCenter_Name']=newdf['MicroCenter_Name'].apply(normMicro)
    newdf=newdf.drop_duplicates(subset=['MicroCenter_SKU'])
    newdf['MicroCenter_Price']=newdf["MicroCenter_Price"].apply(cleanPrice)
    
    productdf=pd.read_csv('testing1.csv')
    checknotnew=fuzzy_merge(productdf,newdf,'Product_Name','MicroCenter_Name',98)
    checknotnew=checknotnew[checknotnew.matches != '']
    checknotnew=checknotnew.drop_duplicates(subset=['matches'])
    
    notnew=pd.merge(checknotnew,newdf,left_on='matches',right_on='MicroCenter_Name',how='left')
    notnew=notnew[['MicroCenter_Name','MicroCenter_Price','MicroCenter_SKU','MicroCenter_Model Number','MicroCenter_Link','Product_Image','UUID']]
    
    list1=notnew['MicroCenter_SKU'].tolist()
    addmicro=newdf[~newdf.MicroCenter_SKU.isin(list1)]
    addmicro['UUID']=addmicro.apply(lambda x:uuid.uuid4(),axis=1)
    
    df=pd.read_csv('testingMicro.csv')
    checkUUID=pd.merge(df,notnew,on='UUID',how='inner')
    list2=checkUUID['UUID'].tolist()
    notnew=notnew[~notnew.UUID.isin(list2)]

    addproduct=addmicro[['MicroCenter_Name','Product_Image','UUID']]
    addproducts('MicroCenter',addproduct)
    list4=[]
    list4.append(addproduct['MicroCenter_Name'].tolist())
    list4.append(addproduct['UUID'].tolist())
    addtrends(list4)
    
    addmicro=addmicro[['MicroCenter_Price','MicroCenter_SKU','MicroCenter_Model Number','MicroCenter_Link','Product_Image','UUID']]
    addmicro=pd.concat([addmicro,notnew])

    data=[]
    data.append(addmicro['MicroCenter_Price'].tolist())
    data.append(addmicro['MicroCenter_SKU'].tolist())
    data.append(addmicro['MicroCenter_Model Number'].tolist())
    data.append(addmicro['MicroCenter_Link'].tolist())
    data.append(addmicro['Product_Image'].tolist())
    data.append(addmicro['UUID'].tolist())
    addtovendor("MicroCenter",data)
    dftest=pd.read_csv('testing1.csv')
    addproduct=addproduct.rename(columns={'MicroCenter_Name':'Product_Name','Product_Image':'Image_URL'})
    addtoproduct=pd.concat([dftest,addproduct])
    addtoproduct.to_csv('testing1.csv',index=False)
    addtomicro=pd.concat([addmicro,df])
    addtomicro.to_csv('testingMicro.csv',index=False)
def newAMZN():
    def get_url(product):
    #replace every space with a + in order to get a working url
        product = product.replace(' ', '+')

        #url when searching a product
        url = f"https://www.amazon.com/s?k={product}&ref=nb_sb_noss_1"

        return url

    def get_item_name(product):
        #gets the h2 tag of the product
        tag = product.find('a', 'a-link-normal a-text-normal')
        
        #strip extra info in order to get the name(text)
        product_name = tag.text
        return product_name


    def get_item_url(product):
        #gets the h2 tag of the product
        tag =  product.find('a', 'a-link-normal a-text-normal')

        #gets the url of a specific product
        url = 'https://www.amazon.com' + tag.get('href')

        return url


    def get_item_price(product):
        try:
            #go to the span tag thats called a-price
            price1 = product.find('span', 'a-price')
            #use price1 because the price is under the tag a-price
            price2 = price1.find('span', 'a-offscreen').text
        except :
            price = 0
            return price
        #get rid of symbols in order to put them in a csv file
        price = price2.replace('$', '')
        price = price.replace(',', '')
        return float(price)


    def get_item_rating(product):
        #get the tag i and only get text
        try:
            rating = product.i.text
            rating = rating[:3]
            if len(rating[0])<0:
                rating=0
        except :
            rating = 0
            return rating
        return rating


    def get_number_of_reviews(product):
        try:
            parent = product.find('div', 'a-row a-size-small')
            number_of_reviews = parent.find('span', 'a-size-base').text
        except:
            number_of_reviews = 0
            return number_of_reviews
        return number_of_reviews


    def get_item_stock(product):
        #find the tag called a-size-base a-color-price to get the stock
        try:
            stock = product.find('span', 'a-size-base a-color-price').text
        except :
            stock = "out of stock"
        return stock

    def get_img(product):
        img = product.find('img', 's-image')
        
        found = img.get('src')

        return found


    def create_a_dataframe(csv_name, product_info):
        headers = ['Amazon_SKU', 'Amazon_Price', 'Amazon_Ratings', 'Amazon_Reviews', 'Amazon_Status', 'Amazon_Image','Amazon_Name','Amazon_URL']
        df = pd.DataFrame(np.array(product_info), columns= headers)
        #df.to_csv(csv_name + ".csv", index = False)
        return df

    def scrape_amazon():
        #hides chrome
        product_information = []
        searched_item = ['3060 Graphics Card', '3070 Graphics Card', '3080 Graphics Card', '3090 Graphics Card', 'Radeon RX 6900 XT', 'Radeon RX 6800 XT']
        for i in searched_item:
            url = get_url(i)
        
            #loads the url
            driver.get(url)

            #get page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            #number of items
            results = soup.find_all('div', {'data-component-type': 's-search-result'})

            #loop through each item to get info
            for item in results:
                record = [item.get('data-asin'), get_item_price(item), get_item_rating(item), get_number_of_reviews(item), get_item_stock(item), get_img(item), get_item_name(item), get_item_url(item)]
                product_information.append(record)

        #closes google chrome 
        driver.quit()
        

        #create a dataframe with the data collected
        return create_a_dataframe('amazon_update', product_information)

    amazon_df = scrape_amazon()
    amazon_df['Amazon_Name']=amazon_df['Amazon_Name'].apply(normAMZN)
    amazon_df=amazon_df[(amazon_df.Amazon_Name.str.len()>20)]
    
    df=pd.read_csv('testingAMZN.csv')
    df=df['Amazon_SKU']
    combinedf=pd.merge(df,amazon_df,on='Amazon_SKU',how='right',indicator=True).query('_merge=="right_only"').drop('_merge',1)
    combinedf=combinedf.drop_duplicates(subset=['Amazon_Name'])
    
    product_df=pd.read_csv('testing1.csv')
    checknotnew=fuzzy_merge(product_df,amazon_df,'Product_Name','Amazon_Name',97)
    checknotnew=checknotnew[checknotnew.matches != '']
    checknotnew=checknotnew.drop_duplicates(subset=['matches'])

    notnew=pd.merge(checknotnew,amazon_df,left_on='matches',right_on='Amazon_Name',how='left')
    notnew=notnew[['Amazon_SKU', 'Amazon_Price', 'Amazon_Ratings', 'Amazon_Reviews', 'Amazon_Status', 'Amazon_Image','Amazon_Name','Amazon_URL','UUID']]
    
    list1=notnew['Amazon_SKU'].tolist()
    addAMZN=combinedf[~combinedf.Amazon_SKU.isin(list1)]
    addAMZN['UUID']=addAMZN.apply(lambda x:uuid.uuid4(),axis=1)
    
    df=pd.read_csv('testingAMZN.csv')
    checkUUID=pd.merge(df,notnew,on='UUID',how='inner')
    list2=checkUUID['UUID'].tolist()
    notnew=notnew[~notnew.UUID.isin(list2)]

    addproduct=addAMZN[['Amazon_Name','Amazon_Image','UUID']]
    addproducts('Amazon',addproduct)
    
    list4=[]
    list4.append(addproduct['Amazon_Name'].tolist())
    list4.append(addproduct['UUID'].tolist())
    addtrends(list4)
    
    addAMZN=addAMZN[['Amazon_SKU','Amazon_Price','Amazon_Ratings','Amazon_Reviews','Amazon_Status','Amazon_URL','Amazon_Image','UUID']]
    addAMZN=pd.concat([addAMZN,notnew])

    data=[]
    data.append(addAMZN['Amazon_SKU'].tolist())
    data.append(addAMZN['Amazon_Price'].tolist())
    data.append(addAMZN['Amazon_Ratings'].tolist())
    data.append(addAMZN['Amazon_Reviews'].tolist())
    data.append(addAMZN['Amazon_Status'].tolist())
    data.append(addAMZN['Amazon_URL'].tolist())
    data.append(addAMZN['Amazon_Image'].tolist())
    data.append(addAMZN['UUID'].tolist())
    
    addtovendor("Amazon",data)
    
    dftest=pd.read_csv('testing1.csv')
    addproduct=addproduct.rename(columns={'Amazon_Name':'Product_Name','Amazon_Image':'Image_URL'})
    addtoproduct=pd.concat([dftest,addproduct])
    addtoproduct.to_csv('testing1.csv',index=False)
    addAMZN=addAMZN.rename(columns={'Amazon_Price':'price','Amazon_Ratings':'rating','Amazon_Reviews':'number_of_reviews','Amazon_Status':'stock','Amazon_URL':'url','Amazon_Image':'Product_Image'})
    addAMZN=addAMZN[['Amazon_SKU','price','rating','number_of_reviews','stock','url','Product_Image','UUID']]
    addtoAMZN=pd.concat([addAMZN,df])
    addtoAMZN.to_csv("testingAMZN.csv",index=False)
def newGame():
    def extract_info(item):
        #get sku
        sku_parent = str(item.find("div","product-tile product-detail"))
        sku_parent = sku_parent[:80]
        sku = re.findall(r'pid=\"(.*)\">',sku_parent)[0]
        
        #get price
        price_parent = str(item.find_all('span' ,  class_ = "actual-price"))
        price = re.findall(r'\$(.*)',price_parent)[0]

        #get status
        status_parent = str(item.find_all("div","availability product-availability global-availability mb-2"))
        status = re.findall(r'data-available=\"(.*)\" data-is-instock',status_parent)[0]
        if status == 'true':
            stock = 'In Stock'
        else:
            stock = 'Out of Stock'

        #get rating
        rating_parent = str(item.find_all("div","tile-ratings"))
        if 'width' in rating_parent:
            star = re.findall(r'width:(.*)%',rating_parent)[0]
            star = round((float(star)*5)/100,1)
        else:
            star = 0.0
        
        #get number of review
        review_parent = str(item.find_all("div","tile-ratings"))

        if 'd-inline-block align-text-top rating-count' in review_parent:
            review = int(re.findall(r'\((.*)\)',review_parent)[0])
        else:
            review = 0
            
        #get image and url
        image_parent = str(item.find_all('div', 'image-container'))
        image = re.findall('(?<=srcset=").*?(?= 1x)', image_parent)[0]
        url = 'https://www.gamestop.com/' + re.findall('(?<=href=").*?(?=\?)',image_parent)[0]

        #get name
        name = str(item.find_all('a','product-tile-link'))
        name = re.findall('(?<=title=").*?(?=">)',name)[0]

        
        result = [sku,price,stock,star,review,image,url,name]
        return result


    records = []

    #https://www.gamestop.com/search/?q=graphics%20card&view=new&tileView=list&sz=100
    url = "https://www.gamestop.com/search/?q=graphics%20card&view=new&tileView=list&sz=100"


    #pagination
    def scrape_GS():
        driver.get(url)
            
        soup = BeautifulSoup(driver.page_source, 'html.parser')
            
        #get item
        results = soup.find_all("div", 'product-grid-tile-wrapper')
        

        for item in results:
            record = extract_info(item)
            if record:
                records.append(extract_info(item))

        #print(records)

        

        
        headers = ['Sku','Price','Stock','Review','Number_of_Reviews','Images','URL','Name']
        gs_df = pd.DataFrame(np.array(records), columns= headers)

        return gs_df


    gs_df = scrape_GS()
    gs_df['Name']=gs_df['Name'].apply(normGame)
    gs_df=gs_df.rename(columns={'Sku':'GameStop_SKU'})
    df=pd.read_csv('testingGame.csv')
    df['GameStop_SKU']=df['GameStop_SKU'].apply(cleanWord)
    gs_df['GameStop_SKU']=gs_df['GameStop_SKU'].apply(cleanWord)
    gs_df['Price']=gs_df['Price'].apply(cleanPrice)
    
    combinedf=pd.merge(df,gs_df,on='GameStop_SKU',how='right',indicator=True).query('_merge=="right_only"').drop('_merge',1)
    combinedf=combinedf.drop_duplicates(subset=['Name'])
    
    
    productdf=pd.read_csv('testing1.csv')
    dfmatch=fuzzy_merge(productdf,combinedf,'Product_Name','Name',97)
    dfmatch=dfmatch[dfmatch.matches != '']
    dfmatch=dfmatch.drop_duplicates(subset=['matches'])
    
    notnew=pd.merge(dfmatch,combinedf,left_on='matches',right_on='Name',how='left')
    notnew=notnew.drop_duplicates(subset=['Product_Name'])
    
    notnew=notnew[['GameStop_SKU','Price','URL','Stock','UUID_x','Review_y','Number_of_Reviews_y','Images']]
    notnew=notnew.rename(columns={'UUID_x':'UUID','Review_y':'Review','Number_of_Reviews_y':'Number_of_Reviews'})
    
    list1=notnew['GameStop_SKU'].tolist()
    addGame=combinedf[~combinedf.GameStop_SKU.isin(list1)]
    addGame['UUID']=addGame.apply(lambda x: uuid.uuid4(),axis=1)

    df=pd.read_csv('testingGame.csv')
    checkUUID=pd.merge(df,notnew,on='UUID',how='inner')
    list2=checkUUID['UUID'].tolist()
    notnew=notnew[~notnew.UUID.isin(list2)]
    notnew=notnew.rename(columns={'Price':'Product_Price','URL':'Product_link','Stock':'Product_Stock','Images':'Product_Image'})
    addproduct=addGame[['Name','Images','UUID']]
    
    addproducts('GameStop',addproduct)
    
    list4=[]
    list4.append(addproduct['Name'].tolist())
    list4.append(addproduct['UUID'].tolist())
    addtrends(list4)
    
    addGame=addGame[['GameStop_SKU','Price','URL','Stock','UUID','Review_y','Number_of_Reviews_y','Images']]
    addGame=addGame.rename(columns={'Price':'Product_Price','URL':'Product_link','Stock':'Product_Stock','Review_y':'Review','Number_of_Reviews_y':'Number_of_Reviews','Images':'Product_Image'})
    addGame=pd.concat([addGame,notnew])
    
    
    data=[]
    data.append(addGame['GameStop_SKU'].tolist())
    data.append(addGame['Product_Price'].tolist())
    data.append(addGame['Product_link'].tolist())
    data.append(addGame['Product_Stock'].tolist())
    data.append(addGame['UUID'].tolist())
    data.append(addGame['Review'].tolist())
    data.append(addGame['Number_of_Reviews'].tolist())
    data.append(addGame['Product_Image'].tolist())
    addtovendor('GameStop',data)
    
    dftest=pd.read_csv('testing1.csv')
    addproduct=addproduct.rename(columns={'Name':'Product_Name','Images':'Image_URL'})
    addtoproduct=pd.concat([dftest,addproduct])
    addtoproduct.to_csv('testing1.csv',index=False)
    addtoGame=pd.concat([addGame,df])
    addtoGame.to_csv('testingGame.csv',index=False)
def trends():
    df=pd.read_csv('Trends.csv')
    today = date.today()
    d1=today.strftime("%m/%d/%Y")
    if(len(df.columns)<17):
       df[d1]=0
    else:
        df=df.drop(df.columns[2],axis=1)
        df[d1]=0
    df.to_csv('Trends.csv',index=False)
def uptrends(arr):
    df=pd.read_csv('Trends.csv')
    today = date.today()
    d1=today.strftime("%m/%d/%Y")
    for i in arr:
        df[d1]=df.apply(lambda x: 1 if x['UUID']==i and x[d1]!= 1 else x[d1],axis=1)
    df.to_csv('Trends.csv',index=False)    
def addtrends(arr):
    df=pd.read_csv('Trends.csv')
    
    for x in range(len(arr[0])):
        newarr=[]
        arr[1][x]=str(arr[1][x])
        newarr.append(arr[0][x])
        newarr.append(arr[1][x].strip())
        

        for i in range(16):
            newarr.append(-1)
        df.loc[len(df.index)]=newarr
    df.to_csv('Trends.csv',index=False)

 
def doupdate():
    updateBest()
    print(1)
    updateMicro()
    print(2)
    updateAMZN()
    print(3)
    updateGame()
    print(4)
def doadd():
    
    driver = webdriver.Chrome(options=chrome_options)
    newGame()
    print('ADDED NEW GAME')
    newBest()
    print('ADDED NEW BEST')
    
    
    newMicro()
    print('ADDED NEW MICRO') 
    
    
    newAMZN()
    print('ADDED NEW AMAZON')
    driver.quit()
trends()   
doupdate()
schedule.every(1).minutes.do(doupdate)
schedule.every().day.at("00:01").do(trends)
schedule.every().monday.at("00:01").do(doadd)
while 1:
    schedule.run_pending()
    time.sleep(1)


driver.quit()