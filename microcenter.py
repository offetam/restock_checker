"""
Used to get /product extension of microcenter
"""
import requests
from bs4 import BeautifulSoup
import re
URL='https://www.microcenter.com/search/search_results.aspx?N=4294966937&NTK=all&page='
end='&cat=Graphics-Cards-:-MicroCenter&myStore=false'
agent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

uniqueArr=[]
for x in range(1,9,1):
    page=requests.get(URL+str(x)+end,headers=agent)
    page.raise_for_status()
    soup=BeautifulSoup(page.text,"html.parser")
    title=soup.findAll('div',{'class': "normal"})
    title_string=str(title)
    uniqueLink=re.findall('(?<=href=").*?(?=" id=)',title_string)
    for i in uniqueLink:
        uniqueArr.append(i)

URL2='https://www.microcenter.com/search/search_results.aspx?N=4294966995&NTK=all&page='
end2='&cat=Processors/CPUs-:-MicroCenter&myStore=false'
for x in range(1,3,1):
    page=requests.get(URL2+str(x)+end2,headers=agent)
    soup=BeautifulSoup(page.text,'html.parser')
    title=soup.findAll('div',{'class': "normal"})
    title_string=str(title)
    uniqueLink=re.findall('(?<=href=").*?(?=" id=)',title_string)
    for i in uniqueLink:
        uniqueArr.append(i)