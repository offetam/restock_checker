"""
Get product link extensions for bestbuy items
"""
import requests
import time
from bs4 import BeautifulSoup 
import re
URL='https://www.bestbuy.com/site/searchpage.jsp?cp='
end='&id=pcat17071&st=graphics+card'
cpuEnd='&id=pcat17071&st=cpu+processor'
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
allexten=[]
for x in range(1,8,1):
    page=requests.get(URL+str(x)+end, headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('h4', class_="sku-header")
    title_string=str(title)
    uniqueexten=re.findall('(?<=<a href=").*?(?=">)',title_string)
    for i in uniqueexten:
        allexten.append(i)
'''
for x in range(1,5,1):
    page=requests.get(URL+str(x)+cpuEnd,headers=agent)
    soup=BeautifulSoup(page.content,'html.parser')
    title=soup.findAll('h4',class_="sku-header")
    title_string=str(title)
    uniqueexten=re.findall('(?<=<a href=").*?(?=">)',title_string)
    for i in uniqueexten:
        allexten.append(i)
'''