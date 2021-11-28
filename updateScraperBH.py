
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
    sku = str(item.find_all('div',{'data-selenium':'miniProductPageProductSkuInfo'}))
    try:
        sku = re.findall(r'-->(.*)<!-- --> ',sku)[0]
    except IndexError:
        sku = re.findall(r'# (.*) MFR',sku)[0]
    
    #find item name
    atag = item.h3.a
    title = atag.text.strip()
    
    #Find price
    try:
        tprice = str(item.find_all("span", {'data-selenium':'uppedDecimalPrice'}))
        uppertag = re.findall(r'First">(.*)<\/span><',tprice)[0]
        lowertag = re.findall(r'Second">(.*)<\/sup>',tprice)[0]
        price = uppertag + "." + lowertag
    except IndexError:
        return

    #get stock info
    try:
        stocktag = item.find_all("span", {"data-selenium": "stockStatus"})
        t_stock = str(stocktag)
        stock = re.findall(r'Status">(.*)<\/',t_stock)[0]
    except IndexError:
        return

    #find img url
    imgtag = item.a.img 
    t_img = str(imgtag)
    try:
        img_url = re.findall(r'src="(.*)"\/>',t_img)[0]
    except IndexError:
        img_url = re.findall(r'files\/(.*)"',t_img)[0]
        img_url = 'https://static.bhphoto.com/images/images345x345/' + img_url
    
    

    #find item url
    url_tag = item.find("a",{'data-selenium':'miniProductPageProductNameLink'})
    url = "https://www.bhphotovideo.com" + url_tag.get("href")
    

    
    #get review
    try:
        review_parent = str(item.find_all("div", {"data-selenium": "miniProductPageProductRatingSection"}))
        try:
            reviewlist = re.findall(r'(<svg.*<\/svg>)',review_parent)[0]
        except IndexError:
            reviewlist = []

        
        reviewlist = reviewlist.split('</use></svg>')
        reviewlist = list(filter(None, reviewlist))

        starlist = []
    
        for i in reviewlist: 
            starr = re.findall(r'class=\"(.*)\" height', i)[0]
            starlist.append(starr)
           

        review = 0.0
        for i in starlist:
            if i == "bhIcon star_FU2un8oJ9r full_FU2un8oJ9r":
                review += 1
            elif i == "bhIcon star_FU2un8oJ9r":
                review += 0.5
    except AttributeError:
        review = 0.0


    #get number of reviews
    try:
        review_num = item.find("span", {"data-selenium": "miniProductPageProductReviews"}).text
        review_num = int(review_num[0])
    except AttributeError:
        review_num = 0

    
    result = [sku, title, price, stock, url, review, review_num, img_url]
    
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
    
print(records)

print(len(records))
#251
#driver.close()


#REMOVE COMMENTS TO SAVE TO CSV
#save data to csv
with open('b&h_FINAL_img.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Sku', 'Name', 'Price','Stock','URL', 'Review','Number_of_Reviews','Image_URL'])
    writer.writerows(records)
    




