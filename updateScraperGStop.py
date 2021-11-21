from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import csv


# open chrome
chrome_options = Options()
chrome_options.add_argument("--headless") #REMOVE COMMENTS FOR HEADLESS
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()

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
        
    #get image
    image_parent = str(item.find_all('div', 'image-container'))
    image = re.findall('(?<=srcset=").*?(?= 1x)', image_parent)[0]
    
    
    result = [sku,price,stock,star,review,image]
    return result


records = []

#https://www.gamestop.com/search/?q=graphics%20card&view=new&tileView=list&sz=100
url = "https://www.gamestop.com/search/?q=graphics%20card&view=new&tileView=list&sz=100"


#pagination
driver.get(url)
   

soup = BeautifulSoup(driver.page_source, 'html.parser')


    
#get item
results = soup.find_all("div", 'product-grid-tile-wrapper')
print(len(results))

for item in results:
    record = extract_info(item)
    if record:
        records.append(extract_info(item))

    

print(records)

print(len(records))
#48
driver.close()


#REMOVE COMMENTS TO SAVE TO CSV
#save data to csv
with open('gamestop_update.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Sku','Price','Stock','Review','Number_of_Reviews','Images'])
    writer.writerows(records)
