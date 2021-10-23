
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import time
import csv

# open chrome
chrome_options = Options()
#chrome_options.add_argument("--headless") #REMOVE COMMENTS FOR HEADLESS
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()


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

    '''
    #find img url
    imgtag = item.a.img 
    t_img = str(imgtag)
    img_url = re.findall(r'src="(.*)"\/>',t_img)[0]
    '''
    '''
    #find item url
    url_tag = item.find("a","title_ip0F69brFR7q991bIVYh1")
    url = "https://www.bhphotovideo.com" + url_tag.get("href")
    '''

    #get review
    try:
        review_parent = item.find("a","ratingLink_3h79l-JEkjtWP9MVCF2z3a")
        reviewlist = review_parent.find_all("svg")
        starlist = []
        for i in reviewlist:
            star = str(i)
            starr = re.findall(r'class=\"(.*)\" height', star)[0]
            starlist.append(starr)

        review = 0.0
        for i in starlist:
            if i == "bhIcon star_3iCe453LqwrKpys0-5fEKx full_3EG7E-E7rKfryMFfiMHoEo":
                review += 1
            elif i == "bhIcon star_3iCe453LqwrKpys0-5fEKx":
                review += 0.5
    except AttributeError:
        review = 0.0

    #get number of reviews
    try:
        review_num = item.find("span","reviews_bV6aIRyuom7XD61RdmPUG").text
        review_num = int(review_num[0])
    except AttributeError:
        review_num = 0

    result = [sku,price,stock,review,review_num]
    return result

url = "https://www.bhphotovideo.com/c/buy/Graphic-Cards/ci/6567/pn/"
records = []

#pagination
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
    
for item in records:
        print(item)

print(len(records))
#251
#driver.close()


#REMOVE COMMENTS TO SAVE TO CSV
#save data to csv
with open('b&h_update.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Sku','Price','Stock','Review','Number_of_Reviews'])
    writer.writerows(records)
    




