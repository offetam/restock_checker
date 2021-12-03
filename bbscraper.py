"""
used to get data from each product link
run time around 4-5min for 1 table of 200 items 3 columns
"""
import bestbuy
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

agent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', "Accept-Encoding": "*",
    "Connection": "keep-alive"}

URL2='https://www.bestbuy.com/site/searchpage.jsp?st=xbox&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
records=[]
start_time = time.time()
for y in bestbuy.allexten:
    page=requests.get(URL2, headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('li', class_="sku-item")
    for i in title:
        #print(i)
        sku=re.findall('(?<=sku-item" data-sku-id=").*?(?=">)',str(i))
        price=re.findall('(?<=-->).*?(?=</span>)',str(i))
        status=re.findall('(?<=data-button-state=").*?(?=" data-sku-id)',str(i))
        img = re.findall('(?<=src=").*?(?=" srcset)',str(i))
        xd=zip(price,status,sku,img)
        records.append(list(xd))
        print(records)


df=pd.DataFrame(records,columns=['BestBuy_Name','BestBuy_Price','BestBuy_Status','BestBuy_Rating','BestBuy_Review','BestBuy_Model Number','BestBuy_SKU','BestBuy_Link','BestBuy_img'])


df.to_csv('bestbuywebdata.csv',index=False)
#print ("My program took", time.time() - start_time, "to run")
