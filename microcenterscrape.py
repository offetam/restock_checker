import requests
from bs4 import BeautifulSoup
import re
import microcenter
import pandas as pd
agent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
URL2='https://www.microcenter.com'
records=[]
for y in microcenter.uniqueArr:
    page=requests.get(URL2+y)
    page.raise_for_status()
    soup=BeautifulSoup(page.text,'html.parser')
    title=soup.findAll('div',{'class': "StandardSku"})
    title_string=str(title)
    
    title2=soup.findAll('span',{'id': "pricing"})
    title2_string=str(title2)
    
    uniquename=re.findall('(?<=data-name=").*?(?=" data-position=)',title_string)
    uniqueprice=re.findall('(?<=</span>).*?(?=</span>)',title2_string)
    records.append([uniquename[0],uniqueprice[0],URL2+y])
header=['Name','Price','Link']
df=pd.DataFrame(records,columns=header)
df.to_csv('microcenterdata.csv',index=False)