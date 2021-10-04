"""
Gets SKU from bestbuy and places them into a list which is used for the bestbuy api search
"""
import requests
import time
from bs4 import BeautifulSoup 
import re

URL='https://www.bestbuy.com/site/searchpage.jsp?cp='
num='1,2,3,4,5,6,7'
end='&id=pcat17071&st=graphics+card'
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
allSKU=['6426149','6430161','6428324','6430277'] 
for x in num[0::2]:
    page = requests.get(URL+x+end, headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('span', class_="sku-value")
    title_string=str(title)
    uniquesku=re.findall('(?<=<span class="sku-value">).*?(?=</span>)',title_string)
    fullline=[]
    for y in uniquesku:
        if(y.isnumeric()):
            fullline.append(y)
    for l in fullline:
        allSKU.append(l)

cpuNum='1,2,3,4'
cpuEnd='&id=pcat17071&st=cpu+processor'
for x in num[0::2]:
    page = requests.get(URL+x+cpuEnd, headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('span', class_="sku-value")
    title_string=str(title)
    uniquesku=re.findall('(?<=<span class="sku-value">).*?(?=</span>)',title_string)
    fullline=[]
    for y in uniquesku:
        if(y.isnumeric()):
            fullline.append(y)
    for l in fullline:
        allSKU.append(l)


