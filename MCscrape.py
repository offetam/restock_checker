import requests
from bs4 import BeautifulSoup
import re
import microcenter
import pandas as pd
import time
agent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
URL2='https://www.microcenter.com'
records=[]
#start_time = time.time()
for y in microcenter.uniqueArr:
    page=requests.get(URL2+y,headers=agent)
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
  
    #print(title4_string)
    uniquename=re.findall('(?<=data-name=").*?(?=" data-position=)',title_string)
    uniquebrand=re.findall('(?<=data-brand=").*?(?=" data-category)',title_string)
    uniqueprice=re.findall('(?<=</span>).*?(?=</span>)',title2_string)
    sku=re.findall('(?<=<div class="SKUNumber">).*?(?=</div></div>)',title3_string)
    model=re.findall('(?<=Mfr Part#</div><div>).*?(?=</div></div>)',title3_string)
    
    try: 
        image=re.findall('(?<=src=).*?(?=/>)', title4_string)[0]
    except:
        image = ['none']

    print(uniqueprice[0])
    if len(model)==0:
        model.append('None')
    if len(sku):
        sku.append('None')
    if len(image) == 0:
        image = ["none"]
    
    records.append([uniquebrand[0]+' '+uniquename[0],uniqueprice[0],sku[0],model[0], image[0],URL2+y])
header=['MicroCenter_Name','MicroCenter_Price','MicroCenter_SKU','MicroCenter_Model Number','MicroCenter_Link','MicroCenter_Image']
#df=pd.DataFrame(records,columns=header)
#df.to_csv('microcenterdata.csv',index=False)
#print ("My program took", time.time() - start_time, "to run")