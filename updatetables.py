from django.db.models.expressions import F
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
from pages.views import update,email_notify
import schedule
from datetime import date
chrome_options = Options()
chrome_options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
agent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', "Accept-Encoding": "*",
    "Connection": "keep-alive"}
def cleanWord(word):
    word=word.replace(" ","")
    return str(word)
def cleanPrice(word):
    word=word.replace("\"","")
    word=word.replace("$","")
    word=word.replace(",","")
    return float(word)
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
            img = re.findall('(?<=src=").*?(?=" srcset)',str(i))
            xd=zip(price,status,sku,img)
            records.append(list(xd))
    
    page=requests.get(xboxURL,headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('li', class_="sku-item")
    for i in title:
            sku=re.findall('(?<=sku-item" data-sku-id=").*?(?=">)',str(i))
            price=re.findall('(?<=-->).*?(?=</span>)',str(i))
            status=re.findall('(?<=data-button-state=").*?(?=" data-sku-id)',str(i))
            img = re.findall('(?<=src=").*?(?=" srcset)',str(i))
            xd=zip(price,status,sku,img)
            records.append(list(xd))
    page=requests.get(ps5URL,headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('li', class_="sku-item")
    for i in title:
            sku=re.findall('(?<=sku-item" data-sku-id=").*?(?=">)',str(i))
            price=re.findall('(?<=-->).*?(?=</span>)',str(i))
            status=re.findall('(?<=data-button-state=").*?(?=" data-sku-id)',str(i))
            img = re.findall('(?<=src=").*?(?=" srcset)',str(i))
            xd=zip(price,status,sku,img)
            records.append(list(xd))
    
    dfnewbest=pd.DataFrame(records,columns=['newPrice','newStatus','BestBuy_SKU'])
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
        uptrends(inStock)
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
    dfnewGame=pd.DataFrame(records,columns=['GameStop_SKU','newPrice','newStock'])
    dfnewGame['newPrice']=dfnewGame['newPrice'].apply(cleanPrice)
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


def doupdate():
    updateBest()
    print(1)
    updateMicro()
    print(2)
    updateAMZN()
    print(3)
    updateGame()
    print(4)

doupdate()
schedule.every(1).minutes.do(doupdate)
schedule.every().day.at("00:01").do(trends)
while 1:
    schedule.run_pending()
    time.sleep(1)

driver.quit()